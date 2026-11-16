# Guia rápido — Análise de precipitação em Caruaru

Preparação local em 16/11/2026, para demonstração acadêmica. Repositório: https://github.com/Douglas-Brasil/analise-precipitacao-caruaru

## Acesso imediato

Abra `ABRIR_JUPYTER.cmd` na pasta do projeto. Ele inicia/reutiliza o JupyterLab local e abre este guia no navegador. Em cada notebook, selecione **Python 3.12 (.venv Caruaru)**. Use **Kernel → Restart Kernel and Run All Cells** para demonstrar execução independente.

```powershell
cd C:\Users\sergiobfj\Documents\dev\estudos\faculdade\analise-precipitacao-caruaru
powershell -NoProfile -ExecutionPolicy Bypass -File .\iniciar_jupyter.ps1
```

A URL autenticada da sessão fica em `.jupyter-local/url.txt`. Não publique esse arquivo. O servidor atende somente em `127.0.0.1`, com autenticação padrão do Jupyter. Fechar a aba não encerra o servidor. Para encerrá-lo, na raiz do projeto: `$env:JUPYTER_RUNTIME_DIR = "$PWD\.jupyter-local"; .\.venv\Scripts\jupyter.exe server stop 8888` (substitua a porta caso o inicializador tenha escolhido outra).

**Servidor iniciado e verificado em 16/11/2026: http://127.0.0.1:8888/lab.** O inicializador também foi executado para abrir o guia no navegador. Se a URL simples pedir token, abra `ABRIR_JUPYTER.cmd`, que recupera a URL autenticada sem precisar copiar credenciais.

Uma sessão do notebook 10 foi iniciada pelo servidor e testada com uma célula que confirma o interpretador `.venv\Scripts\python.exe` e o diretório `notebooks/`. O kernel foi deixado disponível; evidência em `auditoria/kernel_servidor.json`. As saídas dos modelos já estão salvas nos notebooks; para treinar ao vivo, reinicie o kernel e execute todas as células.

## Estado da verificação

**Sete de sete notebooks executados com sucesso em kernels novos**, incluindo 51 células de código dos arquivos, os `%run` internos, Grid Search e Random Search. Importações, caminhos e variáveis funcionaram no ambiente local. Não foi necessário alterar nenhum modelo.

Ambiente: **Python 3.12.8, 64 bits**; JupyterLab 4.6.6, Jupyter 1.1.1, ipykernel 7.4.0, pandas 3.1.1, NumPy 2.5.5, Matplotlib 3.11.2, scikit-learn 1.9.1, imbalanced-learn 0.14.2 e SciPy 1.18.1. `pip check`: **No broken requirements found**. As versões completas estão em `requirements-aula.txt`.

| Notebook | Estado | Duração da primeira verificação |
|---|---|---:|
| `dataset/df_adaptado.ipynb` | OK, exportação segura | 9,91 s |
| `01_analise_exploratoria.ipynb` | OK | 3,03 s |
| `02_analise_valores_nulos.ipynb` | OK | 2,63 s |
| `06_pre-processamento.ipynb` | OK, avisos de depreciação | 24,23 s |
| `07_divisao_e_balanceamento.ipynb` | OK | 9,68 s |
| `09_decision_tree.ipynb` | OK, incluindo buscas e CV | 36,80 s |
| `10_random_forest.ipynb` | OK, 400 árvores | 16,68 s |

Tempo total desta primeira execução: aproximadamente **1 min 43 s**; instalação e preparação do ambiente são etapas separadas. As durações podem variar na aula. Evidência: `auditoria/execucao.json`.

Resultados reais do teste; precisão, recall e F1 abaixo sempre se referem à classe **SIM=1**:

| Estimador existente | Acurácia | Precisão SIM | Recall SIM | F1 SIM | MCC no teste |
|---|---:|---:|---:|---:|---:|
| Árvore inicial | 88,36% | 62,82% | 55,68% | 59,04% | 0,524076 |
| Árvore ajustada | 89,04% | 64,40% | 60,98% | 62,65% | 0,562588 |
| Random Forest | 98,80% | 100,00% | 22,22% | 36,36% | 0,468561 |

Matrizes: linhas = classe real, colunas = predita, ordem **[NAO, SIM]**:

- Árvore inicial: `[[1401, 87], [117, 147]]`.
- Árvore ajustada: `[[1399, 89], [103, 161]]`.
- Random Forest: `[[1725, 0], [21, 6]]`.

