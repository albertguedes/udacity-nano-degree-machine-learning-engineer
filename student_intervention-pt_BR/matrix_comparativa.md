DecisionTreeClassifier 100 0.0022 0.0005 1.0000 0.0114 0.7003
DecisionTreeClassifier 200 0.0071 0.0012 1.0000 0.0012 0.7185
DecisionTreeClassifier 300 0.0056 0.0008 1.0000 0.0017 0.6446

KNeighborsClassifier   100 0.0021 0.0064 0.8322 0.0096 0.7800
KNeighborsClassifier   200 0.0043 0.0108 0.8882 0.0096 0.7847
KNeighborsClassifier   300 0.0030 0.0179 0.8809 0.0095 0.7801

SVC                    100 0.0032 0.0021 0.8481 0.0027 0.8115
SVC                    200 0.0043 0.0030 0.8868 0.0025 0.8013
SVC                    300 0.0080 0.0056 0.8761 0.0020 0.7838

** Classificador 1 - Árvore de decisão**  

| Tamanho do Conjunto de Treinamento | Tempo de Treinamento | Tempo de Estimativa (teste) | Pontuação F1 (treinamento) | Pontuação F1 (teste) |
| :--------------------------------: | :------------------: | :-------------------------: | :------------------------: | :------------------: |
| 100                                |       0.0022         |        * 0.0005             |       * 1.0000             |        0.7003        |
| 200                                |       0.0071         |          0.0012             |       * 1.0000             |        0.7185        |
| 300                                |       0.0056         |          0.0008             |       * 1.0000             |        0.6446 *      |

** Classificador 2 - k-NN**  

| Tamanho do Conjunto de Treinamento | Tempo de Treinamento | Tempo de Estimativa (teste) | Pontuação F1 (treinamento) | Pontuação F1 (teste) |
| :--------------------------------: | :------------------: | :-------------------------: | :------------------------: | :------------------: |
| 100                                |     * 0.0021         |          0.0064             |         0.8322 *           |        0.7800        |
| 200                                |       0.0043         |          0.0108             |         0.8882             |        0.7847        |
| 300                                |       0.0030         |          0.0179 *           |         0.8809             |        0.7801        |

** Classificador 3 - SVM**  

| Tamanho do Conjunto de Treinamento | Tempo de Treinamento | Tempo de Estimativa (teste) | Pontuação F1 (treinamento) | Pontuação F1 (teste) |
| :--------------------------------: | :------------------: | :-------------------------: | :------------------------: | :------------------: |
| 100                                |       0.0032         |          0.0021             |         0.8481             |      *  0.8115       |
| 200                                |       0.0043         |          0.0030             |         0.8868             |         0.8013       |
| 300                                |       0.0080  *      |          0.0056             |         0.8761             |         0.7838       |

