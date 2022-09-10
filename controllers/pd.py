from datetime import datetime


class ProportionalDerivativeController:
    def __init__(self, kp: float, kd: float):
        self._kp = kp
        self._kd = kd
        self._last_value = 0
        self._last_time = datetime.utcnow()

    def calculate(self, value: int) -> int:
        time = datetime.utcnow()
        time_delta = max((time - self._last_time).seconds, 1)
        output = (value * self._kp) + int(
            self._kd * (value - self._last_value) / time_delta
        )
        self._last_value = value
        self._last_time = time
        return output
