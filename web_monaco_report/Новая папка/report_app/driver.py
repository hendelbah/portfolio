from datetime import datetime
from peewee import *


class Driver(Model):
    code = CharField(primary_key=True)
    full_name = CharField()
    car = CharField()
    lap_start = DateTimeField()
    lap_end = DateTimeField()
    lap_time = CharField()
    rank = fn.DENSE_RANK().over(order_by=lap_time.asc()).alias('rank')

    FIELDS = [rank, code, full_name, car, lap_time]

    @staticmethod
    def calc_time(lap_end, lap_start):
        """
        Get lap_time in appropriate format. **Return None if any of args is None**\n
        :type lap_end: datetime
        :type lap_start: datetime
        :return: lap_end and lap_start difference as str or None
        """
        if lap_end is not None and lap_start is not None:
            return f"{lap_end - lap_start}"[:-3]
        else:
            return None