As tabelas manuais antigas da árvore chamam o acerto de 1.401 registros NAO de “verdadeiro positivo”. Para a avaliação de chuva usada pelo `scoring='f1'`, o positivo é SIM; nesse caso a árvore inicial tem **147 verdadeiros positivos**. Use a ordem das classes exibida na matriz e a tabela calculada acima para evitar inverter a interpretação.

**Não usar a acurácia para declarar a floresta superior.** A árvore tem 264 casos SIM no teste aleatório; a floresta tem somente 27 no teste cronológico e encontra 6 deles, deixando 21 sem detecção. Seus conjuntos de teste são diferentes. As métricas numéricas não arredondadas e os parâmetros completos estão nos JSONs de auditoria.

Avisos observados: Pandas anuncia futura remoção de `inplace` no notebook 06, sem impedir a execução; nbformat completou IDs ausentes de células do notebook 10. O Windows/ZeroMQ emite avisos de inicialização, sem falha dos kernels. Joblib/Loky emite `KeyError` no processo auxiliar de limpeza de temporários após as buscas. A árvore foi reexecutada com diretório temporário explícito: concluiu novamente, com os mesmos resultados, mas a mensagem de limpeza persistiu. **Essa pendência de biblioteca permanece**, sem bloquear as células ou o kernel. Evidências: `auditoria/reexecucao_arvore.stderr.log` e `auditoria/execucao_arvore_temp_local.json`.

## Ordem de apresentação e dependências

1. `notebooks/01_analise_exploratoria.ipynb`: dimensões, tipos, distribuição do alvo e estatísticas da base adaptada.
2. `notebooks/02_analise_valores_nulos.ipynb`: nulos e duplicados da base adaptada.
3. `notebooks/06_pre-processamento.ipynb`: estação, remoção de colunas, média da radiação, remoção de linhas nulas, LabelEncoder e MinMaxScaler; exporta uma cópia em `artefatos/datasets`.
4. `notebooks/07_divisao_e_balanceamento.ipynb`: lê o CSV processado fornecido em `dataset/`, divide treino/teste e produz também um treino balanceado.
5. `notebooks/09_decision_tree.ipynb`: executa o notebook 07 via `%run`; treina e avalia árvores, validação cruzada, Grid Search e Random Search. Não depende de variáveis de outro kernel.
6. `notebooks/10_random_forest.ipynb`: fluxo independente; lê a base adaptada, divide cronologicamente, prepara, treina e avalia a floresta.

Opcional, antes das análises: `dataset/df_adaptado.ipynb` documenta a transformação da base bruta em adaptada. Não é pré-requisito, pois o CSV adaptado já está no repositório. Na versão local, gera sua cópia em `artefatos/datasets`.

Os notebooks devem rodar com diretório de trabalho igual à pasta em que estão (`notebooks/` ou `dataset/`). O Jupyter aberto na raiz e os notebooks abertos pelo navegador usam essa organização; o verificador também a define explicitamente. Não rode `%run notebooks/09_decision_tree.ipynb` de um kernel na raiz: seus caminhos relativos pressupõem a pasta `notebooks/`.

Os CSVs originais, adaptados e processados fornecidos permanecem como entradas. As cópias regeneradas são verificadas separadamente, sem substituir os arquivos versionados. Não há notebooks 03, 04, 05 ou 08 nesta versão; os saltos na numeração não indicam arquivos locais ausentes.

## Estrutura completa relevante

| Item | Papel |
|---|---|
| `README.md` | Contexto, objetivos, origem INMET, descrição das bases e link de planejamento Trello. |
| `dataset/*.CSV` | Base bruta, adaptada e processada fornecidas pelo grupo; preservadas. |
| `dataset/df_adaptado.ipynb` | Criação do alvo categórico a partir da precipitação. |
| `notebooks/*.ipynb` | Seis notebooks de análise, tratamento e dois tipos de modelo. |
| `pyproject.toml` | Python >=3.11, dependências e backend uv_build. |
| `.python-version` | Sugere Python 3.11; ambiente local usa 3.12.8 compatível com pyproject. |
| `uv.lock` | Lockfile original preservado; ambiente de hoje instalado com pip a partir de pyproject. |
| `src/analise_precipitacao_caruaru/__init__.py` | Apenas função de exemplo `Hello from...`; não contém treinamento. |
| `.venv/` | Ambiente isolado de 64 bits. |
| `requirements-aula.txt` | Versões efetivamente instaladas para reproduzir este ambiente. |
| `verificar_notebooks.py` | Execução de todos os notebooks em kernels novos, hashes e auditoria dos modelos existentes. |
| `artefatos/html/` | Cópias HTML da execução, úteis como alternativa sem kernel. |
| `artefatos/datasets/` | Exportações regeneradas, sem sobrescrever as bases fornecidas. |
| `auditoria/` | Logs, métricas calculadas, verificações dos datasets e hashes antes/depois. |
| `.jupyter-local/` | Informações locais do servidor e URL de acesso. |

