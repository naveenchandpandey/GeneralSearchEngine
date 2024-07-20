from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .helpers import ConfigHelper

# Reading config file here again as this is kept as a future provision if we ever require separate config files for
# app and database as the project grows
config_helper = ConfigHelper("app/app_config.cnf")
config = config_helper.get_config()

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{config['MYSQL']['user']}:@{config['MYSQL']['host']}/{config['MYSQL']['database']}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
