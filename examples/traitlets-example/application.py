import os

from traitlets.config.application import Application
from traitlets import Bool, Unicode, validate, TraitError

try:
    raw_input
except NameError:
    # py3
    raw_input = input

class NoStart(Exception):
    """Exception to raise when an application shouldn't start"""

# These can be specified from the command line
# E.g. --foo=<value>
# Their documentation will be taken from their help string
base_aliases = {
    'fruit': 'MyApp.fruit',
    'config-file': 'MyApp.config_file',
    }

# These are flags that set a particular value if specified
base_flags = {'generate-config': ({'MyApp': {'generate_config': True}}, "Generate default config file")}


class MyApp(Application):

    name = 'myapp'
    description = 'An example traitlet application'

    aliases = base_aliases
    flags = base_flags

    # Useful traits
    generate_config = Bool(False, config=True, help="""Generate default config file.""")
    config_file = Unicode(config=True, help="""Full path to a config file.""")

    @validate('config_file')
    def _validate_config_file(self, proposal):
        value = proposal['value']

        if value == '':
            return value

        if os.path.isfile(value):
            return value
        else:
            raise TraitError('Config file {} does not exist'.format(value))

    # MyApp specific traits
    fruit = Unicode(u'', config=True, help="""The name of a fruit. Options are 'apple', 'banana', or 'watermelon'.""")

    # Traitlets makes it very easy to do dynamic validation
    @validate('fruit')
    def _validate_fruit(self, proposal):
        value = proposal['value']

        valid_fruits = ['apple', 'banana', 'watermelon']

        if value in valid_fruits:
            return value
        else:
            raise TraitError(
                'Fruit {} is not in the list of valid fruits {}'.format(value, valid_fruits))

    # These are some useful functions that you may want to use
    def write_default_config(self):
        """Write our default config to a .py config file"""
        if self.config_file:
            config_file = self.config_file
        else:
            config_file = os.path.join(os.getcwd(), self._config_file_name_default())

        if os.path.exists(config_file):
            answer = ''

            def ask():
                prompt = "Overwrite %s with default config? [y/N]" % config_file
                try:
                    return raw_input(prompt).lower() or 'n'
                except KeyboardInterrupt:
                    print('')  # empty line
                    return 'n'

            answer = ask()
            while not answer.startswith(('y', 'n')):
                print("Please answer 'yes' or 'no'")
                answer = ask()
            if answer.startswith('n'):
                return

        config_text = self.generate_config_file()
        if isinstance(config_text, bytes):
            config_text = config_text.decode('utf8')
        print("Writing default config to: %s" % config_file)
        if os.path.isdir(os.path.dirname(config_file)):
            with open(config_file, mode='w') as f:
                f.write(config_text)

    def _config_file_name_default(self):
        if not self.name:
            return ''
        return self.name.replace('-', '_') + u'_config.py'

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

if __name__ == '__main__':
    app = MyApp(
    app.launch_instance()













