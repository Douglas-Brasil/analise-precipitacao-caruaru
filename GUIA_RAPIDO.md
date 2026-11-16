# Guia de estudo — chuva em Caruaru

Perguntas e respostas para conversar com o professor. Referência: **aula 08, MSc. Flávio Morais**: métricas nas páginas 6–31, hiperparâmetros e buscas nas 33–63 e Random Forest nas 74–85.

**O que está pronto?** Temos Decision Tree e Random Forest executadas, com saídas salvas. A floresta tem validação temporal, duas buscas pequenas e comparação inicial/ajustada. Nesta etapa, a árvore recebeu correções de apresentação e interpretação, mantendo seus treinos e hiperparâmetros.

**Como executar?** Consulte [COMO_EXECUTAR.md](COMO_EXECUTAR.md). Na aula, abra os notebooks 09 e 10; as tabelas e os gráficos já estão salvos.

## Sobre o projeto

**Qual é o objetivo do projeto?** Classificar se ocorreu chuva em cada registro horário da estação meteorológica de Caruaru, usando as condições meteorológicas medidas.

**Qual é a origem da base?** INMET, estação A341, Caruaru/PE, de 01/01/2025 a 31/12/2025. A origem e o período estão documentados no README e no cabeçalho do CSV original.

**Quantos registros e atributos temos?** A base bruta e a adaptada têm 8.760 linhas e 20 colunas cada. A processada da árvore tem 8.756 linhas, 17 atributos e 1 alvo. A floresta usa 8.760 linhas e 18 atributos antes dos indicadores de ausência.

**O que cada registro representa?** Uma observação de uma hora, com data e hora UTC. Não representa um dia nem uma estação meteorológica diferente.

**Qual é a variável-alvo?** `CHUVA`: SIM ou NAO. Nos modelos, SIM=1 é a classe positiva e NAO=0 é a negativa. A floresta chama sua versão numérica de `CHUVA_BINARIA`.

**O que são features e target?** Features são os atributos de entrada, como umidade e temperatura. Target é a resposta que o modelo tenta classificar: ocorrência de chuva.

**Por que modificamos a coluna de precipitação?** Transformamos o valor numérico em uma resposta categórica: precipitação acima de zero vira SIM; os demais casos viram NAO. Isso adapta a base ao problema de classificação escolhido pelo grupo.

**Por que classificação, e não regressão?** Queremos saber a classe de ocorrência, não estimar quantos milímetros choveram. Prever uma quantidade numérica seria outro problema.

**Por que aprendizado supervisionado?** O treino já contém exemplos de atributos acompanhados da resposta conhecida, derivada da precipitação registrada.

**Estamos classificando ou prevendo chuvas futuras?** Classificamos a ocorrência no mesmo horário das medições. Separar o teste no tempo não transforma automaticamente o modelo em previsão futura.

**Isso já é processamento de Big Data distribuído?** Não. Os três CSVs somam cerca de 4,54 MB; usamos pandas e scikit-learn localmente. Não implementamos Spark ou Hadoop.

## Sobre os dados

**O que é análise exploratória?** É conhecer a base antes de treinar: tamanho, tipos, estatísticas, nulos e frequência das classes. Isso está nos notebooks 01 e 02.

**Quais atributos utilizamos?** As 16 medições meteorológicas: três de pressão, radiação, seis de temperatura/ponto de orvalho, três de umidade e três de vento. A árvore acrescenta estação do ano; a floresta acrescenta mês e hora.

**Quais atributos foram removidos e por quê?** A precipitação numérica foi retirada ao criar o alvo, evitando entregar a resposta ao modelo. Removemos `Unnamed: 19`, que era vazia. A árvore retira data e hora; a floresta extrai mês/hora e depois retira os textos, o timestamp e os próprios alvos das entradas.

**Mês e hora são irrelevantes para chuva?** Não podemos afirmar isso. Eles podem representar sazonalidade. A remoção da hora no fluxo da árvore foi uma decisão histórica; a floresta mantém mês e hora como atributos.

**Quais problemas encontramos na base?** Radiação com 3.286 nulos, uma coluna totalmente vazia e quatro ausências em cada uma das demais medições. Não encontramos linhas totalmente duplicadas na base adaptada.

**Como tratamos os nulos na árvore?** O notebook 06 preenche radiação pela média e remove as quatro linhas que ainda tinham ausências. Restam 8.756 registros sem nulos.

