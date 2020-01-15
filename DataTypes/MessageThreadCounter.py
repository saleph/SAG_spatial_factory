class MessageThreadCounter:

    def __init__(self, thread_id = None, counter = 1 ):
        self.thread_id = thread_id
        self.counter - counter

    def increaseCounter(self):
        ++self.counter

    def decreaseCounter(self)-> bool:
        --self.counter
        return  self.counter == 0