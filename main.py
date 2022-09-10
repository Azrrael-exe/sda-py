import signal
from serial import Serial
from time import sleep
from queue import Queue

from settings import Settings
from llp import LLP, data_parser
from controllers.pd import ProportionalDerivativeController

settings = Settings()

input_queue = Queue(maxsize=10)

llp = LLP(
    port=settings.PORT,
    baudrate=settings.BAUDRATE,
    timeout=0.1,
    header=0x7E,
    queue=input_queue,
)


def handler(signum, frame):
    print("\nCtrl-c was pressed.")
    llp.stop()
    exit()


signal.signal(signal.SIGINT, handler)

llp.start()


sensor_map = {0xA6: "Temperature", 0x9C: "Preasure"}
pd = ProportionalDerivativeController(kp=1, kd=0.1)

while True:
    if not input_queue.empty():
        values = data_parser(data=input_queue.get(), map=sensor_map)
        for value in values:
            print(f"{value.name} Sensor: {value.value} with key {hex(value.key)}")
            if value.key == 0xA6:
                print(pd.calculate(value.value))

    sleep(0.01)