**Como tratamos os nulos na floresta?** Usamos mediana e indicadores de ausência dentro de um Pipeline. O preenchimento é aprendido apenas no treino de cada fold e depois aplicado à validação ou ao teste.

**Existe um problema na criação do alvo?** Sim: quatro precipitações ausentes também viraram NAO pela comparação original. A preparação da árvore remove essas linhas; a floresta conserva a base adaptada. Rever esses rótulos é uma pendência, sem alterar os CSVs originais nesta etapa.

**Como tratamos os outliers?** Não existe detecção ou correção específica implementada. O notebook 06 assume que sensores não geram outliers, mas essa justificativa não comprova a qualidade das medições. A revisão é uma pendência.

**O que é label encoding?** É trocar categorias por códigos numéricos. Na árvore, NAO vira 0 e SIM vira 1; as estações também recebem códigos.

**O que é MinMaxScaler?** É uma transformação que usa mínimo e máximo para ajustar os valores à faixa de zero a um. No notebook 06, ela também recebe o alvo já codificado em 0 e 1.

**Por que normalizamos os dados?** Foi uma decisão do pré-processamento existente. Árvores não exigem essa normalização para comparar limiares. A Random Forest não normaliza os atributos.

**O que é desbalanceamento de classes?** É ter muito mais exemplos de uma classe. Na adaptada, temos 7.440 NAO e 1.320 SIM: apenas 15,07% dos registros são de chuva.

**O que é random undersampling?** É sortear uma parte da classe mais comum para igualar sua quantidade à classe rara. O notebook 07 produz 2.112 registros de treino: 1.056 por classe.

**A Decision Tree usa esse treino balanceado?** Não. O notebook 07 o cria, mas a árvore e suas buscas continuam usando `X_train` e `y_train`, sem undersampling. Não corrigimos essa decisão nesta etapa de apresentação.

**Qual é a desvantagem do undersampling?** Ele descarta exemplos reais da classe mais comum e pode perder informação útil. Por isso deve ser avaliado, e não considerado automaticamente melhor.

**Qual é a diferença entre undersampling, oversampling e SMOTE?** Undersampling reduz a classe comum; oversampling aumenta a rara, por exemplo repetindo exemplos; SMOTE cria exemplos sintéticos entre vizinhos da classe rara. Oversampling e SMOTE não foram implementados aqui.

**Por que não balanceamos o teste?** Ele deve representar o período avaliado com sua distribuição real de classes. Alterar essa distribuição dificulta interpretar o desempenho esperado nesse período.

**Como a floresta lida com o desbalanceamento?** `class_weight='balanced_subsample'` aumenta o peso da classe rara em cada amostra bootstrap. Isso não remove linhas nem cria registros sintéticos.

**Como dividimos treino e teste?** A árvore usa divisão aleatória estratificada: 7.004 no treino e 1.752 no teste, com 264 chuvas no teste. A floresta usa ordem cronológica: 7.008 no treino e 1.752 no teste, com apenas 27 chuvas no teste.

**Qual é o período do teste da floresta?** De 20/10/2025, 00h UTC, a 31/12/2025, 23h UTC. O treino termina em 19/10/2025, 23h UTC, e contém 1.293 casos SIM.

**O que significa random_state=42?** É uma semente para repetir os sorteios. O número 42 não melhora o modelo; poderia ser outra semente fixa.

**O que é stratify?** Na divisão da árvore, `stratify=y` mantém proporções semelhantes das classes no treino e no teste. A floresta não estratifica, porque preserva a ordem temporal.

**O que é data leakage?** É deixar informação da validação ou do teste influenciar o aprendizado ou a escolha dos parâmetros. Isso pode deixar a avaliação otimista demais.

**Onde há risco de leakage neste projeto?** A árvore preenche e normaliza a base antes da divisão; suas transformações usam informação do conjunto inteiro. Na floresta, o Pipeline refaz o preenchimento em cada treino, evitando esse vazamento. A revisão da árvore continua pendente.

## Sobre inteligência artificial

**Como funciona a Decision Tree?** Ela aprende perguntas sobre os atributos e seus limites, dividindo os registros até chegar a folhas que indicam classes.

**Como funciona a Random Forest?** Combina várias árvores com amostras bootstrap e sorteios de atributos. De forma didática, elas votam; nesta implementação, a classe final vem da maior média de probabilidades das árvores, conforme a [documentação da biblioteca](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html).

