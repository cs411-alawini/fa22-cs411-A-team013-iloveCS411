"""Setup at app startup"""
import os
import sqlalchemy
from flask import Flask
from yaml import load, Loader



def init_connection_engine():
    """ initialize database setup
    Takes in os variables from environment if on GCP
    Reads in local variables that will be ignored in public repository.
    Returns:
        pool -- a connection to GCP MySQL
    """


    # detect env local or gcp
    
    if os.environ.get('GAE_ENV') != 'standard':
        try:
            variables = load(open("app.yaml"), Loader=Loader)
        except OSError as e:
            print("Make sure you have the app.yaml file setup")
            os.exit()

        env_variables = variables['env_variables']
        for var in env_variables:
            os.environ[var] = env_variables[var]
    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DB'),
            # host=os.environ.get('MYSQL_HOST')
            query={"unix_socket": os.environ.get('INSTANCE_UNIX_SOCKET')}
        )
    )

    return pool
    

# 
db = init_connection_engine()
'''
conn = db.connect()
results = conn.execute("SELECT * FROM Professors p JOIN Instruct i ON (p.NetId = i.Professor) NATURAL JOIN Sections s NATURAL JOIN Courses c WHERE p.Name LIKE '%%Alawini%%';").fetchall()
print([x for x in results])
conn.close()
'''

app = Flask(__name__)

# To prevent from using a blueprint, we use a cyclic import
# This also means that we need to place this import here
# pylint: disable=cyclic-import, wrong-import-position
from app import routes
