# encoding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLITE_PATTERN = "sqlite:///%s"


# This method used to create the sqlite connection url string
def config_db_url(db_file, url_pattern=SQLITE_PATTERN):
    "配置数据库链接URL"
    import os
    current_pwd = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.sep.join((current_pwd, db_file))

    if not os.path.exists(db_path):
        dirname = os.path.dirname(db_path)
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        f = open(db_path, 'w+')
        f.close()

    return url_pattern % db_path


# Used to create the session object using an engine object
def config_session(engine):
    "配置会话对象"
    Session = sessionmaker(bind=engine)
    return Session()


# Control if SQLAlchemy should print the logging messages
DB_DEBUG = False

# Sqlite Database data storage file
DB_FILE = "data.sqlite3"

# Construct database connection URL string
DB_URL = config_db_url(DB_FILE)

# Construct Database connection engine
ENGINE = create_engine(DB_URL, encoding='utf8', echo=DB_DEBUG)

# Create the Database connection session object which used to execute the
# database statement
SESSION = config_session(ENGINE)
