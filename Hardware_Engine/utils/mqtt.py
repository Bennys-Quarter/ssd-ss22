from paho.mqtt import client as mqtt_client
from utils.database import get_topic_list
from utils.entity import Entity

topics = ["ESP-TEST/temp_sensor"]


def on_connect(client, userdata, flags, rc):
    if not rc:
        print("Info: MQTT successfully connected")
    else:
        print("Error: Failed to connect MQTT, rc=%d", rc)


def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    update_entity = Entity(mqtt_topic=msg.topic)
    update_entity.actual_value = msg.payload.decode()
    update_entity.update()


def subscribe(client):
    topics = get_topic_list()
    for topic in topics:
        client.subscribe(topic)


def unsubscribe(topic):
    pass


def init(mqtt_conn_params):
    client = mqtt_client.Client("HARDWARE_ENGINE")
    client.username_pw_set(mqtt_conn_params['username'], mqtt_conn_params['password'])
    client.on_connect = on_connect
    client.connect(mqtt_conn_params['server'], int(mqtt_conn_params['port']))
    client.on_message = on_message
    subscribe(client)
    return client


def loop_start(client):
    client.loop_start()