O quadro externo do Trello não foi usado como evidência de implementação; esta auditoria considera o conteúdo clonado do repositório.

## Dados confirmados nesta máquina

- Estação A341, Caruaru/PE, registros horários de 01/01/2025 a 31/12/2025.
- Base original e adaptada: 8.760 linhas × 20 colunas cada. Base processada: 8.756 linhas × 18 colunas, sendo 17 atributos e o alvo.
- Adaptada: 7.440 NAO e 1.320 SIM (15,07% de chuva). Processada: 7.436 NAO e 1.320 SIM.
- Zero linhas duplicadas na adaptada; radiação com 3.286 nulos; coluna `Unnamed: 19` inteira vazia; demais medições meteorológicas com quatro nulos por coluna. Processada sem nulos.
- Quatro precipitações ausentes são convertidas em NAO pela regra original; essas linhas são retiradas na preparação da árvore, mas permanecem no fluxo independente da Random Forest, que imputa os preditores. Rever a validade do rótulo nessas quatro linhas.
- Tamanho somado dos três CSVs: 4.542.066 bytes (aproximadamente 4,54 MB). Não é uma base de grande volume nesta versão.
- Os CSVs adaptado e processado regenerados foram comparados aos fornecidos com tolerância numérica de `1e-12`: conteúdo equivalente. Os leitores permanecem usando as bases fornecidas em `dataset/`.
- Evidência detalhada: `auditoria/datasets.json`; hashes e comparação direta com o ZIP em `auditoria/preservacao.json`.

## Modelos, hiperparâmetros e avaliação

Existem **dois tipos de modelos**, ambos já presentes no repositório. Nenhum novo modelo foi implementado nesta preparação.

### Decision Tree — notebook 09

- Treino inicial: `DecisionTreeClassifier(criterion='gini', max_depth=5, min_samples_split=10, random_state=42)`; demais parâmetros padrão da versão instalada.
- Treino ajustado: `DecisionTreeClassifier(criterion='entropy', max_depth=9, min_samples_leaf=3, random_state=42)`; `min_samples_split` volta ao padrão 2.
- Uma terceira instanciação da mesma classe, `DecisionTreeClassifier(random_state=42)`, é usada somente na validação cruzada de F1, sem os limites da árvore inicial.
- Divisão: `train_test_split(test_size=0.2, random_state=42, stratify=y)`, embaralhamento padrão. `CHUVA`: NAO=0, SIM=1.
- Balanceamento disponível: `RandomUnderSampler(random_state=42)`, aplicado somente ao treino. **As árvores e as buscas usam `X_train, y_train`, e não `X_train_bal, y_train_bal`.** Portanto o resultado atual da árvore é sem undersampling.
- Métricas do código: acurácia no teste, matriz de confusão, MCC médio em 5 folds para a árvore inicial e ajustada, F1 médio/desvio em 5 folds para a árvore de parâmetros padrão. Precisão, recall e F1 escritos em Markdown são cálculos manuais históricos e devem ser conferidos contra a execução.
- `cv=5` para classificação: StratifiedKFold de cinco partes, sem shuffle por padrão. Não é validação temporal. F1 usa classe positiva 1 (chuva).
- Grid Search: `max_depth=[2,3,4,5,6,None]`, `criterion=['gini','entropy']`, `min_samples_leaf=[1,5,10]`; 36 combinações × 5 folds = 180 ajustes, mais refit. Estimador base com `random_state=42`, `scoring='f1'`, `n_jobs=-1`.
- Random Search: `max_depth=randint(2,15)` (2 a 14), `criterion=['gini','entropy']`, `min_samples_leaf=randint(1,20)` (1 a 19); `n_iter=15`, `cv=5`, `random_state=42`, `scoring='f1'`, `n_jobs=-1`; 75 ajustes, mais refit.
- `grid.score(...)` e `busca.score(...)` são **F1**, pois seguem `scoring='f1'`; não são acurácia.
- A árvore final tem parâmetros escritos manualmente no código; não é automaticamente substituída por `best_estimator_` de cada nova busca.

