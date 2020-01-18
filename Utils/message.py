from spade.message import Message


def _prepare_message(receiver, information, *, performative="inform"):
    try:
        msg = Message(to=receiver)
        msg.thread = information['thread']
        msg.body = information['body']
        msg.set_metadata("performative", performative)
        msg.set_metadata("message_id", str(information['id']))
        return msg
    except Exception as e:
        print(e)

def _prepare_system_control_message(receiver, *, performative):
    msg = Message(to=receiver)
    msg.body = performative
    msg.thread = None
    msg.body = "heartbeat"
    msg.set_metadata("performative", performative)
    return msg