import utils.database as dbutils
import utils.mqtt as mqttutils


class Entity:
    def __init__(self, _id_: str, mqtt_topic="", address="", _type_="", target_value="", actual_value=""):
        self._id_ = _id_
        self.mqtt_topic = mqtt_topic
        self.address = address
        self._type_ = _type_
        self.target_value = target_value
        self.actual_value = actual_value

    def delete(self):
        if not dbutils.delete_entity(self._id_):
            return False
        mqttutils.unsubscribe(self.mqtt_topic)

    def register(self):
        return dbutils.insert_entity(self.to_dict())
    def update(self):
        dbutils.update_entity(self.to_dict())

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
        if self._type_ == "sensor":
            return {
                "id": self._id_,
                "address": self.address,
                "value": self.actual_value
            }
        else:
            return {
                "id": self._id_,
                "value": self.actual_value
            }
