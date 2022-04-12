class GreeksParams:
    def __init__(
            self,
            spot_bump_size,
            vol_bump_size,
            interest_rate_bump_size,
            dividend_bump_size,
            is_spot_bump_pct=True,
    ):
        self.__spot_bump_size = spot_bump_size
        self.__vol_bump_size = vol_bump_size
        self.__interest_rate_bump_size = interest_rate_bump_size
        self.__dividend_rate_bump_size = dividend_bump_size
        self.__is_spot_bump_pct = is_spot_bump_pct

    def bump_spot(self, spot):
        if self.__is_spot_bump_pct:
            return spot * self.__spot_bump_size
        else:
            return spot + self.__spot_bump_size

    def vol_bump(self):
        return self.__vol_bump_size

    def interest_rate_bump(self):
        return self.__interest_rate_bump_size

    def dividend_bump(self):
        return self.__dividend_rate_bump_size
