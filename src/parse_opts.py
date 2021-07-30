import sys

# mode decision
out = "0"
for idx in range(2, len(sys.argv)):
    if sys.argv[1] in sys.argv[idx]:
        out = "1"
sys.exit(out)
