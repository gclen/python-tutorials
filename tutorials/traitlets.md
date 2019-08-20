### Using traitlets for configuration

### What is traitlets?

Trailets is a package created by the Jupyter development team that is
used to make configuration easier. I find it is useful for larger
projects where sys.argv and argparge become unwieldy. It is also
extremely useful if you want to have configuration files as well as
command line options. To install it just run

```bash
pip install traitlets
```

### Why should I use traitlets?

-   Type enforcement (if you declare a variable to be an integer it will
    throw an error if it is not)
-   Default values for traits can be dynamically computed
-   Easy input validation
-   Hierarchical configuration: command line arguments will override
    what is specified in a config file
-   Logging is easy to set up and is configurable
-   Documentation are the same in generated config files or at the
    command line

While there is some boiler plate code involved it is **much** easier
than trying to set this up yourself. I\'ve had projects where I am
trying to do input validation with class properties, and configuration
with JSON files and it ends up being a big mess.

### A basic example

The full code for this example is in the [examples directory](../examples/traitlets-example) 
but I\'ll highlight some key aspects below. In this example I have a
class for configuration (MyApp) and a class which will take a
configuration and do something useful with it. Defining and validating a
trait is pretty easy:

```python
import os

from traitlets.config.application import Application
from traitlets import Bool, Unicode, validate, TraitError

class MyApp(Application):

    name = 'myapp'
    description = 'An example traitlet application'

    config_file = Unicode(u'', config=True, help="""Full path to a config file.""")
    generate_config = Bool(False, config=True, help="""Generate default config file.""")

    @validate('config_file')
    def _validate_config_file(self, proposal):

        value = proposal['value']
        if value == '':
            return value
        # Check that the file actually exists
        if os.path.isfile():
            return value
        else:
            raise TraitError('Config file {} does not exist'.format(value))

    # This is a trait for MyApp
    fruit = Unicode(u'', config=True, help="""The name of a fruit. Options are 'apple', 'banana', or 'watermelon'.""")
    # Validation of fruit goes here
```

Let\'s break this down a little bit:

-   MyApp inherits from Application which provides a lot of the
    functionality
-   There are a couple of traits imported: Bool and Unicode. There are
    many more trait types that can be used
-   Validation is pretty easy and TraitErrors should be raised if
    validation fails
-   Defining a trait allows you to specify a default value (e.g. False).
    The config parameter indicates whether it can be overridden by a
    config or command line argument. The help string is displayed in a
    generated config file or on the command line when the -h flag is
    specified.

Traitlets lets you define aliases and flags for command line use.
Aliases allow you to access a trait:

```bash
python application.py --fruit="apple"
```

When specified flags set a trait to a particular value (e.g. True or
False)

```bash
python application.py --generate-config
```

Defining the aliases and flags is as simple as creating a dictionary

``` python
base_aliases = {
    'fruit': 'MyApp.fruit',
    'config-file': 'MyApp.config_file',
    }

base_flags = {'generate-config': ({'MyApp': {'generate_config': True}}, "Generate default config file")}
```

With this enabled running

```bash
python application.py -h
```

yields

```
An example traitlet application

Options

\-\-\-\-\-\--

Arguments that take values are actually convenience aliases to full

Configurables, whose aliases are listed on the help line. For more
information

on full configurables, see \'\--help-all\'.

\--generate-config

Generate default config file

\--fruit=\<Unicode\> (MyApp.fruit)

Default: \'\'

The name of a fruit. Options are \'apple\', \'banana\', or
\'watermelon\'.

\--config-file=\<Unicode\> (MyApp.config\_file)

Default: \'\'

Full path to a config file.

To see all available configurables, use \`\--help-all\`
```

If config generation is set up (see the example in git for more details)
running

```bash
python application.py --generate-config
```

wlll generate a config file named myapp\_config.py. The contents of this
file are the available configurations with help strings. And since it is
a python file you can execute arbitrary code to generate values (e.g.
dates). You can also see there are options for logging configuration.

```
\# Configuration file for myapp.

\#\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

\# Application(SingletonConfigurable) configuration

\#\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

\#\# This is an application.

\#\# The date format used by logging formatters for %(asctime)s

\#c.Application.log\_datefmt = \'%Y-%m-%d %H:%M:%S\'

\#\# The Logging format template

\#c.Application.log\_format = \'\[%(name)s\]%(highlevel)s %(message)s\'

\#\# Set the log level by value or name.

\#c.Application.log\_level = 30

\#\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

\# MyApp(Application) configuration

\#\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

\#\# Full path to a config file.

\#c.MyApp.config\_file = \'\'

\#\# The name of a fruit. Options are \'apple\', \'banana\', or
\'watermelon\'.

\#c.MyApp.fruit = \'\'

\#\# Generate default config file.

\#c.MyApp.generate\_config = False
```

Let\'s define another class that will take our configuration object as
input and use it

```python
class Fruit(object):
    def __init__(self, conf):
        self.conf = conf

        print(self.conf.fruit)
```

To actually initialize our config we need to define a method in MyApp to
launch an instance

```python
def start(self):
    if self.generate_config:
        self.write_default_config()
        raise NoStart()

    if self.config_file:
        path, config_file_name = os.path.split(self.config_file)
        self.load_config_file(config_file_name, path=path)

    # Do some stuff with the valid config
    from fruit import Fruit
    # Should print the name of the fruit
    f = Fruit(self)

def launch_instance(cls, argv=None, **kwargs):
    """Launch an instance"""
    try:
        app = cls.instance(**kwargs)
        app.initialize(argv)
        app.start()
    except NoStart:
        return
```

You can see that when launch instance is called it will initialize and
then call start. In the start function the valid config is passed into
the Fruit class. To call launch\\\_instance just use

```python
app = MyApp()
app.launch_instance()
```

### Conclusions

Trailets is a very powerful and flexible framework. This is just a basic
example but there are many extensions that can be used. If you want to
actually use traitlets, I strongly recommend looking at the example in
the [examples directory](../examples/traitlets-example)
since there are more details fleshed out. And as always don\'t hesitate
to ask if you have any questions!
