from tomura.node import Node

import asyncio


class Graphics():

    def __init__(self):
        self.nodes = dict()
        self.context = dict()

    def add_node(self, name, func, parents: list = []):
        self.nodes[name] = Node(name, func=func, context=self.context)

        for parent in parents:
            self.nodes[parent].add_child(self.nodes[name])
            self.nodes[name].add_parent(self.nodes[parent])

    def get_leaf(self):
        for key, value in self.nodes.items():
            if value._childs == []:
                yield value

    def clear(self):
        for name, node in self.nodes.items():
            node.clear()

    async def run(self):
        leafs = list(self.get_leaf())
        return await asyncio.gather(*[asyncio.create_task(leaf()) for leaf in leafs])


if __name__ == '__main__':
    g = Graphics()


    async def test222(**kwargs):
        print(kwargs)
        return ""


    g.add_node(name="test", func=test222)

    asyncio.run(g.run())