**Qual é a diferença entre os dois algoritmos?** A árvore usa uma estrutura única e é mais fácil de interpretar. A floresta combina muitas estruturas, costuma ser mais estável e exige mais processamento.

**O que é ensemble learning?** É combinar vários estimadores em uma resposta. Nossa Random Forest é um ensemble de árvores; não implementamos outro algoritmo de ensemble nesta etapa.

**O que é bagging?** É treinar estimadores em amostras sorteadas e combinar suas respostas. As árvores podem aprender de forma independente.

**O que é bootstrap?** É sortear registros com reposição: um exemplo pode aparecer mais de uma vez e outro pode ficar de fora da amostra de uma árvore.

**Por que sortear atributos também?** Para diversificar as árvores. `max_features` controla quantos atributos podem disputar a melhor divisão em cada nó.

**O que é gini?** É uma medida da mistura de classes em um nó. Divisões melhores deixam os grupos mais puros.

**O que é entropy?** É outra medida da mistura ou incerteza das classes. Também ajuda a escolher divisões que separam melhor os exemplos.

**O que são parâmetros e hiperparâmetros?** Parâmetros são aprendidos no treino, como os limites das divisões. Hiperparâmetros são definidos antes do ajuste, como profundidade e quantidade de árvores.

**Quais hiperparâmetros usamos na árvore?** Inicial: gini, profundidade 5, mínimo de 10 registros para dividir um nó e semente 42. Ajustada: entropy, profundidade 9, mínimo de 3 registros por folha e semente 42; o mínimo para dividir volta ao padrão 2.

**Quais hiperparâmetros usamos na floresta inicial?** 400 árvores, pesos `balanced_subsample`, semente 42 e `n_jobs=-1`. Permanecem os padrões gini, profundidade sem limite, `max_features='sqrt'`, mínimo de 1 por folha e bootstrap ativado.

**Quais foram escolhidos para a floresta ajustada?** 100 árvores, profundidade sem limite e mínimo de 3 registros por folha. Atributos por divisão continuam em `sqrt`, com gini, pesos `balanced_subsample`, bootstrap e semente 42 mantidos.

**O que significa n_jobs=-1?** Usar os processadores disponíveis. Na floresta, as árvores trabalham em paralelo; as buscas usam `n_jobs=1` para evitar dois níveis de paralelismo e problemas de temporários no Windows.

**O que é overfitting?** É aprender detalhes demais do treino e perder desempenho em dados diferentes. Um resultado bom no treino, sozinho, não comprova qualidade.

**O que é underfitting?** É um modelo simples demais para capturar os padrões relevantes, com dificuldade até no treino.

**O que é generalização?** É conseguir classificar bem dados que não foram usados para aprender. Ela precisa ser avaliada em dados separados.

**O que é cross-validation?** É repetir ajustes e avaliações em divisões do treino para estimar o desempenho e comparar configurações sem usar o teste final.

**O que são folds?** São as partes usadas nessas avaliações. Na árvore, são cinco divisões estratificadas; na floresta, cinco períodos de validação em ordem temporal.

**Por que a floresta não usa simplesmente cv=5?** Para classificação, o inteiro 5 cria folds estratificados, que não garantem a ordem do tempo. Usamos `TimeSeriesSplit(n_splits=5, gap=24)`, coerente com o teste cronológico. O treino cresce e a validação sempre vem depois, como descrito no [TimeSeriesSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit).

**Por que deixar 24 horas entre treino e validação?** Para reduzir a proximidade imediata entre medições dos dois períodos. É uma decisão prática documentada, não uma garantia de independência nem um horizonte de previsão futura.

**Por que a média varia entre folds?** Cada período tem condições e proporções de chuva diferentes. Na floresta inicial, F1 médio de validação foi 50,93%, com desvio de 18,31 pontos percentuais; isso indica variação importante entre períodos.

**O que é Grid Search?** É testar todas as combinações da grade definida. Na floresta, são quatro combinações × cinco folds: 20 ajustes, mais o refit da melhor.

**O que é Random Search?** É sortear um número limitado de combinações. Na floresta, sorteamos quatro entre 36 possibilidades: 20 ajustes nos folds, mais refit.

**Qual é a diferença entre as duas buscas?** Grid cobre toda a grade escolhida. Random controla o custo pelo número de sorteios e pode explorar outras opções; nenhuma garante a melhor solução fora do espaço testado.

