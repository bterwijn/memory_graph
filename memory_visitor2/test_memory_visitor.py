from Memory_Visitor import Memory_Visitor

import config_default
import test

if __name__ == '__main__':
    def test_fun(data):
        visitor = Memory_Visitor()
        visitor.visit(data)
    test.test_all(test_fun)
