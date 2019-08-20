## Installing Anaconda

To install Anaconda download the latest install script for your
operating system and python version of choice from [here](https://www.anaconda.com/distribution/).
There will be a couple of prompts. Just follow them and you will have
anaconda installed!

**Caveat: The rest of these instructions have only been tested on Linux
but I\'m sure there are similar instructions for Windows**

Make sure if you choose to prepend Anaconda into your .bashrc that you
either open a new terminal or run:

```bash
source ~/.bashrc
```

### Conda vs virtualenv (or virtualenvwrapper)

Conda environments are similar to [virtual environments](virtualenvs.md)  but have a few key differences:

-   Conda environments are more isolated than virtualenvs since they
    don\'t symlink to system python. This makes them much more portable.
-   Installing packages with C code can be much faster in conda since
    the C code is precompiled. For example \"conda install pandas\" will
    be much faster than \"pip install pandas\"
-   You can still pip install into conda environments and it (usually)
    just works. Unfortunately you can\'t conda install into virtualenvs.
-   It is generally much easier to copy a conda environment (due to the
    isolation) than a virtualenv. Copying a virtualenv requires listing
    all of the packages installed and the reinstalling them.

### How do I actually use conda environments?

To create a conda environment called foo with pandas and
jupyter-notebook installed run:

```bash
conda create -n foo pandas notebook
```

To switch into the environment

```bash
conda activate foo
```

This will modify your prompt to let you know what environment you are in

```bash
(foo) $
```

You can install additional packages into the environment via conda or
pip

```bash
(foo) $ conda install matplotlib
(foo) $ pip install cyberspacy
```

To get out of an environment run:

```
(foo) $ conda deactivate
```

List all of your environments

```bash
conda info --envs
```

Create an environment with a specific version of python

```bash
conda create -n myenv_py35 python=3.5 pandas
```

Adding an environment as a Jupyter notebook kernel:

```bash
# Create an environment
conda create -n my_env <some packages> ipykernel
source activate my_env
# Add the kernel for your own user space
python -m ipykernel install --user --name my_env --display-name "Some useful name"
```

If you want to see the full list of conda commands check out the [documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
