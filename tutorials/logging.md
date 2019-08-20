## A (brief) overview of Python\'s logging module

I\'m sure everyone has a few scripts with commented out print statements
that they\'ve used for debugging, and other print statements to monitor
certain parameters. Proper logging is one of those things that you know
you should do but never get around to. Fortunately, pythons built-in
logging module is easy to use, robust, and has a lot of features. You
can specify different message levels and choose what level you want to
show in the logs. For example, you might want debug statements when
developing but want them turned off in production. This is as simple as
changing the level of the logger (which is way easier than commenting
out a bunch of print statements).

### Message levels

The logging module has five message levels. The default is to display
messages at WARNING and above.


| Logger method | Message level | Typical use case | 
| ------------- | ------------- | ---------------- |
| logger.debug() | DEBUG | When developing and you want to see the values of various parameters to diagnose problems |
| logger.info() | INFO | Confirm things are working as expected (especially in production) | 
| logger.warning() | WARNING | Note that something unexpected happened (e.g. an issue with a third party library) or something will happen in the future (e.g. disk space low) |
| logger.error() | ERROR | Log when an error has occurred (e.g. in a try-except statement) |
| logger.critical() | CRITICAL | Log a serious error that may cause the program to crash |

### Creating a logger

To create a logger and display messages at ERROR and above, you would
write:

```python
import logging

logger = logging.getLogger('logging_demo')
logger.setLevel(logging.ERROR) # display ERROR and above

logger.info('This will not be seen')
logger.error('This will show up in the logs')
```

To be clear, using print statements for a command line program is
perfectly adequate and is less of a pain than logging to stdout. The
primary benefits of the logging module are the variety of handlers and
formatting options which are detailed below. In the code snippet above I
called logging.getLogger(\'logging\_demo\'). This logger will be
globally available across all your modules in a directory (or in a
package). The configuration only needs to be done once. Just put a call
to logging.getLogger() at the top of each module that you want to do
logging and you will be good to go.

### Using handlers

The StreamHandler class is built in, but there are many other useful
handlers in logging.handlers:

| Handler class | Location | Description | 
| ------------- | -------- | ----------- | 
| StreamHandler | logging.StreamHandler | Stdout and stderr |
| FileHandler | logging.FileHandler | Write messages to files |
| RotatingFileHandler | logging.handlers.RotatingFileHandler | Write messages to files, with support for maximum file sizes and log file rotation |
| TimedRotatingFileHandler | logging.handlers.TimedRotatingFileHandler | Write messages to files while rotating log files at timed intervals |
| SMTPHandler | logging.handlers.SMTPHandler | Sends messages to designated email address |
| HTTPHandler | logging.handlers.HTTPHandler | Sends messages to HTTP server |


```python
# Using a file handler
import logging
from logging import FileHandler

logger = logging.getLogger('logging_demo')
logger.addHandler(FileHandler('mylog.log'))
logger.error('Some error')
```

### Formatting

| Format code | Description |
| ----------- | ----------- |  
| \%(asctime)s                      | Date and time as a string         |
| \%(levelname)s                    | Log level                         |
| \%(message)s                      | Log message                       |
| \%(funcName)s                     | Name of function that contains logging call |
| \%(module)s                       | Module name                       |
| \%(threadName)s                   | Thread name                       |

```python
# Configuring the logger format
import logging

logger = logging.getLogger('logging_demo')

log_format = '%(asctime)s | %(levelname)s | %(message)s'

handler = logging.FileHandler('mylog.log')
handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(handler)
```

### Configuration files

Typically logging configuration is not done within the a script but within a configuration file (such as logging.conf).

```python
# Using logging.conf

import logging
import logging.config
import logging.handlers

logging.config.fileConfig('logging.conf')
```

Here is an example of a logging.conf file

```conf
# The names of your loggers
# I recommmend having a root logger that it will fall back on
[loggers]
keys=root, my_logger

[handlers]
keys=console_handler, file_handler

[formatters]
keys=simple_formatter, file_formatter

[logger_root]
level = DEBUG
handlers = console_handler

[logger_my_logger]
level=DEBUG
handlers=file_handler
qualname=tb_logger

[handler_file_handler]
class=logging.FileHandler
level=DEBUG
formatter=file_formatter
args=('mylog.log', 'a')

[handler_console_handler]
class=StreamHandler
level=WARNING
formatter=simple_formatter
args=(sys.stdout,)

[formatter_simple_formatter]
format=%(levelname)s:%(message)s

[formatter_file_formatter]
format=%(asctime)s | %(module)s | %(levelname)s | %(message)s
datefmt='%Y-%m-%d %H:%M:%S'
```

### Tips and tricks

-   The logging.handlers and logging.config modules are not under the
    logging namespace (don\'t ask me why) so you will need to import
    them directly
-   If you are trying to use the same logger in multiple files (in the
    same directly) and things are not working properly check that you
    call the logger at the top of the file (not in the main function)
-   logging.exception() will print out the stack trace. Note that is
    should only be used in exception handling

### Other useful resources

* [The module documentation](https://docs.python.org/3/library/logging.html)
* [Logging cookbook](https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook)