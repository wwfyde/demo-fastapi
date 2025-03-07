class Solution:
    def __init__(self, nums: list[int]):
        self.nums = nums

    # 实例方法
    def print(self, target: int = None) -> int:
        print(self.nums)

        return target

    # 类方法
    @classmethod
    def pick(cls, target: int = None) -> int:
        print(target)
        return target

    # 静态方法
    def pick2(self, target: int = None) -> int:
        print(self.nums)
        print(target)
        return target


def pick(target: int = None) -> int:
    return 1


# 入口
def main():
    s = Solution([1, 2, 3, 3, 3])
    Solution.pick(22)
    s.pick(33)
    print(dir(Solution))

    # s.pick()
    print(s.print())

    for i in range(10):
        for j in range(10):
            print(i, j)
    pick()


def load_data(path: str):
    with open(path, "r") as f:
        data = f.read()
        return data


print(__name__)


if __name__ == "__main__":
    # 把 当前文件 脚本执行
    main()
