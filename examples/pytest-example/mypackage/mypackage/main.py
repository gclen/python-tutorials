def say_hello(name):
    return 'Hello {}!'.format(name)

def divide_numbers(a,b):
    return a/b

class ExampleDatabase:

    def __init__(self, name):
        self.name = name
        self.num_rows = 0

    def add_rows(self, data):
        self.num_rows += len(data)
