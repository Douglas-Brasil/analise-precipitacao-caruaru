"""Executa os notebooks existentes em kernels novos e registra evidências locais.

Use .venv/Scripts/python.exe verificar_notebooks.py na raiz do projeto.
Nenhum modelo adicional é treinado. As células de auditoria só medem objetos
já ajustados; elas não são gravadas nos notebooks da apresentação.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import time
import traceback

os.environ.setdefault("LOKY_MAX_CPU_COUNT", "4")
os.environ.setdefault("OMP_NUM_THREADS", "4")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "4")

import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter

ROOT = Path(__file__).resolve().parent
AUDIT = ROOT / "auditoria"
AUDIT.mkdir(exist_ok=True)
OUTPUT = ROOT / "artefatos"
(OUTPUT / "html").mkdir(parents=True, exist_ok=True)
NAME = "INMET_NE_PE_A341_CARUARU_01-01-2025_A_31-12-2025"
FILES = [ROOT / "dataset/df_adaptado.ipynb"] + sorted((ROOT / "notebooks").glob("*.ipynb"))


def hashes():
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT / "dataset").glob("*.CSV")}


def metric_cell(label, model):
    return nbformat.v4.new_code_cell(
        "# Auditoria: métricas calculadas sem novo treinamento.\n"
        "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, matthews_corrcoef, confusion_matrix, classification_report\n"
        "import json\nfrom pathlib import Path\n"
        f"_p = {model}.predict(X_test)\n"
        "_medidas = dict(accuracy=accuracy_score(y_test, _p), precision_chuva=precision_score(y_test, _p, zero_division=0), recall_chuva=recall_score(y_test, _p, zero_division=0), f1_chuva=f1_score(y_test, _p, zero_division=0), mcc=matthews_corrcoef(y_test, _p), confusion_matrix=confusion_matrix(y_test, _p).tolist(), classification_report=classification_report(y_test, _p, output_dict=True, zero_division=0))\n"
        f"_est = {model}.named_steps['modelo'] if hasattr({model}, 'named_steps') else {model}\n"
        "_medidas['hyperparameters'] = _est.get_params()\n"
        f"Path('../auditoria/{label}.json').write_text(json.dumps(_medidas, indent=2), encoding='utf-8')\n"
        "print(_medidas)",
        metadata={"auditoria_local": True},
    )


def main():
    before = hashes()
    expected_file = AUDIT / "hashes_dataset_antes.json"
    if expected_file.exists():
        expected = json.loads(expected_file.read_text(encoding="utf-8"))
        assert before == {k.replace('\\', '/'): v for k, v in expected.items()}, "Datasets divergiram da cópia inicial"
    else:
        expected_file.write_text(json.dumps(before, indent=2), encoding="utf-8")
    summary = []
    for path in FILES:
        start = time.perf_counter()
        print(f"EXECUTANDO {path.relative_to(ROOT)}", flush=True)
        nb = nbformat.read(path, as_version=4)
        original_cells = copy.deepcopy(nb.cells)
        expanded = []
        for index, cell in enumerate(nb.cells):
            expanded.append(cell)
            if path.name == "09_decision_tree.ipynb" and index in (3, 23):
                expanded.append(metric_cell("decision_tree_inicial" if index == 3 else "decision_tree_ajustada", "modelo" if index == 3 else "modelo_hiperparametrizado"))
        if path.name == "09_decision_tree.ipynb":
            expanded.append(nbformat.v4.new_code_cell(
                "# Auditoria das buscas já executadas.\nimport json\nfrom pathlib import Path\n"
                "_buscas = dict(grid=dict(best_params=grid.best_params_, cv_f1=grid.best_score_, test_f1=grid.score(X_test,y_test), candidates=len(grid.cv_results_['params'])), random=dict(best_params=busca.best_params_, cv_f1=busca.best_score_, test_f1=busca.score(X_test,y_test), candidates=len(busca.cv_results_['params'])))\n"
                "Path('../auditoria/buscas.json').write_text(json.dumps(_buscas, indent=2), encoding='utf-8')\nprint(_buscas)", metadata={"auditoria_local": True}))
        if path.name == "10_random_forest.ipynb":
            expanded.append(metric_cell("random_forest", "pipeline_rf"))
        nb.cells = expanded
        record = {"notebook": str(path.relative_to(ROOT)), "status": "OK"}
        try:
            client = NotebookClient(nb, timeout=900, kernel_name="caruaru-venv", allow_errors=False, resources={"metadata": {"path": str(path.parent)}})
            client.execute()
            nb.cells = [c for c in nb.cells if not c.metadata.get("auditoria_local")]
            assert len(nb.cells) == len(original_cells)
            assert all(c.source == old.source for c, old in zip(nb.cells, original_cells))
            nbformat.write(nb, path)
            html, _ = HTMLExporter().from_notebook_node(nb)
            (OUTPUT / "html" / f"{path.stem}.html").write_text(html, encoding="utf-8")
            record["code_cells"] = sum(c.cell_type == "code" for c in nb.cells)
            record["warnings"] = [o.get("text", "") for c in nb.cells for o in c.get("outputs", []) if o.output_type == "stream" and o.get("name") == "stderr"]
        except Exception as exc:
            record.update(status="ERRO", error=f"{type(exc).__name__}: {exc}")
            (AUDIT / f"erro_{path.stem}.txt").write_text(traceback.format_exc(), encoding="utf-8")
            nbformat.write(nb, AUDIT / f"falha_{path.name}")
        finally:
            record["seconds"] = round(time.perf_counter() - start, 2)
            summary.append(record)
            after = hashes()
            assert before == after, "Um dataset fornecido foi alterado"
            (AUDIT / "execucao.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
            (AUDIT / "hashes_dataset_depois.json").write_text(json.dumps(after, indent=2), encoding="utf-8")
            print(f"{record['status']} ({record['seconds']}s)", flush=True)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    if any(r["status"] != "OK" for r in summary):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
