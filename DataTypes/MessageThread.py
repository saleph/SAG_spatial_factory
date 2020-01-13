import json

from DataTypes.MessageDirection import MessageDirection
from DataTypes.MessageThreadType import MessageThreadType


class MessageThread:

    def __init__(self, id = None, message_thread_type: MessageThreadType = None,
                 message_direction: MessageDirection = None, jsonStr= None ):

        self.id = id
        self.message_direction = message_direction
        self.message_thread_type = message_thread_type

        if jsonStr:
            self.FromJson(jsonStr)


    def ToJson(self):

        result = dict()
        result["id"] = self.id;
        result["message_direction"] = self.message_direction.numerator
        result["message_thread_type"] = self.message_thread_type.numerator

        return json.dumps(result)


    def FromJson(self, json_string: str):
        object = json.loads(json_string)
        self.id = object["id"]
        self.message_thread_type = MessageThreadType(object["message_thread_type"])
        self.message_direction = MessageDirection(object["message_direction"])


    def ChangeMessageDirection(self):
        if self.message_direction == MessageDirection.Downward:
            self.message_direction = MessageDirection.Upward
        else:
            self.message_direction = MessageDirection.Downward
