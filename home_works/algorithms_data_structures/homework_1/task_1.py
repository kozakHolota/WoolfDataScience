import random
from dataclasses import dataclass
from enum import Enum
from operator import getitem
from queue import Queue
from uuid import UUID, uuid4

class RequestPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class RequestStatus(Enum):
    PENDING = 1
    IN_PROGRESS = 2
    DONE = 3

    def __str__(self):
        return self.name

@dataclass
class Request:
    id: UUID
    priority: RequestPriority
    time: int
    description: str
    status: RequestStatus

    def __str__(self):
        return f"Request {self.id} with priority {self.priority.name} and time {self.time}. Status: {self.status}"

class RequestManager:
    def __init__(self):
        self.requests = Queue()

    def add_request(self, priotity: RequestPriority, time: int, description: str):
        self.requests.put(Request(uuid4(), priotity, time, description, status=RequestStatus.PENDING))

    def process_request(self):
        if not self.requests.empty():
            request = self.requests.get()
            request.status = RequestStatus.IN_PROGRESS
            print("Working on request: " + str(request))
            request.status = RequestStatus.DONE
            print("Request done: " + str(request))
            print("Queue is empty") if self.requests.empty() else print("Queue is not empty")
        else:
            raise ValueError("Queue is full. Cannot add request")

def generate_request(rm: RequestManager):
    priotiry = getitem(RequestPriority, random.choice(tuple(RequestPriority.__members__.keys())))
    time = random.randint(1, 10)
    description = "Request description"
    rm.add_request(priotiry, time, description)

if __name__ == "__main__":
    rm = RequestManager()
    try:
        while True:
            generate_request(rm)
            rm.process_request()
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)
