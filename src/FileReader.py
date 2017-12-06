"""
文件读取
从指定文件中读取源码内容
"""
class FileReader:
    """
    文件读取类——用于从指定的文件中读取源码
    """

    __result = None

    def __init__(self, filename=None):
        """

        :param filename: 文件名
        :raises: FileNotFindError
        """
        if filename is None:
            return
        else:
            try:
                with open(filename, 'r') as f:
                    self.__result = "".join(f.readlines())
            except FileNotFoundError as e:
                print(e)

    def get_result(self):
        """
        返回源码文本，如果未加载文件或未正确加载文件则返回一个空列表

        :rtype: list
        """
        if self.__result is None:
            return []
        else:
            return self.__result

    def fileload(self, filename):
        """
        加载指定文件

        :param filename: 文件路径
        :raise: FileNotFoundError
        """
        try:
            with open(filename, 'r') as f:
                self.__result = "".join(f.readlines())
        except FileNotFoundError as e:
            print(e)


if __name__ == '__main__':
    fr = FileReader('demo.txt')
    print(fr.get_result())
