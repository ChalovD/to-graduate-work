from abc import ABC
from typing import Generic, TypeVar

T = TypeVar('T')


class Solution(ABC, Generic[T]):
    def get_solution(self) -> T:
        pass
