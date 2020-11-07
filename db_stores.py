import pymysql
from pymysql.constants import CLIENT

def get_connection(config):
    connection = pymysql.connect(
        host=config['sqlhost'],
        user=config['sqluser'],
        password=config['sqlpassword'],
        db=config['sqldbname'],
        client_flag=CLIENT.MULTI_STATEMENTS
    )
    return connection

def one_store(config, store_id):
    connection = get_connection(config)
    try:
        cursor = connection.cursor()
        query = """
                SELECT * FROM Stores
                WHERE Stores.Store_ID = %s;
                """
        cursor.execute(query, store_id)
        store = cursor.fetchone()
    finally:
        connection.close()
    return {
        "id": store[0],
        "name": store[1],
        "location": store[2],
        "hours": store[3],
        "owner": store[4],
        "ratings": store[5],
        "covid_restrictions": store[6]
    }

def all_stores(config):
    connection = get_connection(config)
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM Stores;"
        cursor.execute(query)
        result = cursor.fetchall()
    finally:
        connection.close()

    result = list(map(lambda store: {
        "id": store[0],
        "name": store[1],
        "location": store[2],
        "hours": store[3],
        "owner": store[4],
        "ratings": store[5],
        "covid_restrictions": store[6]
    }, list(result)))
    return result

def search_stores_by_name(config, keyword):
    connection = get_connection(config)
    try:
        cursor = connection.cursor()
        query = """
                SELECT * FROM Stores
                WHERE Stores.Store_Name LIKE %s;
                """
        cursor.execute(query, f"%{keyword}%")
        result = cursor.fetchall()
    finally:
        connection.close()

    result = list(map(lambda store: {
        "id": store[0],
        "name": store[1],
        "location": store[2],
        "hours": store[3],
        "owner": store[4],
        "ratings": store[5],
        "covid_restrictions": store[6]
    }, list(result)))
    return result

def create_store(config, name, location, hours, owner, ratings, covid_restrictions):
    connection = get_connection(config)
    try:
        cursor = connection.cursor()
        query = """
                INSERT INTO Stores(
                    Store_Name, Store_Location, Opening_Hours,
                    Store_Owner, Store_Ratings, Covid_Restrictions
                ) VALUES (%s, %s, %s, %s, %s, %s);
                """
        cursor.execute(query, (name, location, hours, owner, ratings, covid_restrictions))
        result = cursor.lastrowid
        connection.commit()
    finally:
        connection.close()
    return result

def update_store(config, store_id, name, location, hours, owner, ratings, covid_restrictions):
    connection = get_connection(config)
    try:
        cursor = connection.cursor()

        if name:
            query = """
                    UPDATE Stores
                    SET Store_Name = %s
                    WHERE Store_ID = %s
                    """
            cursor.execute(query, (name, store_id))

        if location:
            query = """
                    UPDATE Stores
                    SET Store_Location = %s
                    WHERE Store_ID = %s
                    """
            cursor.execute(query, (location, store_id))

        if hours:
            query = """
                    UPDATE Stores
                    SET Opening_Hours = %s
                    WHERE Store_ID = %s
                    """
            cursor.execute(query, (hours, store_id))

        if owner:
            query = """
                    UPDATE Stores
                    SET Store_Owner = %s
                    WHERE Store_ID = %s
                    """
            cursor.execute(query, (owner, store_id))

        if ratings:
            query = """
                    UPDATE Stores
                    SET Store_Ratings = %s
                    WHERE Store_ID = %s
                    """
            cursor.execute(query, (ratings, store_id))

        if covid_restrictions:
            query = """
                    UPDATE Stores
                    SET Covid_Restrictions = %s
                    WHERE Store_ID = %s
                    """
            cursor.execute(query, (covid_restrictions, store_id))
        connection.commit()
    finally:
        connection.close()
    return store_id

# import json
# with open('config.json') as f:
#     config = json.load(f)

# if __name__ == "__main__":
#     print(update_stores(config, 3, "", "", "", "", "", ""))
