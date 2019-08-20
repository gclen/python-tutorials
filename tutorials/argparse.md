Just a basic example of how you can enable command line arguments in
your python script

```python
import argparse
from datetime import datetime, timedelta


parser = argparse.ArgumentParser(description='Description of your program', add_help=True)

# Instead of strings you can convert the variables type using the type argument
parser.add_argument('--threshold', '-t', help='An example int variable Default is 3', default=3, type=int)

# Creating variables to be used as defaults
default_start = datetime.utcnow() - timedelta(hours=12)
default_end = datetime.utcnow()

parser.add_argument('--start', '-s', default=default_start, help='Start date/time to query (default: 12 hours ago)')
parser.add_argument('--end', '-e', default=default_end, help='End date/time to query (default: now)')
parser.add_argument('--url', '-u', help='An example string', default='')
# Required arguments example
parser.add_argument('--cert', '-c', default=None, help='Path to PKI certificate file', required=True)
parser.add_argument('--key', '-k', default=None, help='Path to PKI key file', required=True)

# Actually parse the arguments
args = parser.parse_args()

# You can access the arguments using their full name
creds = (args.cert, args.key)
threshold = args.threshold

```

You can also do validation of the values passed in by using the type
parameter and custom functions

```python
def valid_mode(value):
    if value.lower() not in ['foo', 'bar']:
        raise argparse.ArgumentError('Mode must be one of foo or bar')
    return value

# You can do validation of the input using the type argument and a custom function
parser.add_argument('--mode', '-m', help='Which mode to use. Options are foo or bar', type=valid_mode)
```

If you run your script with the -h flag it will display all of your help
strings (as expected)

```
$ python argparse_example.py -h

usage: argparse_example.py [-h] [--threshold THRESHOLD] [--start START]
                           [--end END] [--url URL] --cert CERT --key KEY
                           [--mode MODE]

Description of your program

optional arguments:
  -h, --help            show this help message and exit
  --threshold THRESHOLD, -t THRESHOLD
                        An example int variable Default is 3
  --start START, -s START
                        Start date/time to query (default: 12 hours ago)
  --end END, -e END     End date/time to query (default: now)
  --url URL, -u URL     An example string
  --cert CERT, -c CERT  Path to PKI certificate file
  --key KEY, -k KEY     Path to PKI key file
  --mode MODE, -m MODE  Which mode to use. Options are foo or bar
```
