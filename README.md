# flask-sklearn
Python flask app that does CRUD on sklearn models

The MySQL DB has a single table with schema as:-
```
    MODEL_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    MODEL_NAME VARCHAR(255),
    MODEL_PARAMS TEXT,
    MODEL_PKL BLOB(65535),
    NUM_FEATURES INT,
    NUM_CLASSES INT,
    NUM_TRAINED INT
```

Also, supports a bonus API  - "Get groups of models that are at same
training stage" GET /models/groups/