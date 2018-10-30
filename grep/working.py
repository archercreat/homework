import argparse
import sys
import re

def output(line):
    print(line)

def ignore_output(lines, lowlines, pattern, invert):
    if invert:
        for i in range(len(lowlines)):
            if re.search(pattern, lowlines[i].rstrip()) is None:
                output(lines[i])
    else:
        for i in range(len(lowlines)):
            if re.search(pattern, lowlines[i].rstrip()):
                output(lines[i])

def normal_output(lines, pattern, invert):
    if invert:
        for line in lines:
            if re.search(pattern, line.rstrip()) is None:
                output(line)
    else:
        for line in lines:
            if re.search(pattern, line.rstrip()):
                output(line)

def tolow(lines, pattern):
    return list(map(str.lower, lines)), pattern.lower()

def clear_and_print(lines):
    while lines:
        try:    lines.remove("")
        except: break
    for line in lines:
        output(line)

def just_context(lines, pattern, context, after, before, line_numb):
    nlines = ["" for i in range(len(lines))]
    if context:
        choise = context
    elif after:
        choise = after
    elif before:
        choise = before
    after += 1
    before += 1
    if line_numb:
        for i in range(len(lines)):
            if re.search(pattern, lines[i].rstrip()):
                nlines[i] = str(lines.index(lines[i])+1) + ":" + lines[i]
                for c in range(choise+1):
                    if after != 1 or context != 0:
                        try:
                            if ":" not in nlines[i+c]:
                                nlines[i+c] = str(lines.index(lines[i+c])+1) + "-" + lines[i+c]
                            else: pass
                        except: pass
                    if before != 1 or context != 0:
                        try:
                            if ":" not in nlines[i-c]:
                                nlines[i-c] = str(lines.index(lines[i-c])+1) + "-" + lines[i-c]
                            else: pass
                        except: pass
    else:
        for i in range(len(lines)):
            if re.search(pattern, lines[i].rstrip()):
                nlines[i] = lines[i]
                for c in range(choise+1):
                    if after != 1 or context != 0:
                        try:
                            nlines[i+c] = lines[i+c]
                        except: pass
                    if before != 1 or context != 0:
                        try:
                            nlines[i-c] = lines[i-c]
                        except: pass
    clear_and_print(nlines)


# count elements that mach pattern
def count(lines, pattern):
    c = 0
    for line in lines:
        if re.search(pattern, line.rstrip()):
            c += 1
    return str(c)

# normal case if no context
def line_num(lines):
    return ([str(lines.index(lines[i])+1) + ":" + lines[i] for i in range(len(lines))])

def grep(lines, params):
    params.pattern = params.pattern.replace("?",".").replace("*", ".*?")

    if params.ignore_case:
        new_lines, params.pattern = tolow(lines, params.pattern)

    if params.line_number and not params.context:
        lines = line_num(lines)

    if params.context or params.after_context or params.before_context:
        just_context(lines, params.pattern, params.context, params.after_context, params.before_context, params.line_number)

    elif params.count:
        output(count(lines, params.pattern))

    else:
        if params.ignore_case:
            ignore_output(lines, new_lines, params.pattern, params.invert)
        else:
            normal_output(lines, params.pattern, params.invert)

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