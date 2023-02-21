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

    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""USE ModelDB""")
    connection.commit()
    
    sql = """INSERT INTO MODEL_METADATA (MODEL_NAME, MODEL_PARAMS, MODEL_PKL, NUM_FEATURES, NUM_CLASSES, NUM_TRAINED) VALUES (%s, %s, %s, %s, %s, %s)"""
    val = (model_name, json.dumps(model_params), pickle.dumps(model), num_features, num_classes, n_trained)
    cursor.execute(sql, val)
    connection.commit()
    
    id = cursor.lastrowid

    cursor.close()
    connection.close()
    return id

def retrieve_model(id):
    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""USE ModelDB""")
        connection.commit()

        sql = "SELECT * FROM MODEL_METADATA WHERE MODEL_ID = %s"
        mid = f'{id}'
        cursor.execute(sql, mid)
        records = cursor.fetchall()
        print("Total rows are: ", len(records))
        result = {}
        for row in records:
            result['model'] = row[1]
            result['params'] = json.loads(row[2])
            result['d'] = row[4]
            result['n_classes'] = row[5]
            result['n_trained'] = row[6]

        cursor.close()
        return result
    except:
        abort(HTTPStatus.NOT_FOUND, description = "Invalid Model ID")
    finally:
        if connection:
            connection.close()

def create_table():
    connection = connect()
    cursor = connection.cursor()
    #create database
    cursor.execute("""CREATE DATABASE IF NOT EXISTS ModelDB""")
    connection.commit()
    
    cursor.execute("""USE ModelDB""")
    connection.commit()

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

    cursor.execute("DESCRIBE ModelDB.MODEL_METADATA")
    indexList = cursor.fetchall()

    print(indexList)    
    
    cursor.close()
    connection.close()

def drop_table():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""USE ModelDB""")
    connection.commit()
    cursor.execute("DROP TABLE MODEL_METADATA")
    connection.commit()
    cursor.close()
    connection.close()