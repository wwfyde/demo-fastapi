from dataclasses import dataclass
from enum import Enum


@dataclass
class Error:
    code: str
    name: str
    desc: str


class ErrorCode(Enum):
    USER_NOTFOUND = Error("A001", "USER_NOTFOUND", "用户未找到")

    def __str__(self):
        # 自定义字符串输出
        return f"[{self.value.code}] {self.value.name}: {self.value.desc}"

    @property
    def code(self):
        return self.value.code

    @property
    def name(self):
        return self.value.name

    @property
    def desc(self):
        return self.value.desc
