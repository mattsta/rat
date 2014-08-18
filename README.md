# rat: Redis Analysis Tool

## Why
The goal of rat is to have a reasonably automatic way to find
"strange" things with Redis error reports and Redis `INFO` output without
needing to read all 100+ lines yourself to figure out what *could* be wrong.

rat parses an error report or info output, runs analysis modules,
then shows results from the analysis modules.

Analysis modules are allowed to make both objective and subjective
judgements about the input to help you figure out what may be wrong,
misbehaving, or just strange.

Modules should equally check for correct server behavior as well
as checking for anomalous usage behavior.

## Usage

### Quick Start

#### Use error report or `INFO` output from local file
```haskell
./rat.py error-report.txt
```

#### Use error report from GitHub issue
```haskell
./rat.py -g 1818
```

#### Example Output
```javascript
% ./rat.py -g 1818
Analyzing Redis Error Report...
{'ver': {'status': 'OK', 'version': '2.8.4'}}
{'sig': {'crashed because': 'memory access error', 'killed by': (11, 'SIGSEGV')}}
{'mem': {'memory usage': '20.99 GB', 'size': 'large', 'using non-jemalloc allocator': 'libc'}}
{'rdb': {'changes not written yet': '11,467',
         'current save duration': '1 second ago',
         'currently saving': True,
         'last save duration': '2 minutes, 51 seconds ago'}}
{'kernel': {'non-standard system': 'FreeBSD 10.0-RELEASE amd64'}}
{'stacktrace': ['0x4372e9 <???> at /usr/local/bin/redis-server',
                '0x800cd93f6 <_swapcontext+0x146> at /lib/libthr.so.3',
                '0x800cd8ff3 <sigaction+0x343> at /lib/libthr.so.3']}
{'ufork': {'fork time very large': '0.1234 seconds'}}
{'activity': {'average commands per second': 162, 'total commands processed': '795,044,463'}}
{'cmds': {'BAD USAGE': {'KEYS command used': '1,563,983 times'},
          'sorted by calls': [{'get': '414,014,012 times'},
                              {'hgetall': '248,403,559 times'},
                              {'zadd': '77,393,992 times'},
                              {'hmset': '48,903,265 times'},
                              {'zrangebyscore': '3,763,011 times'},
                              {'keys': '1,563,983 times'},
                              {'zremrangebyscore': '994,818 times'},
                              {'del': '6,859 times'},
                              {'set': '786 times'},
                              {'expire': '155 times'},
                              {'select': '13 times'},
                              {'info': '6 times'},
                              {'config': '2 times'},
                              {'dump': '2 times'}],
          'sorted by duration': [{'zrangebyscore': {'runtime': '43.3%', 'total': '6 hours, 47 minutes, 9 seconds'}},
                                 {'zadd': {'runtime': '27.6%', 'total': '4 hours, 19 minutes, 35 seconds'}},
                                 {'hgetall': {'runtime': '11.2%', 'total': '1 hour, 45 minutes, 25 seconds'}},
                                 {'zremrangebyscore': {'runtime': '6.6%', 'total': '1 hour, 2 minutes, 32 seconds'}},
                                 {'keys': {'runtime': '5.3%', 'total': '49 minutes, 38 seconds'}},
                                 {'hmset': {'runtime': '3.9%', 'total': '36 minutes, 54 seconds'}},
                                 {'get': {'runtime': '2.0%', 'total': '19 minutes, 3 seconds'}},
                                 {'del': {'runtime': '0.1%', 'total': '33 seconds, 356 ms, 550 us'}},
                                 {'set': {'runtime': '0.0%', 'total': '3 seconds, 600 ms, 121 us'}},
                                 {'info': {'runtime': '0.0%', 'total': '68 ms, 121 us'}},
                                 {'config': {'runtime': '0.0%', 'total': '33 ms, 368 us'}},
                                 {'expire': {'runtime': '0.0%', 'total': '2 ms, 359 us'}},
                                 {'select': {'runtime': '0.0%', 'total': '71 us'}},
                                 {'dump': {'runtime': '0.0%', 'total': '12 us'}}]}}
```

### Usage Help

```haskell
usage: rat.py [-h] [-m MODE] [-g] name

rat: Redis Analysis Tool

positional arguments:
  name                  filename or GitHub issue # to process

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  Analysis mode: 'error' or 'info'
  -g, --github          Use 'name' argument as GitHub issue number
```

## Extending
Analysis modules live in the `modules` directory.

### The Function
The module callback function is: `run(flat, sections, mode)`

#### Parameters
`flat` is a dictionary of every field in one flat namespace.

`sections` is a dictionary of dictionaries, where the key to the
second level dictionary is every section name.

`flat` and `sections` have the same data, except with `sections`,
you can do `sections["Server"]` to return all `"Server"`
fields at once.

`mode` is either "info" or "error".  You can check the mode to
run more or less verbose processing depending on expectations.

#### Return Value
The return value of `run()` will be shown to the user in a dictionary
with the key of the module name.

Example: the return value of `3` from `run()` in module `thing.py` will be
returned to the user as `{'thing': 3}`.  For easier reading, you can
return dictionaries like `{"has bad memory": True}` so the user will
see: `{'thing': {"has bad memory": True}}`.

If the `run()` function returns a Falsy value (`None`, `False`, empty containers)
then the module is omitted from results.


## Contributions
Our goal here is to create automated tools allowing us to quickly find odd
conditions observable through Redis health output.

Add new modules to rat by:

  - create a module (or modify an existing module)
  - add your module to the `reportModules` list
  - check the output of your module against the sample files in `examples/` by running `./run-examples.sh`
  - maybe add your own test cases to `examples/`
  - open a pull request to get your module officially added
