def main():
    a_str = "abc"
    字符串a = "abc"

    print(字符串a)

    列表a = [1, 2, 3]

    字典a = {"a": 1, "b": 2}
    字典b = dict(a=1, b=2)


class MyList(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, index):
        print("getitem")
        return super().__getitem__(index)

    def __setitem__(self, index, value):
        print("setitem")
        return super().__setitem__(index, value)

    def __delitem__(self, index):
        print("delitem")
        return super().__delitem__(index)


if __name__ == "__main__":
    # python 中一切皆是对象

    # 任何一个对象都有类型

    # 字符串的常用方法

    main()
