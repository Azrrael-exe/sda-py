from serial import Serial
from dataclasses import dataclass
from queue import Queue
from threading import Thread


@dataclass
class Variable:
    name: str
    key: int
    value: int


def data_parser(data: list[int], map: dict = {}) -> list[Variable]:
    size = 3
    if not len(data) % size:
        variables = [data[i : i + size] for i in range(0, len(data), size)]
        return [
            Variable(
                name=map.get(variable[0], "unknow"),
                key=variable[0],
                value=(variable[1] << 8 | variable[2]),
            )
            for variable in variables
        ]
    else:
        return []


class LLP(Serial):
    def __init__(
        self, port: str, baudrate: int, timeout: float, header: int, queue: Queue
    ):
        super().__init__(port=port, baudrate=baudrate, timeout=timeout)
        self._header = header
        self._queue = queue
        self._running = False
        self._thread = None

    def stop(self):
        self._running = False

    def run(self):
        self._running = True
        while self._running:
            received_header = self.read(size=1)
            if received_header:
                if ord(received_header) == self._header:
                    package_size = ord(self.read(size=1))
                    payload = [b for b in self.read(size=package_size)]
                    checksum = ord(self.read(size=1))
                    calculated_checksum = 0xFF - (sum(payload) & 0b11111111)
                    if checksum == calculated_checksum:
                        self._queue.put(payload)
        self.close()

    def start(self):
        self._thread = Thread(target=self.run)
        self._thread.start()
