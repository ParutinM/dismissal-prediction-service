import hydra

from omegaconf import DictConfig
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema
from sqlalchemy_utils import database_exists, create_database
from tables import Base


@hydra.main(config_path='.', config_name='config.yaml', version_base=None)
def create_db(cfg: DictConfig) -> None:
    # creates empty db if not exists
    engine = create_engine(f"{cfg.driver}://{cfg.host}:{cfg.port}/{cfg.database.name}")
    if not database_exists(engine.url):
        create_database(engine.url)

    # creates schemas if not exists
    conn = engine.connect()
    conn.execute(CreateSchema(cfg.database.schema, if_not_exists=True))
    conn.commit()

    # create all tables
    Base.metadata.create_all(engine)
    conn.close()


if __name__ == "__main__":
    create_db()
