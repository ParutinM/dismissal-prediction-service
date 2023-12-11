import email
import hydra
import pandas as pd

import opendatasets as od
from sqlalchemy import create_engine

from sqlalchemy.orm import Session
from typing import List
from tqdm import tqdm
from omegaconf import DictConfig
from pathlib import Path

from tables import User, Mail
from googletrans import Translator


def get_text_from_email(msg: email.message.Message) -> str:
    """To get the content from email objects"""
    parts = []
    for part in msg.walk():
        if part.get_content_type() == 'text/plain':
            parts.append(part.get_payload())
    return ''.join(parts)


def split_email_addresses(line: str) -> List[str]:
    """To separate multiple email addresses"""
    if line:
        addresses = line.split(',')
        addresses = list(map(lambda x: x.strip(), addresses))
    else:
        addresses = list()
    return addresses


def get_user_config(em: str) -> dict:
    cfg = {
        "email": em,
        "is_employee": "@enron.com" in em,
        "name": ' '.join(
            [_.capitalize() for _ in em.replace("@enron.com", '').split('.')])
        if "@enron.com" in em else None,
        "chief_id": None
    }
    return cfg


def get_mail_config(msg: email.message.Message) -> dict:
    cfg = {
        "date": pd.to_datetime(msg['Date'], errors='ignore'),
        "subject": msg['Subject'],
        "subject_type": 'replied' if 're:' == msg['Subject'][:3].lower() else
                        'forwarded' if 'fw:' == msg['Subject'][:3].lower() else
                        'empty' if len(msg['Subject']) == 0 else
                        'ordinary',
        "content": get_text_from_email(msg),
    }
    return cfg


@hydra.main(config_path='.', config_name='config.yaml', version_base=None)
def scrap_to_db(cfg: DictConfig):
    # open data with pandas
    if not Path(f"{cfg.dataset.dir}/{cfg.dataset.name}/{cfg.dataset.file}").exists():
        od.download_kaggle_dataset(cfg.dataset.url, cfg.dataset.dir)
    data = pd.read_csv(f"{cfg.dataset.dir}/{cfg.dataset.name}/{cfg.dataset.file}")

    # scrapping data
    users = {}
    engine = create_engine(f"{cfg.driver}://{cfg.host}:{cfg.port}/{cfg.database.name}")
    for msg in tqdm(data.message, desc="Loading data"):
        mails = []
        msg = email.message_from_string(msg)
        for from_email in split_email_addresses(msg["From"]):
            for to_email in split_email_addresses(msg["To"]):
                if from_email not in users.keys():
                    users[from_email] = User(**get_user_config(from_email))
                if to_email not in users.keys():
                    users[to_email] = User(**get_user_config(to_email))
                mails.append(Mail(
                    from_=users[from_email],
                    to=users[to_email],
                    **get_mail_config(msg)
                ))

        # load to db
        with Session(engine) as session:
            session.add_all(mails)
            session.commit()


if __name__ == "__main__":
    scrap_to_db()
