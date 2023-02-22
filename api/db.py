import MySQLdb
import os
import pickle
import json
from http import HTTPStatus
from flask import abort

def connect():
    """ https://mysqlclient.readthedocs.io/user_guide.html#mysqldb """
    return MySQLdb.connect(host=os.environ['MYSQL_HOST'],
                           user=os.environ['MYSQL_USER'],
                           passwd=os.environ['MYSQL_ROOT_PASSWORD'],
                           db=os.environ['MYSQL_DATABASE'])

# connect to db and persist
def persist_model(model_name, model_params, model, num_features, num_classes, n_trained):
    try:
        connection = connect()
        cursor = connection.cursor()
    
        sql_query = """INSERT INTO MODEL_METADATA (MODEL_NAME, MODEL_PARAMS, MODEL_PKL, NUM_FEATURES, NUM_CLASSES, NUM_TRAINED) VALUES (%s, %s, %s, %s, %s, %s)"""
        val = (model_name, json.dumps(model_params), pickle.dumps(model), num_features, num_classes, n_trained)
        cursor.execute(sql_query, val)
        connection.commit()
    
        id = cursor.lastrowid

        cursor.close()
        return id
    except:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description = "Unable to save model")
    finally:
        if connection:
            connection.close()

def retrieve_model(id):
    try:
        connection = connect()
        cursor = connection.cursor()

        sql_query = "SELECT * FROM MODEL_METADATA WHERE MODEL_ID = %s"
        print(id)
        cursor.execute(sql_query, (id,))
        records = cursor.fetchall()
        # No row found for model_id
        if not records:
            raise Exception

        cursor.close()
        return records
    except:
        abort(HTTPStatus.NOT_FOUND, description = "Invalid Model ID")
    finally:
        if connection:
            connection.close()

def update_num_train(model_id, num_train):
    try:
        connection = connect()
        cursor = connection.cursor()

        sql_query = "UPDATE MODEL_METADATA SET NUM_TRAINED = %s WHERE MODEL_ID = %s"
        cursor.execute(sql_query, (num_train, model_id,))

        connection.commit()
        cursor.close()
    except:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description = "SQL ERROR")
    finally:
        if connection:
            connection.close()

def create_table():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS MODEL_METADATA (
    MODEL_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    MODEL_NAME VARCHAR(255),
    MODEL_PARAMS TEXT,
    MODEL_PKL BLOB(65535),
    NUM_FEATURES INT,
    NUM_CLASSES INT,
    NUM_TRAINED INT
    )''')
    connection.commit()

    cursor.close()
    connection.close()

def drop_table():
    connection = connect()
    cursor = connection.cursor()
    
    cursor.execute("DROP TABLE MODEL_METADATA")
    connection.commit()
    cursor.close()
    connection.close()