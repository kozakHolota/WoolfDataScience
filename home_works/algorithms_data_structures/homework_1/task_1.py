from dataclasses import dataclass
from enum import Enum
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

@dataclass
class Request:
    id: UUID
    priority: RequestPriority
    time: int
    description: str
    status: RequestStatus

    def __str__(self):
        return f"Request {self.id} with priority {self.priority.name} and time {self.time}. Status: {self.status.name}"

class RequestManager:
    def __init__(self):
        self.requests = Queue()

    def add_request(self, priotity: RequestPriority, time: int, description: str):
        self.requests.put(Request(uuid4(), priotity, time, description, status=RequestStatus.PENDING))

    def process_requests(self):
        while not self.requests.empty():
            request = self.requests.get()
            request.status = RequestStatus.IN_PROGRESS
            print(f"Processing request {request}.")
            request.status = RequestStatus.DONE
            print(f"Request {request.id} is done. Desxcription: {request}")
            self.requests.put(request)
