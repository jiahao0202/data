from abc import ABC
from datetime import datetime
from product.instrument import Instrument
from utils.product_util import BarrierTypeEnum, BarrierDirectionEnum, RebateTypeEnum


class BarrierOption(Instrument, ABC):
    def __init__(self,
                 expiration_date: datetime,
                 strike: float,
                 barrier: float,
                 rebate: float,
                 barrier_type: BarrierTypeEnum,
                 direction: BarrierDirectionEnum,
                 rebate_type: RebateTypeEnum,
                 is_triggered: bool
                 ):
        super().__init__(expiration_date)
        self.__strike = strike
        self.__barrier = barrier
        self.__barrier_type = barrier_type
        self.__direction = direction
        self.__rebate = rebate
        self.__rebate_type = rebate_type
        self.__is_triggered = is_triggered

    @property
    def strike(self) -> float:
        return self.__strike

    @property
    def barrier(self) -> float:
        return self.__barrier

    @property
    def rebate(self) -> float:
        return self.__rebate

    @property
    def barrier_type(self) -> BarrierTypeEnum:
        return self.__barrier_type

    @property
    def direction(self) -> BarrierDirectionEnum:
        return self.__direction

    @property
    def rebate_type(self) -> RebateTypeEnum:
        return self.__rebate_type

    @property
    def is_triggered(self) -> bool:
        return self.__is_triggered

    def trigger(self):
        self.__is_triggered = True
