from enum import Enum


class UnitBin(Enum):
    contains_slash = ['/']
    contains_percent = ['%']
    contains_mg = ['mg']
    contains_mol = ['mol']
    contains_day = ['day', 'week', 'month']
    contains_time = ['hour', 'minute', 'second', 'night']
    contains_weight = ['pound', 'kg', 'kilogram']

    def check(self, unit: str) -> int:
        return int(any([v in unit for v in self.value]))