Valores de validação cruzada reproduzidos:

| Avaliação | Resultado |
|---|---:|
| MCC médio, árvore inicial, 5 folds | 0,527493 |
| MCC médio, árvore ajustada, 5 folds | 0,546698 |
| F1 médio, árvore padrão, 5 folds | 0,568927 |
| Desvio do F1, árvore padrão, 5 folds | 0,027811 |

MCC de validação cruzada e MCC no teste são medidas obtidas em divisões diferentes; não intercambiar os valores.

| Busca | Melhores parâmetros | F1 médio CV | F1 teste |
|---|---|---:|---:|
| Grid | entropy; profundidade 6; mínimo folha 10 | 0,630283 | 0,582996 |
| Random | entropy; profundidade 9; mínimo folha 3 | 0,614117 | 0,626459 |

O Grid teve maior F1 de validação; o Random teve maior F1 no teste. Isso explica a aparente contradição com o texto histórico. A escolha metodológica deve ser discutida com o professor.

### Random Forest — notebook 10

- `RandomForestClassifier(n_estimators=400, class_weight='balanced_subsample', random_state=42, n_jobs=-1)`; demais parâmetros padrão. O texto final do notebook menciona 300 árvores, mas **o código efetivamente treina 400**. O texto original foi preservado.
- Ordenação por data/hora; primeiros 80% para treino e últimos 20% para teste; sem embaralhar.
- Variáveis: medições meteorológicas numéricas mais mês/hora; removidos data textual, hora textual, timestamp e alvos. Seleção numérica por `ColumnTransformer`.
- `SimpleImputer(strategy='median', add_indicator=True)` dentro de `Pipeline`, ajustado somente no treino. Sem normalização.
- `balanced_subsample` pondera as classes a cada amostra bootstrap, sem remover registros.
- Métricas implementadas: acurácia, precisão/recall/F1 de chuva, classification_report, matriz de confusão e importância de variáveis. Não há CV, Grid Search ou Random Search para Random Forest neste repositório.

Os parâmetros completos dos estimadores ajustados e as métricas adicionais calculadas pela auditoria ficam em `auditoria/decision_tree_inicial.json`, `auditoria/decision_tree_ajustada.json` e `auditoria/random_forest.json`.

## Decisões metodológicas e pendências para discutir

1. **Alvo:** precipitação horária >0 mm gera SIM; zero gera NAO. A comparação `NaN > 0` também resulta em falso e pode classificar ausências como NAO. Conferir quantidades na auditoria de dados.
2. **Pré-processamento da árvore:** média e MinMaxScaler ajustados na base inteira antes da divisão. Isso permite informação do teste influenciar o tratamento; o ideal futuro é ajustar essas transformações somente no treino e dentro dos folds. A lógica foi preservada.
3. **Teste e sazonalidade:** a árvore usa teste aleatório e a floresta teste cronológico. Períodos e proporções de chuva diferem; não apresentar a diferença de acurácia como prova de superioridade de um algoritmo.
4. **Seleção de busca:** a afirmação histórica de que Random Search foi melhor precisa distinguir F1 de validação e de teste. Escolher repetidamente pelo resultado no teste compromete sua independência; preferir seleção por CV e avaliação final única em um estudo posterior.
5. **Significado do problema:** classificação de ocorrência no mesmo horário; as medições do horário não demonstram previsão de chuva futura. Para isso seriam necessários horizonte e variáveis defasadas, não implementados aqui.
6. **Desbalanceamento:** acurácia alta pode esconder baixa detecção de chuva. Apresentar recall/F1 de SIM, matriz e suporte das classes. O treino balanceado criado no 07 ainda não é utilizado no 09.
   Na divisão da árvore, são 7.004 registros de treino e 1.752 de teste; undersampling gera 2.112 registros (1.056 por classe), que atualmente não alimentam o modelo. Na floresta, são 7.008 no treino (até 19/10/2025 23h UTC) e 1.752 no teste (20/10 a 31/12/2025), com 1.293 e 27 casos de chuva, respectivamente.
