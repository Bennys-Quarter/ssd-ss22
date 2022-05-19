import sqlite3
import os


def init_db():
    if os.path.exists("entities.db"):
        print("Database already set up!")
        return
    conn = sqlite3.connect("entities.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE entities( id TEXT NOT NULL, mqtt_topic TEXT NOT NULL, address TEXT, type TEXT NOT 
    NULL, target_value TEXT, actual_value TEXT)""")
    conn.commit()
    conn.close()

def get_topic_list():
    conn = sqlite3.connect("entities.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT DISTINCT mqtt_topic FROM entities""")
    result = cursor.fetchall()
    conn.close()
    if result:
        return result[0]
    else:
        return []

def get_entity_by_id(_id_: str):
    conn = sqlite3.connect("entities.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM entities where id=?""", (_id_,))
    result = cursor.fetchone()
    conn.close()
    if not result:
        return {}
    return {
        "id": result[0],
        "mqtt_topic": result[1],
        "address": result[2],
        "type": result[3],
        "target_value": result[3],
        "actual_value": result[4]
    }


def get_entity_by_topic(mqtt_topic: str):
    conn = sqlite3.connect("entities.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM entities where mqtt_topic=?""", (mqtt_topic,))
    result = cursor.fetchone()
    conn.close()
    if not result:
        return {}
    return {
        "id": result[0],
        "mqtt_topic": result[1],
        "address": result[2],
        "type": result[3],
        "target_value": result[3],
        "actual_value": result[4]
    }


def update_entity(entity_dict):
    if not get_entity_by_id(entity_dict["id"]):
        return False
    conn = sqlite3.connect("entities.db")
    cursor = conn.cursor()
    if entity_dict["target_value"]:
        cursor.execute("UPDATE entities SET target_value=? WHERE id=? OR mqtt=?", (entity_dict["target_value"],
                                                                                   entity_dict["id"],
                                                                                   entity_dict["mqtt_topic"]))
    if entity_dict["actual_value"]:
        cursor.execute("UPDATE entities SET actual_value=? WHERE id=? OR mqtt=?", (entity_dict["actual_value"],
                                                                                   entity_dict["id"],
                                                                                   entity_dict["mqtt_topic"]))
    conn.commit()
    conn.close()
    return True


def delete_entity(_id_: str):
    if not get_entity_by_id(_id_):
        return False
    conn = sqlite3.connect("entities.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entities WHERE id=?", (_id_,))
    conn.commit()
    conn.close()
    return True


def insert_entity(entity_dict):
    if get_entity_by_id(entity_dict["id"]):
        return False
    conn = sqlite3.connect("entities.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO entities(id, mqtt_topic, address, type) VALUES(?, ?, ?, ?)",
                   (entity_dict["id"], entity_dict["mqtt_topic"], entity_dict["address"], entity_dict["type"]))
    conn.commit()
    conn.close()
    return True