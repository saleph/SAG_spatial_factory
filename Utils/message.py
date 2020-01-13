from spade.message import Message


def _prepare_message(receiver, information):
    msg = Message(to=receiver)
    msg.thread = information['thread']
    msg.body = information['body']
    msg.set_metadata("performative", "inform")
    msg.set_metadata("message_id", str(information['id']))
    return msg