# Dismissal prediction service
via hackathon ["Leaders of Digital Transformation"](https://i.moscow/cabinet/lct/hackatons/b092bcd74cc6478e98595ac2b319881a)

### Description

A service for predicting the imminent dismissal of each employee 
depending on events when working with corporate email.

Service includes:
- NN model
- Web-service

### Preparing for usage

#### 1. Poetry

This tool needs to download all `python` dependencies for this project

To download `poetry` execute in terminal
```shell
curl -sSL https://install.python-poetry.org | python3 -
```
and add to your PATH

To download all dependencies create/activate `python` environment and print:
```shell
poetry install
```
All dependencies will be downloaded 

#### 2. PostgresSQL

As database this project uses `PostgresSQL`. To download it use the instruction 
from [official website](https://www.postgresql.org/download/).

After downloading it run `./db/create_db.py` to create database.

If you want to fill it with [Enron Email Dataset](https://www.kaggle.com/datasets/wcukierski/enron-email-dataset), 
which was used to train model, run `./db/scrap_enron_email_dataset.py`

**Note:** To download from Kaggle you need to put in `./db` your private key `kaggle.json`. 
It should look like:
```json
{"username":"your_kaggle_username","key":"your_kaggle_key"}
```

