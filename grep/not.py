
import argparse
import sys
import re
'''
1.ignore_case
2.context
3.before_context
4.after_context
5.line_num
6.invert
7.output

'''
def output(line):
    print(line)

def ignore_case(lines, pattern):
    for line in lines:
        if re.search(pattern, line.rstrip()) is None:
            output(line)

def normal_case(lines, pattern):
    for line in lines:
        if re.search(pattern, line.rstrip()):
            output(line)

def context(lines, pattern, context, line_num):
    nlines = [None for i in range(len(lines))]
    for i in range(len(lines)):
        if re.search(pattern, lines[i].rstrip()):
            nlines[i] = lines[i]
            for c in range(context+1):
                try: nlines[i+c] = lines[i+c] # if out of range
                except: pass
                try: nlines[i-c] = lines[i-c] # if out of range
                except: pass


def count(lst, pattern):
    c = 0
    for line in lst:
        if re.search(pattern, line.rstrip()):
            c += 1
    return str(c)

def change_pattern(pattern):
    if "?" in pattern:
        pattern = pattern.replace("?", ".")
    if "*" in pattern:
        pattern = pattern.replace("*", ".*?")
    return pattern

def line_num(lst):
    lst = [str(lst.index(lst[i])+1)+":"+lst[i] for i in range(len(lst))]
    return lst

def grep(lines, params):
    


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