7. **Qualidade de sensores:** sensores automáticos não garantem ausência de falhas, outliers ou inconsistências. A justificativa histórica do notebook 06 precisa ser revista; não foi alterado o tratamento nesta preparação.
8. **Radiação:** investigar por que há tantas ausências e sua relação com noite/sensor antes de assumir que média global é adequada.
9. **Estação:** o código cria `ESTACAO`, embora parte do texto fale em meses. O mapeamento de meses é manual e a codificação por LabelEncoder seguida de MinMaxScaler cria ordem artificial. Validar o critério sazonal antes de generalizar.
10. **Escopo de Big Data:** o repositório usa pandas e scikit-learn localmente; não implementa Spark, Hadoop ou processamento distribuído. Apresentar o volume real e o estágio acadêmico do trabalho, sem afirmar escala distribuída já implementada.

Estas são pendências metodológicas registradas, não alterações realizadas. Não houve novos modelos nem mudança de hiperparâmetros, amostragem ou critérios de avaliação.

## Comandos de ambiente e reprodução

Não é preciso ativar o ambiente para usar os comandos abaixo. Isso evita depender da política de execução de `Activate.ps1`.

```powershell
# Ambiente já criado; comandos abaixo documentam como recriar.
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-aula.txt
.\.venv\Scripts\python.exe -m pip install -e . --no-deps
.\.venv\Scripts\python.exe -m ipykernel install --prefix .venv --name caruaru-venv --display-name "Python 3.12 (.venv Caruaru)"
.\.venv\Scripts\python.exe -m pip check

# Reexecuta os sete notebooks, atualiza saídas e gera evidências/HTML.
.\.venv\Scripts\python.exe verificar_notebooks.py

# Alternativa: Jupyter no terminal, com URL autenticada exibida no console.
.\.venv\Scripts\python.exe -m jupyterlab --ServerApp.ip=127.0.0.1 --ServerApp.port=8888
```

Se a política do PowerShell bloquear scripts, use o inicializador `.cmd` ou os comandos diretos de Python. Para verificar o interpretador em uma célula: `import sys; print(sys.executable)`; ele deve terminar em `analise-precipitacao-caruaru\.venv\Scripts\python.exe`.

## Preservação e alterações locais

- `main` e `origin/main` foram obtidas do commit `a0d8d83dd5070ae3708f6c2ca3dfa2f6e10f7851`, confirmado com `git ls-remote` em 16/11/2026.
- Trabalho local na branch `preparacao-aula-2026-11-16`; sem push e sem modificação remota.
- As alterações de preparação foram registradas em commit exclusivamente local nessa branch; `main` continua no commit original.
- Originais completos, incluindo notebooks com saídas anteriores, preservados em `..\analise-precipitacao-caruaru-original-a0d8d83.zip`.
- Sete notebooks: metadados de kernel apontados para o ambiente local e saídas atualizadas pela execução real, sem alterar o código dos modelos ou o texto histórico. O nbformat também adicionou IDs a células do notebook 10 que não os tinham.
- `dataset/df_adaptado.ipynb`: apenas exportação redirecionada para `artefatos/datasets`, para não sobrescrever o CSV adaptado original.
- `notebooks/06_pre-processamento.ipynb`: apenas exportação redirecionada para `artefatos/datasets`, explicitando o destino e evitando CSV solto em `notebooks/`.
- `.gitignore`: exclusão do ambiente, caches, exportações, evidências e dados locais do servidor.
- Acrescentados este guia, versões instaladas, inicializadores e verificador. `pyproject.toml`, `uv.lock`, README e código dos modelos preservados.
- Os hashes dos três CSVs são comparados antes/depois de cada notebook; arquivos de evidência: `auditoria/hashes_dataset_antes.json` e `auditoria/hashes_dataset_depois.json`.

## Roteiro de cinco minutos para a aula

1. Mostre objetivo, fonte INMET e classes do notebook 01.
2. Explique nulos e transformações no 02/06.
3. Mostre divisão e a observação de que undersampling ainda não entra no treino da árvore.
4. Abra a árvore já executada, mostre matriz, F1/MCC e buscas.
5. Abra Random Forest, explique teste cronológico, métricas da classe SIM e limitações. Finalize com próximas decisões metodológicas, sem prometer previsão futura ou comparação direta de algoritmos.

Se faltar tempo para reexecutar buscas durante a aula, use os notebooks com saídas verificadas ou os arquivos de `artefatos/html/`.
