# Financial Knowledge Graph

# Introduction
The project is aimed to construct a knowledge graph in the financial area, especially, the financial services and their providers. 
Members:
|Name
|----|
|Wang Chenyu|
|Guan Qikun|
|Chen Fang|

# Structure
```
.
├── crawler
├── data processing
├── knowledge graph construction
├── models
├── ├── TrainClassifier
├── ├── ├── generate_embeds.py
├── ├── ├── trainclassifier.py
└── interface
```

# 0. Configuration
├── database: neo4j
├── 
# 1. crawler

# 2. data

# 3. data processor

# 4. FYP-main

# 5. models
## TrainClassifier
### generate_embeds.py
This file is used to generate the embeddings of the tokens in the training and validation sets. The vast majority of the tokens are labeled as 0. To reduce the training burden, the code is to select a small fraction of the tokens labeled 0 while preserving all tokens labeled otherwise. 
### trainclassifier.py
This file is to train a logistic regression classifier given the embeddings generated in generate_embeds.py on the training set. A classification report is generated to show the performance of the classifier on the validation set. 
