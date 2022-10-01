import signal
from serial import Serial
from time import sleep
from queue import Queue

from settings import Settings
from worker import LowLevelParser, Controller
from llp import data_parser

import requests

settings = Settings()


llp_output_queue = Queue(maxsize=10)


uart = Serial(port=settings.PORT, baudrate=settings.BAUDRATE, timeout=0.1)

llp = LowLevelParser(
    uart=uart,
    header=0x7E,
    input_queue=Queue(),
    output_queue=llp_output_queue,
)

raw_temperature_queue = Queue(maxsize=10)
controlled_temperature_queue = Queue(maxsize=10)

temperature_controller = Controller(
    input_queue=raw_temperature_queue,
    output_queue=controlled_temperature_queue,
    kp=1,
    kd=0.1,
    ki=0,
)

def handler(signum, frame):
    print("\nCtrl-c was pressed.")
    llp.stop()
    exit()


signal.signal(signal.SIGINT, handler)

llp.start()
temperature_controller.start()

sensor_map = {0xA6: "Temperature", 0x9C: "Preasure"}

while True:
    if not llp_output_queue.empty():
        data = llp_output_queue.get()
        values = data_parser(data=data, map=sensor_map)
        print(values)
        for value in values:
            if value.name == "Temperature":
                raw_temperature_queue.put(value.value)
    
    if not controlled_temperature_queue.empty():
        value = controlled_temperature_queue.get()
        print(value)
    sleep(0.1)

