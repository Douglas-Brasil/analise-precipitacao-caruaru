# 🌧️ Análise de Chuva em Caruaru — INMET

Projeto de análise de dados meteorológicos com foco na precipitação pluviométrica em **Caruaru, Pernambuco**, utilizando dados disponibilizados pelo Instituto Nacional de Meteorologia (INMET), referentes ao período de 1º de janeiro a 31 de dezembro de 2025.

O projeto envolve exploração, preparação e pré-processamento de dados meteorológicos, visando à análise de índices de chuva e à aplicação de modelos de Inteligência Artificial (IA).

## 🎯 Objetivos

- Explorar e analisar os dados meteorológicos de Caruaru.
- Realizar o tratamento e o pré-processamento da base de dados.
- Transformar a variável numérica de precipitação em uma variável categórica para classificação da ocorrência de chuva.
- Investigar padrões e características relacionados à precipitação.
- Preparar os dados para a aplicação de modelos de Inteligência Artificial.
- Documentar e organizar as atividades desenvolvidas ao longo do projeto.

## 📂 Estrutura do projeto

```text
.
├── dataset/
│   ├── INMET_NE_PE_A341_CARUARU_01-01-2025_A_31-12-2025
│   ├── INMET_NE_PE_A341_CARUARU_01-01-2025_A_31-12-2025_ADAPTADO
│   └── INMET_NE_PE_A341_CARUARU_01-01-2025_A_31-12-2025_PROCESSADA
│
├── notebooks/
│   └── Arquivos Jupyter Notebook (.ipynb)
│
└── README.md
```

## 🗃️ Base de dados

Os arquivos presentes no diretório `dataset/` representam diferentes etapas de preparação dos dados.

| Arquivo | Descrição |
|---|---|
| `INMET_NE_PE_A341_CARUARU_01-01-2025_A_31-12-2025` | **Base original:** dados meteorológicos obtidos do INMET, preservando os dados de origem. |
| `INMET_NE_PE_A341_CARUARU_01-01-2025_A_31-12-2025_ADAPTADO` | **Base adaptada:** substituição da coluna numérica de precipitação por uma variável categórica denominada `CHUVA`, com os valores `SIM` ou `NAO`. |
| `INMET_NE_PE_A341_CARUARU_01-01-2025_A_31-12-2025_PROCESSADA` | **Base processada:** dados após a realização das etapas de pré-processamento, preparados para a aplicação dos modelos de IA. |

Os nomes acima representam os nomes-base dos arquivos; suas extensões podem variar conforme o formato utilizado.

### 🌧️ Variável `CHUVA`

Na base adaptada, a variável categórica `CHUVA` representa a ocorrência de chuva, substituindo a variável numérica original de precipitação.

- `SIM`: ocorrência de chuva, conforme o critério definido no pré-processamento.
- `NAO`: ausência de chuva, conforme o critério definido no pré-processamento.

**Observação:** o critério exato utilizado para classificar a ocorrência de chuva deve ser consultado nos notebooks do projeto. A definição é importante para garantir consistência nas análises e no treinamento dos modelos.

## 📓 Notebooks

O diretório `notebooks/` reúne os arquivos Jupyter Notebook utilizados no desenvolvimento do projeto.

Os notebooks documentam as análises, as transformações dos dados e as demais atividades executadas durante o trabalho.

Consulte os notebooks para acompanhar a sequência das etapas, verificar as decisões de tratamento dos dados e reproduzir as análises realizadas.

## 📋 Planejamento e atividades

As tarefas, instruções e atividades previstas para o desenvolvimento do projeto estão organizadas no Trello.

🔗 **[Acessar o quadro do Trello — Índices de Chuva Caruaru](https://trello.com/invite/b/6adf80a8f8b0d97f467325a2/ATTI01fb22815ff8c7ac21aeeed1b40fb99e0645FE90/indices-de-chuva-caruaru)**

O quadro deve ser utilizado como referência para acompanhar as atividades planejadas, as etapas em andamento e as tarefas concluídas.

## ⚙️ Tecnologias e ferramentas

- **Python:** linguagem de programação utilizada para manipulação e análise dos dados.
- **Jupyter Notebook:** ambiente interativo para desenvolvimento e documentação das análises.
- **INMET:** fonte dos dados meteorológicos.
- **Inteligência Artificial:** aplicação de modelos sobre os dados após as etapas de preparação.

Bibliotecas Python adicionais devem ser documentadas conforme forem utilizadas nos notebooks, como pandas, NumPy, Matplotlib e scikit-learn, caso façam parte do projeto.

Abra o notebook desejado dentro do diretório `notebooks/` e execute as células na ordem apresentada.


## 📚 Fonte dos dados

**Instituto Nacional de Meteorologia (INMET)**

Os dados utilizados correspondem à estação meteorológica A341, localizada em Caruaru, Pernambuco, no período de 01/01/2025 a 31/12/2025.

- [Portal oficial do INMET](https://portal.inmet.gov.br/)
- [Dados meteorológicos históricos do INMET](https://portal.inmet.gov.br/dadoshistoricos)

---

*Projeto desenvolvido para análise de dados meteorológicos e investigação de padrões de precipitação em Caruaru — PE.*
