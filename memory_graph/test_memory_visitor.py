from memory_graph.Memory_Visitor import Memory_Visitor

import  memory_graph.config_default as config_default
import memory_graph.test as test

if __name__ == '__main__':
    def test_fun(data):
        visitor = Memory_Visitor()
        visitor.visit(data)
    test.test_all(test_fun)