**O que significa scoring='f1'?** É escolher a configuração pelo F1 da classe positiva 1, que é SIM neste projeto. Não significa acurácia nem F1 médio das duas classes.

**Por que escolhemos F1 de SIM?** Porque chuva é a classe rara. Queremos equilibrar alertas corretos e chuvas detectadas; a acurácia pode ficar alta apenas acertando os muitos registros NAO.

**O teste participa das buscas da floresta?** Não. Elas recebem somente `X_train` e `y_train`. A escolha entre buscas usa a média do F1 temporal; a avaliação do teste acontece depois.

**O que é refit?** Depois de escolher a combinação na validação, a busca ajusta esse candidato usando todo o treino. `best_estimator_` já é esse Pipeline treinado.

**O que significa modelo otimizado?** É o candidato ajustado pela busca. Não significa melhor em qualquer situação; aqui houve melhora também no teste, mas a escolha foi feita antes de observar essa comparação.

## Sobre avaliação e interpretação

**O que é uma matriz de confusão?** Uma tabela de classes reais nas linhas e previstas nas colunas. Nossos gráficos usam NAO=0 primeiro e SIM=1 depois: `[[vn, fp], [fn, vp]]`. Os slides da aula colocam positivo primeiro; o importante é respeitar os rótulos.

**O que são verdadeiros e falsos positivos e negativos?** VP: choveu e o modelo disse SIM. FP: não choveu, mas ele disse SIM. FN: choveu, mas ele disse NAO. VN: não choveu e ele disse NAO.

**Qual interpretação foi corrigida na árvore?** O acerto de 1.401 registros NAO era chamado de verdadeiro positivo em tabelas manuais. Como SIM=1 é positivo, esse número é VN; os VP iniciais são 147. Agora as métricas são calculadas automaticamente, sem aquelas contas manuais.

**O que é acurácia?** Total de acertos dividido pelo total: `(vp + vn) / total`.

**O que é precisão?** Entre os alertas SIM, quantos estavam certos: `vp / (vp + fp)`.

**O que é sensibilidade?** Entre as chuvas reais, quantas foram detectadas: `vp / (vp + fn)`. Também se chama recall da classe SIM.

**O que é especificidade?** Entre as horas sem chuva, quantas foram identificadas corretamente: `vn / (vn + fp)`. No código, usamos `recall_score(..., pos_label=0)`.

**O que é F1-score?** É a média harmônica da precisão e da sensibilidade: `2 × precisão × sensibilidade / (precisão + sensibilidade)`. Só fica alto quando as duas estão boas.

**O que é MCC?** É uma medida que combina as quatro partes da matriz. Vai de -1 a 1: 1 indica concordância perfeita; 0 indica ausência de correlação; -1 indica discordância total.

**Por que acurácia sozinha pode enganar?** No teste da floresta, 1.725 de 1.752 horas não tiveram chuva. Dizer NAO em tudo daria 98,46% de acurácia e não encontraria nenhuma chuva. Esse é um cálculo de referência, não outro modelo implementado.

**Por que acompanhar MCC e especificidade se escolhemos por F1?** F1 foca a classe SIM e não usa diretamente os verdadeiros negativos. MCC e especificidade ajudam a verificar o comportamento nas duas classes e os falsos alertas.

**Como os resultados são apresentados?** Acurácia, precisão, sensibilidade, especificidade e F1 em porcentagem com duas casas; MCC com quatro casas. Os cálculos mantêm a precisão original: só a exibição é arredondada.

## Resultados reais

**Quais são os resultados da Decision Tree no teste aleatório?** As duas versões usam o mesmo teste de 1.752 registros, com 264 SIM. Os treinos e hiperparâmetros existentes foram preservados.

| Modelo | Acurácia | Precisão SIM | Sensibilidade SIM | Especificidade | F1 SIM | MCC |
|---|---:|---:|---:|---:|---:|---:|
| Árvore inicial | 88,36% | 62,82% | 55,68% | 94,15% | 59,04% | 0,5241 |
| Árvore ajustada | 89,04% | 64,40% | 60,98% | 94,02% | 62,65% | 0,5626 |

**Quais são os resultados da Random Forest no teste cronológico?** As duas versões usam o mesmo teste de 1.752 registros, com apenas 27 SIM.

