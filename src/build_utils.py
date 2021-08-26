import os, subprocess, sys, tty, termios, json
from git import Repo

class pcolor:
    red='\033[0;31m'
    green='\033[0;32m'
    blue='\033[0;34m'
    cyan='\033[0;36m'
    gray='\033[0;37m'
    yellow='\033[1;33m'
    clear='\033[0m'

# getting command
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

# cmmd gen. ( background mode or not )
def proc_cmd(cmmd, debug, bg=0):
    if debug:
        print(cmmd)
    else:
        if bg=='1':
            if not os.path.exists("./build_logs"):
                os.mkdir("./build_logs")
            for idx in range(101):
                if not os.path.isfile('./build_logs/log_%d'%idx):
                    cmd = "nohup " + cmmd + " 2>&1 > ./build_logs/log_%d &"%idx
                    subprocess.call(cmd, shell=True)
                    break
                elif idx == 100:
                    print("Error : please, delite the log files in directory '/build_logs/'  ")
                    print("Error : command '%s' was ignored.")
                    break
            print("Your background works were done.")
            print("Build log was saved at " + pcolor.yellow + "build_logs/log_%d &"%idx + pcolor.clear)
        else:
            subprocess.call(cmmd, shell=True)

# modify to general format : local build configure file
def conf_modi():
    with open('webos-local.conf') as f:
        mems = f.readlines()
    for lines in range(len(mems)):
        if ('pqdb.tar' in mems[lines])&(mems[lines][0]!='#'):
            line_mem = mems[lines].split('deploy/tar/')[0]+'deploy/tar/${MACHINE}/pqdb.tar'+mems[lines].split('pqdb.tar')[-1]
            if line_mem != mems[lines]:
                mems[lines] = line_mem
                with open('webos-local.conf', 'w') as f:
                    f.writelines(mems)
            break

def load_previous_status():
    with open('build_configure.json') as f:
        build_stat = json.load(f)
    build_stat["checkout_branch"]= Repo(path='./').active_branch.name
    if os.path.isfile('./oe-init-build-env'):
        with open('./oe-init-build-env') as f:
            mems = f.readlines()
        for lines in range(len(mems)):
            if ('MACHINE=' in mems[lines])&(mems[lines][0]!='#'):
                build_stat["chip"] = mems[lines].split('MACHINE="')[-1].split('"')[0]
                break
    else:
        build_stat["chip"]="None"
    with open('build_configure.json') as f:
        build_check = json.load(f)
    if (build_stat["chip"]!=build_check["chip"]) | (build_stat["checkout_branch"]!=build_check["checkout_branch"]):
        with open('build_configure.json', 'w') as outfile:
            json.dump(build_stat, outfile)
    return build_stat

def program_ops(chip):
    branches = []
    SoC_64 = []
    with open('build_ops') as fid:
        ops_data = fid.readlines()
    for idx in range(len(ops_data)):
        if '## branches' in ops_data[idx]:
            branch_sp = idx+1
            branch_key = ops_data[idx].split('recognize key : "')[-1].split('"')[0]
        if '## 64bit SoC' in ops_data[idx]:
            SoC_sp = idx + 1
            SoC_key = ops_data[idx].split('recognize key : "')[-1].split('"')[0]
    for idx in range(branch_sp,SoC_sp-1):
        if branch_key in ops_data[idx][0]:
            branches.append(ops_data[idx].split('\n')[0])###\r or \n need to check
    for idx in range(SoC_sp, len(ops_data)):
        if SoC_key in ops_data[idx][0]:
            SoC_64.append(ops_data[idx].split(SoC_key)[-1].split('\n')[0])
    chip_type = "SoC_32"
    for idx in range(len(SoC_64)):
        if SoC_64[idx] in chip:
            chip_type = "SoC_64"
    return branches, chip_type

def kill_PIDs():
    pipe = subprocess.Popen("pwd", stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
    user_name = pipe.stdout.read()
    user_name = user_name.split("users/")[-1].split('/')[0]
    pipe = subprocess.Popen("ps aux | grep %s | grep bitbake" % user_name, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, shell=True)
    Process_log = pipe.stdout.read().split('\n')

    num_f = []
    PIDs = []
    PID_idx = -1
    for P_idx in range(len(Process_log)):
        flag = 0
        prev = False
        if len(Process_log[P_idx]) > 0:
            if "ps aux | grep" not in Process_log[P_idx]:
                num_f.append([])
                PID_idx += 1
                for idx in range(len(Process_log[P_idx])):
                    curr = Process_log[P_idx][idx] == " "
                    if prev != curr:
                        flag += 1
                        prev = curr
                    if flag == 2:
                        num_f[PID_idx].append(Process_log[P_idx][idx])
                pid = 0
                for idx in range(len(num_f[P_idx])):
                    pid += (int(num_f[P_idx][len(num_f[P_idx]) - idx - 1]) * 10 ** idx)
                PIDs.append(pid)
    pids = ""
    for idx in range(len(PIDs)):
        pids += str(PIDs[idx]) + " "
    return pids

def QnA(Q, err, err2="", selective=False, args=[]):
    print Q,
    x = getch()
    if selective:
        selected = 0
        msg_able=True
        x = ord(x) == 13 and '1' or x
        for idx in range(len(args)):
            if str(idx + 1) == x:
                selected = idx
                msg_able=False
        answer = args[selected]
        if msg_able:
            print(pcolor.yellow+err+pcolor.clear)
    else: #yes or no
        if (x == 'y') | (x == 'Y') | (ord(x) == 13):
            answer = True
        elif (x == 'n') | (x == 'N'):
            answer = False
            if err2!="":
                print(err2)
        else:
            answer = False
            print(pcolor.yellow+err+pcolor.clear)
    return answer