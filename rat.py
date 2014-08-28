#!/usr/bin/env python
import sys
import imp
import os
import re

from collections import defaultdict
import argparse
import signal
import pprint

modulesDir = "modules"

# Note: your module names shouldn't conflict with built-in Python
#       module names.  e.g. don't name a module "os" or "sys" or "signal"
reportModules = ["ver", "sig", "swe", "bits", "hz", "mods", "mem",
                 "rdb", "kernel", "poller", "alloc", "stacktrace",
                 "ufork", "poll", "aof", "activity", "repl",
                 "cluster", "loading", "cmds"]

# Use Python's internal signal map to generate a Number<->Name map
SIGNAL_NAME = dict((getattr(signal, n), n) \
    for n in dir(signal) if n.startswith('SIG') and '_' not in n )

def loadModules(modsdir):
    loaded = []
    for mod in reportModules:
        try:
            loaded.append(__import__(mod.split(".")[0]))
        except ImportError:
            print "Missing expected module:", mod
        except:
            print "%s:" % mod, sys.exc_info()[0]
    return loaded

def parseInput(fd):
    # Skip over any non-INFO or non-report output at beginning of our input.
    startRegex = r"^(# |===)"
    if isinstance(fd, list):
        prev = fd
        line = fd[0]
        while not re.match(startRegex, line):
            prev = fd
            fd = fd[1:]
            line = fd[0]
        fd = prev
    elif isinstance(fd, file):
        prev = fd.tell()
        line = fd.readline()
        while not re.match(startRegex, line):
            prev = fd.tell()
            line = fd.readline()
        # We need to rewind the FD back to the found
        # line so it can iterate properly.
        fd.seek(prev)

    if re.match(r"^=== REDIS BUG REPORT START", line):
        print "Analyzing Redis Error Report..."
        return parseBugReport(fd)
    else:
        print "Analyzing Redis INFO Output..."
        return parseInfoOutput(fd)

def parseBugReport(fd):
    def cleanupLine(line):
        try:
            [before, after] = re.split(r"\d{3}\s#\s", line)
            return after
        except ValueError:
            return line

    flat = defaultdict(str)
    sections = defaultdict(dict)
    section = None
    offset = 0
    for line in fd:
        offset = offset + 1
        line = line.rstrip()
        if " --- " in line:
            if "INFO OUTPUT" in line:
                # When traversing a list, parseInfoOutput receives
                # the original list, but it needs to start at the
                # Into beginning offset.
                (iflat, isections) = parseInfoOutput(fd)
                # merge result dicts
                flat = defaultdict(str, iflat.items() + flat.items())
                sections = defaultdict(dict, isections.items() + sections.items())
                section = None
            elif "STACK TRACE" in line:
                section = "stackTrace"
                flat[section] = []
            elif "CLIENT LIST OUTPUT" in line:
                section = "clientList"
                flat[section] = []
            elif "REGISTERS" in line:
                section = None
            elif "FAST MEMORY TEST" in line:
                section = "memtest"
                flat[section] = []
        elif "Guru Meditation" in line:
            [_, error] = re.split(r"Guru Meditation: ", line)
            flat["softwareError"] = error
        elif "crashed by signal" in line:
            [before, sig] = re.split(r"crashed by signal: ", line)
            sig = int(sig)
            flat["signal"] = sig
            try:
                [date, ver] = re.split(r"# +Redis +", before)
                flat['redis_version'] = ver[:-1]
            except:
                pass
            flat["signalName"] = SIGNAL_NAME[sig]
        elif "assertation:" in line and "no assertation" in line:
            [before, assertation] = re.split(r"Failed assertion: ", line)
            flat["assert"] = assertation
        elif section == "stackTrace":
            flat[section].append(line)
        elif section == "clientList":
            flat[section].append(cleanupLine(line))
        elif section == "memtest":
            if "PASSED" in line:
                flat[section + "Result"] = "passed quick memory check"
                section = None
            elif "MEMORY ERROR DETECTED" in line:
                flat[section + "Result"] = "memory error detected"
                section = None
            else:
                flat[section].append(line)
        elif "=== REDIS BUG REPORT END." in line:
            return (flat, sections)

    print "Warning: reached end of error report without an END marker."
    return (flat, sections)

def parseInfoOutput(fd):
    def num(s):
        if isinstance(s, list) or isinstance(s, dict):
            return s
        try:
            return int(s)
        except ValueError:
            try:
                return float(s)
            except ValueError:
                return s

    flat = defaultdict(str)
    sections = defaultdict(dict)
    # allowFlatAccess is only enabled after we hit the first
    # section header.  This prevents us from grabbing pasted
    # command lines as valid INFO output.
    allowFlatAccess = False
    for line in fd:
        line = line.rstrip()
        if not line:
            # If empty space between sections, skip.
            continue
        elif "# # Server" in line:
            # Process info output from a crash report
            allowFlatAccess = True
            sectionName = "Server"
            sections[sectionName] = {}
        elif line.startswith("#"):
            # If header, create new top level section
            allowFlatAccess = True
            [_, sectionName] = line.split("# ")
            sections[sectionName] = {}
#        elif re.match(r"\[?\d+\]?(:[MS])?", line): # found PID prefixes again
        elif "CLIENT LIST OUTPUT" in line:
            # We reached the end of INFO output in an error report
            break
        elif allowFlatAccess:
            try:
                [key, val] = line.split(":")
            except ValueError: # line didn't have proper split format
                continue # skip this iteration; maybe it gets better?
            # If value has multiple key/val pairs, split them out.
            multiVal = val.split(",")
            if len(multiVal) > 1:
                vals = {}
                for valEntry in multiVal:
                    split = valEntry.split("=")
                    if len(split) == 2:
                        [innerKey, innerVal] = split
                        vals[innerKey] = num(innerVal)
                    else:
                        vals[innerKey] += "; " + split[0]
                val = vals
            sections[sectionName][key] = num(val)
            flat[key] = num(val)
    return (flat, sections)

def processInput(fd, modules, mode):
    (flat, sections) = parseInput(fd)
    results = []
    for mod in modules:
#        print "Evaluating %s module..." % (mod.__name__)
        result = mod.run(flat, sections, mode)
        if result:
            results.append({mod.__name__: result})

    for result in results:
        pprint.pprint(result, width=120)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="rat: Redis Analysis Tool")
    parser.add_argument("name", help="filename or GitHub issue # to process")
    parser.add_argument("-m", "--mode", default="error",
                        help="Analysis mode: 'error' or 'info'")
    parser.add_argument("-g", "--github", action="store_true",
                        help="Use 'name' argument as GitHub issue number")
    args = parser.parse_args()

    if args.github:
        import json
        import requests
        r = requests.get("https://api.github.com/repos/antirez/redis/issues/" +
                args.name)
        apiResult = json.loads(r.text)
        fd = apiResult['body'].split("\r\n")
    else:
        if args.name == "-":
            fd = sys.stdin
        else:
            fd = open(args.name)

    mode = args.mode

    sys.path.append(modulesDir)
    useModules = loadModules(modulesDir)

    processInput(fd, useModules, mode)