| Modelo | Acurácia | Precisão SIM | Sensibilidade SIM | Especificidade | F1 SIM | MCC |
|---|---:|---:|---:|---:|---:|---:|
| Floresta inicial | 98,80% | 100,00% | 22,22% | 100,00% | 36,36% | 0,4686 |
| Floresta ajustada | 99,03% | 85,71% | 44,44% | 99,88% | 58,54% | 0,6133 |

**Como traduzir isso em quantidade de erros?** Na floresta inicial, acertamos 6 chuvas, perdemos 21 e não geramos falsos alertas. Na ajustada, acertamos 12 chuvas, perdemos 15 e geramos 2 falsos alertas. A detecção melhorou, mas ainda deixa passar mais da metade das chuvas do teste.

**Quais são as matrizes reais?** Na ordem `[NAO, SIM]`:

| Modelo | Matriz `[[vn, fp], [fn, vp]]` |
|---|---|
| Árvore inicial | `[[1401, 87], [117, 147]]` |
| Árvore ajustada | `[[1399, 89], [103, 161]]` |
| Floresta inicial | `[[1725, 0], [21, 6]]` |
| Floresta ajustada | `[[1723, 2], [15, 12]]` |

**Quais foram os melhores hiperparâmetros das buscas da árvore?** A tabela separa validação e teste. A escolha histórica da árvore final foi mantida; a apresentação não trocou parâmetros.

| Busca da árvore | Critério | Profundidade | Mínimo por folha | F1 médio CV | F1 teste |
|---|---|---:|---:|---:|---:|
| Grid Search | entropy | 6 | 10 | 63,03% | 58,30% |
| Random Search | entropy | 9 | 3 | 61,41% | 62,65% |

**O Random Search foi superior ao Grid?** Na árvore, só no F1 do teste. O Grid teve maior média de validação. Na floresta, as duas buscas chegaram à mesma configuração e empataram no F1 médio temporal. Não podemos afirmar superioridade geral de uma busca.

**Quais foram os melhores hiperparâmetros da floresta?** Ambas encontraram a mesma configuração; o desempate previamente definido escolheu Grid, sem consultar o teste.

| Busca da floresta | Árvores | Profundidade | Mínimo por folha | Atributos por divisão | F1 médio CV temporal |
|---|---:|---|---:|---|---:|
| Grid Search | 100 | sem limite | 3 | sqrt | 64,02% |
| Random Search | 100 | sem limite | 3 | sqrt | 64,02% |

**Qual foi a melhora na validação da floresta?** F1 temporal médio de 50,93% no modelo inicial e 64,02% no candidato ajustado. Essa comparação foi usada para estudar os ajustes dentro do treino; não é o F1 do teste.

**Quais valores de MCC são de validação da árvore?** Inicial: 0,5275; ajustada: 0,5467. Eles vêm dos cinco folds do treino. Os MCC de teste são 0,5241 e 0,5626, respectivamente.

**A validação F1 da árvore representa a árvore inicial?** A célula original de F1 cria uma árvore com parâmetros padrão e semente 42: média de 56,89%, com desvio de 2,78 pontos percentuais. Ela é diferente da inicial limitada a profundidade 5. O notebook agora identifica essa diferença.

**Quais atributos mais influenciaram a floresta ajustada?** As importâncias abaixo vêm das divisões das árvores e estão no notebook 10:

| Atributo | Participação na importância total |
|---|---:|
| Umidade relativa do ar no horário | 16,19% |
| Umidade máxima da hora anterior | 11,21% |
| Umidade mínima da hora anterior | 9,58% |
| Hora | 6,28% |
| Temperatura mínima da hora anterior | 5,28% |

**Importância significa causa?** Não. É contribuição para as divisões do modelo. Variáveis correlacionadas podem dividir importância, e esse ranking não demonstra que uma variável causou chuva.

**E o ranking da Decision Tree?** O notebook 09 não apresenta um ranking de importância. Não inventamos valores nem acrescentamos esse cálculo nesta etapa de padronização.

**Podemos afirmar que um algoritmo é melhor que o outro?** Não com esses testes. A árvore usa teste aleatório com 264 chuvas e a floresta usa outro período com 27. Podemos comparar inicial e ajustado dentro de cada fluxo, mas não declarar um vencedor entre algoritmos.

## Limitações e perguntas prováveis

**Quais são as limitações atuais?** Somente uma estação e um ano, desbalanceamento, poucas chuvas no teste final, possível dependência temporal e rótulos de ausência de precipitação que precisam de revisão. O fluxo da árvore também mantém o pré-processamento anterior à divisão.

