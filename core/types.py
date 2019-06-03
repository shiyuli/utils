from typing import List, TypeVar, Generic, Iterator

T = TypeVar('T')

class Line(Generic[T]):
    raw: T

    def __init__(self, data: T):
        self.raw = data

    def replace(self, new: T) -> None:
        self.raw = new


class Lines(Generic[T]):
    raw: List[Line[T]]

    def __init__(self, data: List[T]) -> None:
        self.parse(data)

    def parse(self, raw: List[T]) -> None:
        self.raw = []
        for line in raw:
            self.raw.append(Line(line))

    def tolist(self) -> List[T]:
        output: List[T] = []
        for line in self.raw:
            output.append(line.raw)

        return output


class Stream:
    raw: Lines[str]
    filename: str

    def __init__(self, filename: str):
        self.filename = filename
        self.__load()

    def reset(self) -> None:
        self.__load()

    @property
    def size(self) -> int:
        return len(self.raw.raw)

    #
    # def get(self, index: int) -> Line[T]:
    #     if index >= self.size:
    #         return ''
    #     return self.__raw[index]
    #
    # def set(self, index: int, by: str) -> None:
    #     self.__raw[index] = by

    def save(self) -> None:
        with open(self.filename, 'w') as f:
            f.writelines(self.raw.tolist())

    def __load(self) -> None:
        with open(self.filename, 'r') as f:
            self.raw = Lines(f.readlines())
