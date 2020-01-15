class MessageThreadCounter:

    def __init__(self, thread_id = None, counter = 0 ):
        self.thread_id = thread_id
        self.counter = counter

    def increaseCounter(self):
        self.counter += 1

    def decreaseCounter(self) -> bool:
        self.counter -= 1
        return self.isCounterEmpty()

    def getCounterValue(self):
        return self.counter

    def isCounterEmpty(self):
        return self.counter == 0