**O teste é completamente novo para nós?** Não: já havia sido consultado em versões anteriores. Nesta execução da floresta ele ficou fora das buscas; uma confirmação realmente nova exigiria outro período de dados.

**O que falta implementar?** No escopo solicitado, as métricas, as buscas e a comparação da floresta estão implementadas. Permanecem como trabalho futuro: revisar qualidade/rótulos, tratar o risco de leakage da árvore, usar testes comparáveis e avaliar outros anos.

**O que seria necessário para prever chuva futura?** Definir um horizonte e usar somente variáveis disponíveis antes do horário previsto, com atributos defasados e validação temporal adequada. Isso não foi implementado.

**Por que não acrescentamos outros algoritmos da aula?** O escopo ficou em Decision Tree e Random Forest. Boosting e outros métodos aparecem na teoria da aula, mas não foram implementados neste trabalho.

**Por que cem árvores podem superar quatrocentas neste resultado?** Não foi só a quantidade: a busca também aumentou o mínimo por folha para 3. Mais árvores não garantem melhor F1; os parâmetros foram escolhidos em conjunto pela validação.

**O sorteio do Random Search encontrou o mesmo candidato do Grid. Isso é erro?** Não. Os espaços se sobrepõem e o sorteio pode visitar a mesma configuração. Os dois avaliaram essa configuração nos mesmos folds.

**Posso escolher parâmetros pelo maior resultado do teste?** Não é uma boa prática: isso transforma o teste em parte da seleção. A floresta escolhe pelo F1 de validação; a escolha histórica da árvore é uma limitação documentada, não foi refeita para melhorar números.

**Como sei que o código calcula as métricas?** Nos notebooks 09 e 10, elas vêm de `accuracy_score`, `precision_score`, `recall_score`, `f1_score` e `matthews_corrcoef`. A matriz vem de `confusion_matrix` ou de `ConfusionMatrixDisplay`. Não há cálculos manuais substituindo os resultados.

**O que foi alterado para padronizar a apresentação?** Formatação, tabelas e explicações. A árvore mantém os mesmos ajustes, parâmetros e divisões. A floresta mantém a metodologia e os espaços de busca definidos na finalização; não fizemos novas tentativas para melhorar a métrica depois da avaliação.

## Onde encontrar cada etapa

| Etapa | Notebook | Situação |
|---|---|---|
| Criação de CHUVA | `dataset/df_adaptado.ipynb` | Implementada; gera cópia sem alterar o CSV fornecido. |
| Exploração e frequência das classes | `01_analise_exploratoria.ipynb` | Implementada. |
| Nulos e duplicados | `02_analise_valores_nulos.ipynb` | Implementada. |
| Remoção de colunas, média, codificação e normalização da árvore | `06_pre-processamento.ipynb` | Implementadas; ajuste anterior à divisão continua como limitação. |
| Divisão da árvore e undersampling disponível | `07_divisao_e_balanceamento.ipynb` | Implementados; treino balanceado não alimenta a árvore. |
| Árvore inicial/ajustada, matrizes e métricas automáticas | `09_decision_tree.ipynb` | Implementadas e identificadas como teste. |
| CV, Grid e Random Search da árvore | `09_decision_tree.ipynb` | Mantidos; tabela distingue CV e teste. |
| Pipeline, pesos e divisão cronológica da floresta | `10_random_forest.ipynb` | Implementados. |
| Cinco folds temporais e duas buscas pequenas | `10_random_forest.ipynb` | Implementados apenas no treino. |
| Matrizes, métricas e comparação da floresta | `10_random_forest.ipynb` | Implementadas no mesmo teste reservado. |
| Importância dos atributos da floresta | `10_random_forest.ipynb` | Implementada para inicial e ajustada. |
| Previsão futura, revisão de rótulos e teste comum entre algoritmos | Nenhum | Pendências ou sugestões, não resultados já implementados. |

## Resposta curta para abrir a apresentação

“Estamos classificando ocorrência de chuva horária em Caruaru. Já exploramos e preparamos os dados, temos uma árvore de decisão e finalizamos a Random Forest. Na floresta, escolhemos hiperparâmetros pelo F1 de chuva em cinco validações temporais, sem usar o teste na busca. A versão ajustada detectou 12 das 27 chuvas do teste, contra 6 da inicial. Ainda precisamos ampliar os dados e revisar limitações antes de falar em previsão futura ou superioridade de um algoritmo.”
