import argparse
import sys
import re
from collections import deque

def output(line):
    print(line)

def check_second(line, line_num=False, match=True):
    if line_num and match:          output(str(line_num) + ':' + line)
    elif line_num and not match:    output(str(line_num) + '-' + line)
    else:                           output(line)

def check_first(lines, pattern, invert=False, line_number=False):
    count = 0
    for line in lines:
        count += 1
        if bool(pattern.search(line.rstrip())) != invert:
            check_second(line, count if line_number else False)

def just_context(lines, pattern, before, after, invert=False, line_number=False):
    count = 0
    out = 0
    deq = deque(maxlen=before)

    for line in lines:
        count += 1

        if bool(pattern.search(line.rstrip())) != invert:
            out = after
            while deq:
                work = deq.popleft()
                check_second(work[0], work[1] if line_number else False, False)
            check_second(line, count if line_number else False)
        elif out:
            check_second(line, count if line_number else False, False)
            out -= 1
        else:
            deq.append((line, count))

def count(lines, pattern, invert=False):
    c = 0
    for line in lines:
        if bool(pattern.search(line.rstrip())) != invert:
            c += 1
    return str(c)

def grep(lines, params):
    params.pattern = params.pattern.replace('.', '\\.').replace('*', '.*').replace('?', '.')
    params.pattern = re.compile(params.pattern, re.I if params.ignore_case else 0)
    if params.count:
        output(count(lines, params.pattern, params.invert))
    elif params.context or params.after_context or params.before_context:
        before = max(params.before_context, params.context)
        after = max(params.after_context, params.context)
        just_context(lines, params.pattern, before, after, params.invert, params.line_number)
    else:
        check_first(lines, params.pattern, params.invert, params.line_number)

def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)
    

def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(), params)


if __name__ == '__main__':
    main()