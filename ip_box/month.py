from dataclasses import dataclass
from datetime import date, timedelta
from functools import cached_property
from typing import Self


@dataclass(frozen=True)
class Month:
    year: int
    month: int

    @classmethod
    def from_date(cls, date: date) -> Self:
        return cls(date.year, date.month)

    @classmethod
    def inclusive_range(cls, start: "Month", end: "Month") -> list[Self]:
        result = []
        current = start
        while current <= end:
            result.append(current)
            current = current + 1
        return result

    @cached_property
    def polish_name(self) -> str:
        return {
            1: "styczeń",
            2: "luty",
            3: "marzec",
            4: "kwiecień",
            5: "maj",
            6: "czerwiec",
            7: "lipiec",
            8: "sierpień",
            9: "wrzesień",
            10: "październik",
            11: "listopad",
            12: "grudzień",
        }[self.month]

    @cached_property
    def first_day(self) -> date:
        return date(self.year, self.month, 1)

    @cached_property
    def last_day(self) -> date:
        if self.month == 12:
            next_month = 1
            next_year = self.year + 1
        else:
            next_month = self.month + 1
            next_year = self.year
        return date(next_year, next_month, 1) - timedelta(days=1)

    def __add__(self, num_months: int) -> Self:
        total_months = self.year * 12 + (self.month - 1) + num_months
        new_year = total_months // 12
        new_month = (total_months % 12) + 1
        return type(self)(new_year, new_month)

    def __sub__(self, num_months: int) -> Self:
        return self + -num_months

    def __lt__(self, other: "Month") -> bool:
        return (self.year, self.month) < (other.year, other.month)

    def __le__(self, other: "Month") -> bool:
        return (self.year, self.month) <= (other.year, other.month)

    def __gt__(self, other: "Month") -> bool:
        return (self.year, self.month) > (other.year, other.month)

    def __ge__(self, other: "Month") -> bool:
        return (self.year, self.month) >= (other.year, other.month)
