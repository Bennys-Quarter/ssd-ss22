import utils.database as dbutils
import utils.mqtt as mqttutils


class Entity:
    def __init__(self, _id_="", mqtt_topic="", address="", _type_="", target_value="", actual_value=""):
        self._id_ = _id_
        self.mqtt_topic = mqtt_topic
        self.address = address
        self._type_ = _type_
        self.target_value = target_value
        self.actual_value = actual_value

    def load_from_id(self):
        entity_dict = dbutils.get_entity_by_id(self._id_)
        if not entity_dict:
            return False
        self.mqtt_topic = entity_dict["mqtt_topic"]
        self.address = entity_dict["address"]
        self._type_ = entity_dict["type"]
        self.target_value = entity_dict["target_value"]
        self.actual_value = entity_dict["actual_value"]
        return True

    def load_from_topic(self):
        self.mqtt_topic = self.mqtt_topic.split("_state")[0]  # Filter the output state topic
        entity_dict = dbutils.get_entity_by_topic(self.mqtt_topic)
        if not entity_dict:
            return False
        self._id_ = entity_dict["id"]
        self.mqtt_topic = entity_dict["mqtt_topic"]
        self.address = entity_dict["address"]
        self._type_ = entity_dict["type"]
        self.target_value = entity_dict["target_value"]
        self.actual_value = entity_dict["actual_value"]
        return True

    def get_type(self):
        return self._type_

    def delete(self):
        if not dbutils.delete_entity(self._id_):
            return False
        mqttutils.unsubscribe(self.mqtt_topic)
        return True

    def register(self):
        return dbutils.insert_entity(self.to_dict())

    def update(self, actual_value):
        self.actual_value = actual_value
        entity_dict = self.to_dict()
        dbutils.update_entity(entity_dict=entity_dict)

    def to_dict(self):
        return {
            "id": self._id_,
            "mqtt_topic": self.mqtt_topic,
            "address": self.address,
            "type": self._type_,
            "target_value": self.target_value,
            "actual_value": self.actual_value
        }

    def to_dict_state(self):
        return {
            "id": self._id_,
            "address": self.address,
            "value": self.actual_value
        }
