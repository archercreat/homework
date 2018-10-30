x = '?123'

print x.replace("?", ".").replace("*", ".*?")

x, y = 0, 0

print x, y

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
                nlines[i] = str(i+1) + ":" + lines[i]
                for c in range(choise+1):
                    if after != 1 or context != 0:
                        try:
                            if ":" not in nlines[i+c]:
                                nlines[i+c] = str(i+c+1) + "-" + lines[i+c]
                            else: pass
                        except: pass
                    if before != 1 or context != 0:
                        try:
                            if ":" not in nlines[i-c]:
                                nlines[i-c] = str(i-c+1) + "-" + lines[i-c]
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