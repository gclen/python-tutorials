## Creating and using virtual environments

### Why should I use virtual environments?

There are two main benefits: the ability to install python packages on a machine that you don\'t have
sudo access on, and being able to have multiple versions of a dependency
on your system. If you have a piece of code that depends on an older
version of a package (and may break if the dependency is upgraded) but
the newer version has some sweet new features then virtual environments
can help. You can also test if your code will break when upgrading the
dependencies. Additionally, if you are developing a package that will be
used by other people you can start from a fresh environment to see all
of the dependencies (e.g. you may have already installed some package
that other users haven\'t). With this in mind here is a quick tutorial
on python virtual environments.

### Getting setup

To get the full benefit of virtual environments I strongly recommend
that you have pip installed. You
will want to install both virtualenv and virtualenvwrapper if they are
not already installed:

```bash
pip install virtualenv
pip install virtualenvwrapper
mkdir ~/.virtualenvs
# You'll want to add these to your ~/.bashrc
export WORKON_HOME=~/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```

### Using virtualenvwrapper

The following commands assume that you have installed virtualenvwrapper.
While not required it makes it significantly easier to create and manage
multiple virtual environments. To create a virtual environment run:

```bash
mkvirtualenv <name>
```

This will create a virtual environment foo with only pip and setuptools
installed. If you would like to create a virtualenv with all the
packages that are normally installed on your system run:

```bash
mkvirtualenv --system-site-packages <name>
```

To remove a virtual environment run:

```bash
rmvirtualenv <name>
```

To work in a virtual environment use the workon command:

```bash
workon <name>
```

You will know when a virtual environment is active because the name of
the virtualenv will be shown in the prompt. For example:

```bash
user@hostname $
user@hostname $ workon foo
(foo) user@hostname $
```

To exit a virtual environment just use deactivate:

``` bash
deactivate
```

To switch between two environments you don\'t need to deactivate the
first one. Workon will do the work for you:

``` bash
(foo)sid@hostname $ workon bar
(bar)sid@hostname $
```

When you are in a virtual environment you can use pip like you normally
would:

```
(foo)sid@hostname $ pip install pandas
```

If you are writing scripts don\'t forget to change the shebang to the
python interpreter in your local virtualenv. If you are developing a
package and don\'t want to keep reinstalling it as you make changes run

```bash
(foo)sid@hostname $ pip install -e /path/to/package
```

This makes a symlink in the site-packages of the virtualenv. If it
doesn\'t seem to recognize your changes, check that it works in a python
interpreter. It may be an issue with the shebang.

If you want to use python3 in your virtualenv on Ubuntu (which defaults
to python2) use:

```bash
mkvirtualenv --python=`which python3` <name of environment>
```

All other virtualenvwrapper functions should behave in the same way.
