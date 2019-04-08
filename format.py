
lines = ["l1","l2","\tl4","\t\tl5","\tl6"]
for line in lines:
    print(line)


output = ["l1","l2.l4.l5.l6"]
for l in output:
    print(l)


lineStack = [(0,lines[0])]

opStack = []
while(lineStack != [] or opStack != []):
    for line in lines[1:]:

        # count the tabs to get the indentation level
        indentCount = 0
        for c in line:
            if (c == '\t'):
                indentCount += 1
                continue
            break

        prevLine =