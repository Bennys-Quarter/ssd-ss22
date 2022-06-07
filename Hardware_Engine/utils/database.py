import sqlite3
import os


db_path = "./databases/entities.db"

def init_db():
    if os.path.exists(db_path):
        print("Database already set up!")
        return
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE entities( id TEXT NOT NULL, mqtt_topic TEXT NOT NULL, address TEXT, type TEXT NOT 
    NULL, target_value TEXT, actual_value TEXT)""")
    conn.commit()
    conn.close()


def get_topic_list():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""SELECT DISTINCT mqtt_topic,type FROM entities""")
    results = cursor.fetchall()
    conn.close()
    topic_list = []
    if not results:
        return topic_list
    for result in results:
        topic = result[0]
        _type_ = result[1]
        if _type_ == "sensor" or _type_ == "input":
            topic_list.append({"mqtt_topic": topic, "action": "subscribe"})
        elif _type_ == "output":
            topic_list.append({"mqtt_topic": topic + "_state", "action": "subscribe"})
            topic_list.append({"mqtt_topic": topic, "action": "publish"})
    return topic_list


def get_entity_by_id(_id_: str):
    conn = sqlite3.connect(db_path)
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
        "target_value": result[4],
        "actual_value": result[5]
    }


def get_inventory():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""SELECT id,type FROM entities""")
    results = cursor.fetchall()
    conn.close()
    inventory_list = []
    for result in results:
        inventory_list.append({"id": result[0], "type": result[1]})
    return inventory_list


def get_entity_by_topic(mqtt_topic: str):
    conn = sqlite3.connect(db_path)
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
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    #print(entity_dict)
    if entity_dict["target_value"]:
        cursor.execute("UPDATE entities SET target_value=? WHERE id=?", (entity_dict["target_value"],
                                                                         entity_dict["id"]))
    if entity_dict["actual_value"]:
        cursor.execute("UPDATE entities SET actual_value=? WHERE id=?",
                       (str(entity_dict["actual_value"]),
                        entity_dict["id"]))
    conn.commit()
    conn.close()
    return True


def delete_entity(_id_: str):
    if not get_entity_by_id(_id_):
        return False
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entities WHERE id=?", (_id_,))
    conn.commit()
    conn.close()
    return True


def insert_entity(entity_dict):
    # We do not want not unique IDs and identical topics for different entities
    if get_entity_by_id(entity_dict["id"]) or get_entity_by_topic(entity_dict["mqtt_topic"]):
        return False
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO entities(id, mqtt_topic, address, type) VALUES(?, ?, ?, ?)",
                   (entity_dict["id"], entity_dict["mqtt_topic"], entity_dict["address"], entity_dict["type"]))
    conn.commit()
    conn.close()
    return True
