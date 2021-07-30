import sys
out = "0"
if sys.argv[1] == "chip_mode":
    for idx in range(2, len(sys.argv)):
        if "." in sys.argv[idx]:
            out=sys.argv[idx].split(".")[-1]
    sys.exit(out)
elif sys.argv[1] == "branch_mode":
    for idx in range(2, len(sys.argv)):
        if "@" in sys.argv[idx]:
            out=sys.argv[idx]
    sys.exit(out)
else:
    for idx in range(2, len(sys.argv)):
        if sys.argv[1] in sys.argv[idx]:
            out = "1"
    sys.exit(out)
