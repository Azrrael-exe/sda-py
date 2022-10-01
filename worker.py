import abc
from time import sleep
from queue import Queue
from serial import Serial
from threading import Thread
from datetime import datetime

import logging


class Worker(abc.ABC):
    def __init__(self, input_queue: Queue, output_queue: Queue):
        self._input_queue = input_queue
        self._output_queue = output_queue
        self._running = False
        self._thread = None

    @abc.abstractmethod
    def _execute(self) -> None:
        pass

    def _run(self):
        self._running = True
        while self._running:
            self._execute()
        self._close()

    def stop(self):
        self._running = False

    def _close(self):
        pass

    def start(self) -> None:
        self._thread = Thread(target=self._run)
        self._thread.start()

    @property
    def running(self) -> bool:
        return self._running


class LowLevelParser(Worker):
    def __init__(
        self,
        input_queue: Queue,
        output_queue: Queue,
        uart: Serial,
        header: int,
    ):
        super().__init__(input_queue=input_queue, output_queue=output_queue)
        self._header = header
        self._uart = uart

    def _close(self) -> None:
        self._uart.close()

    def _execute(self) -> None:
        received_header = self._uart.read(size=1)
        if received_header:
            if ord(received_header) == self._header:
                package_size = ord(self._uart.read(size=1))
                payload = [b for b in self._uart.read(size=package_size)]
                checksum = ord(self._uart.read(size=1))
                calculated_checksum = 0xFF - (sum(payload) & 0b11111111)
                logging.info(checksum)
                if checksum == calculated_checksum:
                    self._output_queue.put(payload)


class Controller(Worker):
    def __init__(
        self, input_queue: Queue, output_queue: Queue, kp: float, kd: float, ki: float
    ):
        super().__init__(input_queue=input_queue, output_queue=output_queue)
        self._ki = ki 
        self._kd = kd
        self._kp = kp

        self._last_value = 0
        self._last_time = datetime.utcnow()

    def _execute(self) -> None:

        value = self._input_queue.get()
        time = datetime.utcnow()
        time_delta = max((time - self._last_time).seconds, 1)
        output = (value * self._kp) + int(
            self._kd * (value - self._last_value) / time_delta
        )
        self._last_value = value
        self._last_time = time
        
        self._output_queue.put(output)
        sleep(5)
