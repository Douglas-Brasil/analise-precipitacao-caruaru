# Como executar no Windows e no VS Code

## 1. Qual pasta devo abrir hoje?

O projeto preparado está em:

```text
C:\Users\sergiobfj\Documents\dev\estudos\faculdade\analise-precipitacao-caruaru
```

No VS Code, use **Arquivo → Abrir Pasta** e selecione essa pasta. O ambiente já foi criado nesta máquina. Para a aula de hoje, vá direto à seleção do kernel no passo 6.

As mudanças desta aula estão consolidadas na branch `main` do repositório no GitHub. Um novo clone obtém os notebooks, os guias e as saídas executadas desta versão.

## 2. Como clonar o projeto?

Instale o [Git para Windows](https://git-scm.com/downloads/win) se o comando `git` ainda não existir. Abra um terminal PowerShell na pasta onde guarda os projetos:

```powershell
git clone https://github.com/Douglas-Brasil/analise-precipitacao-caruaru.git
cd analise-precipitacao-caruaru
```

Isso obtém a versão publicada na `main`. Se já tiver um clone, com as alterações locais salvas em commit e a árvore de trabalho limpa, atualize-o:

```powershell
git switch main
git pull --ff-only origin main
```

Se o Git informar que os históricos divergiram, integre as contribuições antes de atualizar; não use force push. A `.venv` não é copiada pelo Git; crie outra nos próximos passos.

## 3. Como instalar o Python?

Use **Python 3.12 de 64 bits**. O ambiente validado nesta máquina usa 3.12.8. Baixe um instalador compatível na [página oficial de versões para Windows](https://www.python.org/downloads/windows/), escolha **Windows installer (64-bit)** e habilite o launcher `py` e a opção de adicionar Python ao PATH, quando oferecida pelo instalador.

Feche e reabra o terminal depois da instalação. Confira:

```powershell
py --list-paths
py -3.12 --version
py -3.12 -c "import struct; print(struct.calcsize('P') * 8)"
```

O último comando deve mostrar `64`. Nesta máquina também existe um Python 3.14 de 32 bits; por isso usamos explicitamente `py -3.12` para criar o ambiente.

## 4. Como criar e ativar o ambiente virtual?

Abra o terminal **na raiz do projeto**, onde estão `README.md`, `dataset/` e `notebooks/`:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
python -c "import sys; print(sys.executable)"
```

O caminho exibido deve terminar em `.venv\Scripts\python.exe`. O prefixo `(.venv)` costuma aparecer no terminal. Para sair do ambiente, use `deactivate`.

Se o PowerShell bloquear o script de ativação, libere apenas o terminal atual e tente novamente:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

A ativação é opcional: os comandos abaixo usam o caminho completo do Python do ambiente.

## 5. Como instalar as dependências?

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pip check
```

O `pyproject.toml` instala Pandas, NumPy, Matplotlib, scikit-learn, imbalanced-learn, Jupyter e ipykernel; SciPy vem como dependência e é usado pela Decision Tree. O resultado esperado de `pip check` é `No broken requirements found`.

Para repetir as versões usadas na preparação local, se `requirements-aula.txt` estiver disponível:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-aula.txt
.\.venv\Scripts\python.exe -m pip install -e . --no-deps
```

Registre o kernel local:

```powershell
.\.venv\Scripts\python.exe -m ipykernel install --prefix .venv --name caruaru-venv --display-name "Python 3.12 (.venv Caruaru)"
```

Não é necessário instalar novos pacotes para executar as buscas e métricas acrescentadas à Random Forest.

## 6. Quais extensões e qual kernel usar no VS Code?

Instale as extensões oficiais da Microsoft **Python** (`ms-python.python`) e **Jupyter** (`ms-toolsai.jupyter`) na aba de extensões (`Ctrl+Shift+X`). Se o comando `code` estiver disponível, também pode usar:

```powershell
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code .
```

Abra um arquivo `.ipynb`. No canto superior direito, clique em **Selecionar Kernel / Select Kernel**. Escolha **Python 3.12 (.venv Caruaru)** ou o ambiente Python com caminho `.venv\Scripts\python.exe`. Se precisar, use **Select Another Kernel → Python Environments** e procure a `.venv`.

O interpretador do terminal e o kernel do notebook são escolhas separadas: ativar a `.venv` no terminal não garante que o notebook esteja usando o mesmo Python. Essa seleção segue a [documentação de kernels do VS Code](https://code.visualstudio.com/docs/datascience/jupyter-kernel-management).

## 7. Como abrir e em qual ordem executar?

Abra os notebooks pelo explorador do VS Code. A numeração tem saltos; não faltam arquivos para a execução desta versão.

| Ordem | Notebook | O que demonstra |
|---:|---|---|
| Opcional | `dataset/df_adaptado.ipynb` | Criação da classe CHUVA a partir da precipitação. |
| 1 | `notebooks/01_analise_exploratoria.ipynb` | Estrutura, estatísticas e distribuição das classes. |
| 2 | `notebooks/02_analise_valores_nulos.ipynb` | Nulos e duplicados. |
| 3 | `notebooks/06_pre-processamento.ipynb` | Preparação da base usada pela árvore. |
| 4 | `notebooks/07_divisao_e_balanceamento.ipynb` | Divisão aleatória e treino balanceado disponível. |
| 5 | `notebooks/09_decision_tree.ipynb` | Decision Tree, métricas, validação e buscas já existentes. |
| 6 | `notebooks/10_random_forest.ipynb` | Fluxo completo e independente da Random Forest. |

Para demonstrar **somente a Random Forest**, basta abrir o notebook 10 e executá-lo do início ao fim. Ele lê a base adaptada fornecida em `dataset/`; não precisa que os demais notebooks tenham sido executados.

O notebook 09 usa `%run 07_divisao_e_balanceamento.ipynb`, portanto recria suas próprias variáveis. Não depende de outro notebook aberto no mesmo kernel.

As exportações dos notebooks de preparação vão para `artefatos/datasets`, preservando os CSVs fornecidos. Os leitores continuam usando os arquivos versionados em `dataset/`.

## 8. Como executar uma célula ou todas as células?

- Clique na célula e use o botão triangular à esquerda para executar apenas ela.
- `Shift+Enter` executa a célula e avança para a próxima.
- Use **Run All / Executar Tudo** no topo para executar todas em ordem.
- Para uma demonstração limpa, use **Restart Kernel / Reiniciar Kernel** e depois **Run All**.
- Aguarde o fim da execução; um `[*]` ou indicador girando significa que a célula ainda está trabalhando.
- Não execute apenas a célula de avaliação antes de ler os dados e treinar os modelos.

Tabelas, textos e gráficos aparecem logo abaixo de cada célula. As saídas reais da última execução já estão salvas no notebook 10: é possível apresentá-las sem treinar novamente. Salve com `Ctrl+S` para guardar as novas saídas após uma execução. Os comandos de células seguem a [documentação de notebooks do VS Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks).

## 9. Como executar no navegador, se necessário?

Na pasta atual, abra `ABRIR_JUPYTER.cmd` pelo Explorador de Arquivos do Windows ou use:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\iniciar_jupyter.ps1
```

O script abre uma URL autenticada do JupyterLab local. Alternativa pelo terminal:

```powershell
.\.venv\Scripts\python.exe -m jupyterlab --ServerApp.ip=127.0.0.1 --ServerApp.port=8888
```

Abra a URL exibida e escolha o mesmo kernel. Se a porta estiver ocupada, o Jupyter pode escolher outra. Para encerrar o servidor iniciado no terminal, use `Ctrl+C` e confirme quando solicitado. Não é necessário criar uma interface para usar os notebooks.

## 10. Como resolver os erros mais comuns?

| Problema | O que fazer |
|---|---|
| `py` não é reconhecido | Reabra o terminal após instalar Python; confira se o launcher foi instalado. |
| `py -3.12` não encontra Python | Instale uma versão 3.12 de 64 bits e confira `py --list-paths`. |
| `.venv` não aparece no explorador | Ela foi ocultada por `files.exclude`; continua existindo e funcionando. |
| `ModuleNotFoundError` para pandas, sklearn ou imblearn | Selecione o kernel da `.venv` e execute o comando de instalação do passo 5. O pacote de `sklearn` chama-se `scikit-learn`; o de `imblearn` chama-se `imbalanced-learn`. |
| Biblioteca foi instalada, mas o notebook não encontra | Confira `sys.executable` na célula; reinicie o kernel correto após instalar. |
| Kernel não aparece | Refaça o registro do passo 5 e use **Developer: Reload Window** na paleta do VS Code. |
| `NameError` para X_train, y_pred, grid ou busca | Execute as células anteriores em ordem ou reinicie e use Run All. |
| `FileNotFoundError` ao ler CSV | Confira se a pasta `dataset/` está ao lado de `notebooks/` e mantenha os nomes/extensões originais. |
| `%run` não encontra o notebook 07 | Execute o notebook 09 com diretório de trabalho em `notebooks/`. |
| Busca está demorando | Aguarde: o notebook mostra o início e o fim de cada etapa. As duas buscas da floresta fazem 20 ajustes cada, mais refit; não aumente o espaço durante a aula. |
| Avisos de depreciação no notebook 06 | São avisos do Pandas; a versão instalada executa o código existente. Não alteramos a Decision Tree nesta etapa. |
| Mensagens de limpeza do Joblib na árvore | Foram observadas na versão anterior; os cálculos terminaram. A floresta usa buscas sequenciais e paralelismo nas próprias árvores. |
| Arquivo mudou no disco enquanto estava aberto | Salve ou recarregue conscientemente; para ver esta preparação, reabra o notebook salvo no projeto. |

Para conferir o Python e os caminhos em uma célula:

```python
import sys # mostra qual python o kernel utiliza
import os # permite conferir a pasta de trabalho
print(sys.executable) # deve apontar para o python da venv
print(os.getcwd()) # deve apontar para a pasta notebooks neste fluxo
```

Se a pasta de trabalho estiver errada, ajuste-a antes das leituras, substituindo o caminho se estiver em outra máquina:

```python
os.chdir(r'C:\Users\sergiobfj\Documents\dev\estudos\faculdade\analise-precipitacao-caruaru\notebooks') # usa a pasta esperada pelos caminhos relativos
```

## 11. O que está oculto no explorador?

O VS Code exibe `dataset/`, `notebooks/`, `README.md`, `GUIA_RAPIDO.md` e este tutorial. Ambiente, caches, scripts e artefatos continuam no disco. A ocultação é apenas visual e não muda importações, leitura de dados ou treinamento.

Para estudar os conceitos e interpretar os resultados, consulte [GUIA_RAPIDO.md](GUIA_RAPIDO.md).
