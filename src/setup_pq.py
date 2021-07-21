import os, sys, termios, tty, subprocess

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    print(ch)
    return ch
# setup file list
Setup_file=[]
Setup_file.append("build_configure.json")
Setup_file.append("build_exec")
Setup_file.append("build_ops")
Setup_file.append("build_utils.pyc")
Setup_file.append("pq-compiler.sh")

file_list = os.listdir('../')
for idx in range(len(file_list)):
    if idx == len(file_list)-1 :
        print "[%d : %s]\n"%(idx+1,file_list[idx]),
    else:
        print "[%d : %s],\t" % (idx + 1, file_list[idx]),
    if idx%4==3:
        print "\n",
print "Please, Select your build-starfish directory : ",
x = ord(getch()) # 48 = 0
selected = file_list[x-49]

for idx in range(len(Setup_file)):
    cmmd = "cp ./bin/%s ../%s/"%(Setup_file[idx],selected)
    subprocess.call(cmmd, shell=True)