from datetime import datetime


class TimeUtils:

    @staticmethod
    def time_diff_natural_day(valuation_date: datetime, expiration_date: datetime):
        return (expiration_date.timestamp() - valuation_date.timestamp()) / (3600 * 24 * 365)
