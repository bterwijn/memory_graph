
class My_Class:

    # class variables:
    count = 0
    unique_value = 0

    def __init__(self):
        print("__init__ called, initialize instance variables of object")
        self.my_instance_variable = []  # create instance variable
        My_Class.count += 1  # also change class variable

    def my_instance_method(self):
        print("my_instance_method called, access to instance variables via 'self'")
        self.my_instance_variable.append(My_Class.unique_value)
        My_Class.unique_value += 1  # also change class variable

    @classmethod
    def my_class_method(cls):
        print("my_class_method called, access to class variables via 'cls', no instance variables")
        print(f"{cls.count=}")

    @staticmethod
    def my_static_method():
        print("my_static_method called, no 'self' or 'cls'")
        print(f"{My_Class.count=}")  # but still access to class variables

obj1 = My_Class()
obj2 = My_Class()

obj1.my_instance_method()
obj1.my_class_method()
obj1.my_static_method()

for _ in range(2):
    obj1.my_instance_method()
    obj2.my_instance_method()

print(f"{obj1.count=}")     # reading class variable if no instance variable found
obj1.count = 100            # creating instance variable
print(f"{obj1.count=}")     # now finding and reading instance variable
print(f"{My_Class.count}")  # class variable still available via class name
print(f"{obj2.count=}")     # obj2 still reads the class variable
