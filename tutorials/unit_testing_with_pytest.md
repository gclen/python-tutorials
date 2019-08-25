## Testing your code with pytest

This guide is intended to give you a brief overview of why and how you should test your code. It is not meant to be a comprehensive overview (there are many great books and tutorials out there) but it should help you get started.  

### Why write tests?

When you are writing new code you want to check that your new code doesn't break any existing functionality. You might manually run some tests using an interpreter or Jupyter notebook. However, manually testing your code quickly becomes untenable as your codebase grows larger. What you need is a test suite that can be run automatically to ensure that you didn't break any functionality or introduce new bugs somewhere else. For example, this test suite could be run everytime you push your code to git, and notifying you if the tests fail. Having a robust test suite makes it easier to ship code quickly. 

### Some basic concepts

__Types of testing__

There are typically three broad categories of tests that you might have in your test suite:

1. Unit tests. These test individual components (such as a function) and check that the components produce the correct output, raise expected errors if given invalid input etc. These are relatively easy to create and automate.  
2. Integration tests. This checks how the components fit together (e.g. pulling data from a database). These are slightly harder to create/automate since multiple components need to be up and running (e.g. a database as well as your code).
3. End-to-end testing. These are more complicated tests which might involve a user performing multiple actions (such as logging in, viewing multiple web pages or purchasing something). These are very useful to have but are harder to maintain/automate. 

There are other kinds of testing that you can do such as performance testing ("how long does it take to run?") or stress testing ("what happens if I hammer the database?"). 

__Mocking__

You might be wondering how you write unit tests for code which interfaces with another component such as a database. You can create "mock" instances of those components (this process is called mocking) which will return the expected results. 

__Code coverage__

As you might expect, code coverage refers to the amount of code that is covered by unit tests. In theory you should have 100% coverage but you will see diminishing returns for the amount of work required to create all of those tests. In practice you should shoot for 70%-80%. Code coverage measures how much of your code is covered by tests, but it does not measure the quality of those tests. I recommend having fewer high quality tests than aiming for 100% coverage with less meaningful tests. 


### Choosing a testing framework

Python has a testing module (unittest) as part of the standard library which is based on the Java testing framework JUnit. I find it cumbersome to use since in order to create a test you need to define a class that subclasses from unittest.TestCase. There is not a lot of functionality built into this module which leads to a lot of boilerplate code.

I would recommend using another testing framework such as pytest (my preferred choice) or nose. Pytest and nose are fairly similar but pytest is more widely used and better supported. In contrast to unittest, tests in pytest are just python functions. There are also many plugins (>500) available to integrate with other frameworks (such as Flask). Pytest also will run unittest test cases without a problem so you don't need to write your existing test suite from scratch if you have one.

As you might have guessed from the title, I will be focusing on pytest for the rest of this tutorial.

### Getting started with pytest

To install pytest run

```
pip install pytest
```

or

```
conda install pytest
```

### Writing your first test

Pytest will look for all files of the form test_*.py or *_test.py in the current directory and all subdirectories.

Let's create a file named first_test.py

```python
# first_test.py
def say_hello(name):
    return 'Hello {}!'.format(name)

def test_say_hello():
    assert say_hello('Alice') == 'Hello Alice!'
```

When we run pytest

```bash
$ pytest
```

we should get the following output:

```
$ pytest
==================================== test session starts =====================================
platform linux -- Python 3.7.4, pytest-5.0.1, py-1.8.0, pluggy-0.12.0
rootdir: /home/gclenden/git/python-tutorials/examples/pytest-example
collected 1 item                                                                             

first_test.py .                                                                        [100%]

================================== 1 passed in 0.02 seconds ==================================
```

Of course you do not need to define the say_hello function in the same file as your test. See the creating a test suite for your module section below.

### Catching errors

You can also test that a function raises an error when given invalid input. For example you can check that the divide_numbers function raises the proper exception when dividing by zero.


```python
# test_raise_error.py
import pytest

def divide_numbers(a,b):
    return a/b

def test_divide_numbers():
    assert divide_numbers(10, 2) == 5

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide_numbers(1, 0)
```

### Using fixtures

Test fixtures are used to set up components with all the necessary code to initialize the object. This means you can instantiate other components of your codebase (or mocked versions of them) and pass them to your tests. 
Pytest makes creating fixtures super easy since you just need to add the @pytest.fixture decorator.

```python
# test_fixtures.py
import pytest

class ExampleDatabase:

    def __init__(self, name):
        self.name = name
        self.num_rows = 0

    def add_rows(self, data):
        self.num_rows += len(data)

@pytest.fixture
def db_connection():
    return ExampleDatabase('example_db')

def test_table_name(db_connection):
    assert db_connection.name == 'example_db'

def test_add_rows(db_connection):
    # DB should be empty
    assert db_connection.num_rows == 0
    # Try adding some data
    data = ['foo', 'bar', 'baz']
    db_connection.add_rows(data)
    # There should be 3 rows
    assert db_connection.num_rows == 3
```

### Creating a test suite for your module

I've created an [example module](../examples/pytest-example/) called mymodule with the unit tests above so you can see the structure of a module with tests. Make sure that you install the module

```
pip install -e <path to the module>)
```

so that your tests are able to import the functions appropriately. The first example above would now be

```python
from mypackage import say_hello

def test_say_hello():
    assert say_hello('Alice') == 'Hello Alice!'
```

If you want to learn more about packaging code and creating modules, see my tutorial on [python packaging](packaging.md).

### Determining code coverage

To calculate code coverage you can use the pytest-cov package

```
pip install pytest-cov
```

In the root directory of mypackage run

```
pytest --cov=mypackage tests/
```

which will output the report below

```
==================================== test session starts =====================================
platform linux -- Python 3.7.4, pytest-5.0.1, py-1.8.0, pluggy-0.12.0
rootdir: /home/gclenden/git/python-tutorials/examples/pytest-example/mypackage
plugins: cov-2.7.1
collected 5 items                                                                            

tests/first_test.py .                                                                  [ 20%]
tests/test_fixtures.py ..                                                              [ 60%]
tests/test_raise_error.py ..                                                           [100%]

----------- coverage: platform linux, python 3.7.4-final-0 -----------
Name                    Stmts   Miss  Cover
-------------------------------------------
mypackage/__init__.py       1      0   100%
mypackage/main.py          10      0   100%
-------------------------------------------
TOTAL                      11      0   100%


================================== 5 passed in 0.04 seconds ==================================

```

### Other resources

- [Pytest getting started guide](http://doc.pytest.org/en/latest/getting-started.html)
- [More on fixtures](https://docs.pytest.org/en/latest/fixture.html)

### Conclusions

Having an automated test suite for your code becomes necessary as your codebase grows larger. Pytest is an extremely powerful tool and I've barely scratched the surface of its functionality. 

