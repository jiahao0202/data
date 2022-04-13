import unittest
from datetime import datetime

from product.options.vanilla_option import VanillaOption
from utils.product_util import OptionTypeEnum


class TestVanillaOptionPricer(unittest.TestCase):
    def setUp(self) -> None:
        self.vanilla_option = VanillaOption(expiration_date=datetime(2022, 4, 6),
                                            strike=100,
                                            option_type=OptionTypeEnum.Call)

