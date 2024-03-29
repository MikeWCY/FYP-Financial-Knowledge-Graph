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
├── requirement.txt
├── crawler
├── ├── scrapy_wikicategory  # get entities pages from wikidata category lists and crawl wikipedia pages
├── ├── orgRelation # get 9319 triple entity-relation-entity list from wikidata
├── ├── wikientities # crawl the info of entities according to the entity_list.json
├── data_processor
├── ├── report_crawler.py
├── ├── report_parser.py
├── ├── report2
├── ├── Data2
├── data
├── ├── infobox # data collected from wikipedia infobox
├── ├── relation # data collected from wikidata pages
├── FYP-main # interface
├── ├── clf_multi.joblib
├── ├── main.py
├── ├── question.py
├── ├── graph.py
├── ├── test.py
├── ├── demo.html
├── models
├── ├── TrainClassifier
├── ├── ├── generate_embeds.py
├── ├── ├── trainclassifier.py
├── ├── bert-ner.ipynb
├── ├── sec-bert-simple.ipynb
.

```

# 0. Configuration
<br/> database: neo4j
<br/> language: python3
<br/> IDE: PyCharm
<br/> anaconda
<br/> jupyter notebook
<br/> package: 
<br/> $pip install -r requirement.txt
# 1. crawler
## 1.1 scrapy_wikicategory
### 1.1.1 Package installed:
<br/> numpy, scrapy, tqdm, lxml
### 1.1.2 conselor:
<br/>  get entities and their wikipages starting from  "https://en.wikipedia.org/wiki/Category:Banks_of_China"
<br/>  queue1.py: add original request and start the queue to crawl
<br/>  how to start: run main.py in PyCharm
### 1.1.3 data_preprocess:
<br/> origin-page: storing 664 crawed raw pages
<br/> process.py: get structured data from raw pages, write wikipedia_info.json
<br/> process: pre-process the original pages and make classification
<br/> result_lower: 51 resulting files in terms of relations
<br/> rseult_process: get information of product and services
## 1.2 orgRelation
### 1.2.1 results
<br/> entities_list.json: all the entities and their searching information during crawling
<br/> entityRelation_list.json: all the triple relations
<br/> relation: storing the result data
### 1.2.2 Package installed: 
<br/> scrapy, json,time,requests,os,codes,csv
## 1.3 wikientities
### 1.3.1 Package installed
<br/> scrapy, requests
### 1.3.2 getEntities.py
<br/> main functions of the crawler
### 1.3.3 entities.json
<br/> resulting 721 crawled entites
# 2. data
## 2.1 infobox
## 2.2 relation
# 3. data processor
## 3.1 Package installed
<br/> requests, urllib, pandas, bs4, os, re, csv, pdfplumber
## 3.2 processor
<br/> report_crawler.py: crawl links of reports from www.annualreports.com, and store reports as pdf
<br/> report_parser.py: parse the pdf reports to txt and select  sentences with numbers
## 3.3 result
<br/> report2: crawled pdfs
<br/> Data2: parsed result
# 4. FYP-main (web pages used for demonstration)
## 4.1 Package installed
<br/> re,py2neo,flask,json,textdistance,pandas,operator,codecs,json,streamlit,
<br/> neo4j,pandas,altair,time,transformers,numpy,pandas,torch,datasets,joblib,PIL
## 4.2 Packed model
<br/> clf-multi.joblib
## 4.3 interface pages
<br/> main.py：show demonstration of the five sections
<br/> graph.py：show graph of the slected triples
<br/> question.py 
<br/> test.py
# 5. models
## 5.1 Package installed
<br/> transformers, torch,pandas, numpy, sklearn
## 5.2 baseline models
<br/> bert-ner.ipynb: numeric ner model based on bert-base
<br/> sec-ber-simple.ipynb: numeric ner model based on sec-bert trained with small anount of data
## 5.3 TrainClassifier
### 5.3.1 generate_embeds.py
This file is used to generate the embeddings of the tokens in the training and validation sets. The vast majority of the tokens are labeled as 0. To reduce the training burden, the code is to select a small fraction of the tokens labeled 0 while preserving all tokens labeled otherwise. 
### 5.3.2 trainclassifier.py
This file is to train a logistic regression classifier given the embeddings generated in generate_embeds.py on the training set. A classification report is generated to show the performance of the classifier on the validation set. 
