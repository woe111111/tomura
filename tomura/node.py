import asyncio

from tomura.utils import get_logger


class Node():

    def __init__(self, name, func,context={},data=None,):
        """

        :param name:  节点名称
        :param func:  执行函数
        :param data:  执行结果
        """
        self.logger = get_logger(name)
        self.context = context
        self.lock = asyncio.Lock()
        self.func = func
        self.name = name
        self.data = data
        self._childs = []
        self._parents = []

    def add_parent(self, parent):
        self._parents.append((parent))

    def add_child(self, child):
        self._childs.append(child)

    def __str__(self):
        return self.name

    async def __call__(self):
        """
            递归执行
        :return:
        """
        async with self.lock:
            try:
                if self.func is not None and self.data is None:
                    self.data = await self.func(
                        *await asyncio.gather(*[asyncio.create_task(parent()) for parent in self._parents]))
                return (self)
            except Exception as e:
                raise e
            finally:
                self.logger.debug("node call", data=repr(self.data))

    def clear(self):
        self.data = None


if __name__ == '__main__':
    async def node0(ddd):
        print(ddd)


    async def node1(*xxx):
        print(3333)
        print(xxx)


    node0 = Node("root", node0, data=222)

    node22 = Node("root", node0, data=44)

    node = Node("test", node1)
    node.add_parent(node0)
    node.add_parent(node22)

    asyncio.run(node())
