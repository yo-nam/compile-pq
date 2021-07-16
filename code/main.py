import subprocess, sys, json, tty, termios, os
from git import Repo

dbg = False
run_mode = False
bg_mode = 0

def proc_cmd(cmmd, debug, bg=0):
    if debug:
        print(cmmd)
    else:
        if bg=='1':
            for idx in range(101):
                if os.path.isfile('./build_logs/log_%d'%idx)==False:
                    cmd = "nohup " + cmmd + " 2>&1 > ./build_logs/log_%d &"%idx
                    subprocess.call(cmd, shell=True)
                    break
                elif idx == 100:
                    print("Error : please, delite the log files in directory '/build_logs/'  ")
                    print("Error : command '%s' was ignored.")
                    break
        else:
            subprocess.call(cmmd, shell=True)

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

class pcolor:
    red='\033[0;31m'
    green='\033[0;32m'
    blue='\033[0;34m'
    cyan='\033[0;36m'
    gray='\033[0;37m'
    yellow='\033[1;33m'
    clear='\033[0m'

############# loading previous status ###################
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
#########################################################
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
        branches.append(ops_data[idx].split('\r')[0])###\r or \n need to check
for idx in range(SoC_sp, len(ops_data)):
    if SoC_key in ops_data[idx][0]:
        SoC_64.append(ops_data[idx].split(SoC_key)[-1].split('\r')[0])

# mode decision
if (len(sys.argv) > 1) & (len(sys.argv) % 2 == 1):
    for idx in range(len(sys.argv)):
        if '-d' in sys.argv[idx]:
            if sys.argv[idx + 1] == '1':
                dbg = True
        if '-m' in sys.argv[idx]:
            run_mode = sys.argv[idx + 1]
        if '-b' in sys.argv[idx]:
            bg_mode = sys.argv[idx + 1]
else:
    sys.exit('NG2')
if run_mode == False:
    sys.exit('NG1')

chip_type = "out_sourcing"
for idx in range(len(SoC_64)):
    if SoC_64[idx] in build_stat["chip"]:
        chip_type = "in_house"

if run_mode=='build':
    if chip_type == "in_house":
        if build_stat["make_libpqdb_tar"]:
            proc_cmd("bitbake lib32-pqdb -f -c package_sysrootdir_tar",dbg, bg_mode)
        if build_stat["compile_libpqdb"]:
            proc_cmd("bitbake lib32-libpqdb",dbg, bg_mode)
        if build_stat["compile_pqcontroller"]:
            proc_cmd("bitbake lib32-pqcontroller",dbg, bg_mode)
        if build_stat["compile_to_epk"]:
            proc_cmd("bitbake lib32-starfish-" + build_stat["build_country"] + "-" + build_stat["build-type"], dbg, bg_mode)
    else :
        if build_stat["make_libpqdb_tar"]:
            proc_cmd("bitbake pqdb -f -c package_sysrootdir_tar",dbg, bg_mode)
        if build_stat["compile_libpqdb"]:
            proc_cmd("bitbake libpqdb",dbg, bg_mode)
        if build_stat["compile_pqcontroller"]:
            proc_cmd("bitbake pqcontroller",dbg, bg_mode)
        if build_stat["compile_to_epk"]:
            proc_cmd("bitbake starfish-"+build_stat["build_country"]+"-"+build_stat["build-type"],dbg, bg_mode)
    print("\n\n#################################################################\nImage was built by PQ-Compiler.\nIf there is any needs for functions, please contact to PQ-team\n#################################################################\n")


elif run_mode=='parse':
    with open('build_configure.json') as f:
        modi_stat = json.load(f)
    pullable = False
    printable = False
    print(
        "\n\n#################################################################\n                   webOS PQ-Compiler v0.1             by PQ-Team")
    print("------------------------- Build env. ----------------------------")
    print(" Checkout branch : %s\n Selected chip : %s " % (build_stat["checkout_branch"], build_stat["chip"]))
    print("#################################################################")
    print "\nWant to change environments? : [y/n] ",
    diff_dec = getch()
    if (diff_dec == 'y')|(diff_dec == 'Y')|(ord(diff_dec) == 13):
        printable = True
        print "Select your branch (defualt : %s) \n ["%build_stat["checkout_branch"],
        for branch_idx in range(len(branches)):
            if branch_idx == (len(branches)-1):
                print "%d: %s ] : "%(branch_idx+1, branches[branch_idx]),
            else:
                print "%d: %s, " %(branch_idx+1, branches[branch_idx]),
        x = ord(getch()) # 48 = 0
        if x==13:
            x = 0
        elif (x>(len(branches)+48))|(x<=48):
            print(":::Warning : Wrong input, it will be set to '%s'"%build_stat["checkout_branch"])
        else:
            x=x-48
            modi_stat["checkout_branch"] = branches[x-1]

        #print "Want to update your branch? (it contained git pull, defualt : no) : [y/n] ",
        print "Want to update your branch? (defualt : no) : [y/n] ",
        x = getch()
        if (x == 'y') | (x == 'Y'):
            pullable = True
        x = raw_input("Input chip name (default : %s) : "%build_stat["chip"])
        if x == '':
            x = build_stat["chip"]
        modi_stat["chip"] = x
    elif (diff_dec =='n')|(diff_dec =='N'):
        print("It will execute as-like last time.")
    else:
        print(":::Warning : Wrong input, it will execute as-like last time.")

    print("\n#################################################################")
    print("--------------------- Output options ----------------------------")
    print(
        " Make libpqdb tar file : %s\n Compile libpqdb : %s\n Compile pqcontroller : %s\n Make epk image : %s\n Build country : %s\n Build-type : %s" % (
            build_stat["make_libpqdb_tar"], build_stat["compile_libpqdb"], build_stat["compile_pqcontroller"],
            build_stat["compile_to_epk"], build_stat["build_country"], build_stat["build-type"]))
    print("#################################################################")

    print "\nIs there any different options? [y/n] ",
    diff_dec = getch()
    if (diff_dec == 'y') | (diff_dec == 'Y') | (ord(diff_dec) == 13):
        ######################################
        printable = True
        print "Want to make libpqdb tar file? (default : yes) : [y/n] ",
        x = getch()
        if (x == 'y') | (x == 'Y') | (ord(x) == 13):
            modi_stat["make_libpqdb_tar"] = True
        elif (x == 'n') | (x == 'N'):
            modi_stat["make_libpqdb_tar"] = False
        else:
            modi_stat["make_libpqdb_tar"] = True
            print(":::Warning : Wrong input, libpqdb tar file will be made.")

        print "Want to compile libpqdb? (default : no) : [y/n] ",
        x = getch()
        if (x == 'y') | (x == 'Y'):
            modi_stat["compile_libpqdb"] = True
        elif (x == 'n') | (x == 'N') | (ord(x) == 13):
            modi_stat["compile_libpqdb"] = False
        else:
            modi_stat["compile_libpqdb"] = False
            print(":::Warning : Wrong input, libpqdb won't be compiled")

        print "Want to compile pqcontroller? (default : no) : [y/n] ",
        x = getch()
        if (x == 'y') | (x == 'Y'):
            modi_stat["compile_pqcontroller"] = True
        elif (x == 'n') | (x == 'N') | (ord(x) == 13):
            modi_stat["compile_pqcontroller"] = False
        else:
            modi_stat["compile_pqcontroller"] = False
            print(":::Warning : Wrong input, pqcontroller won't be compiled")

        print "Want to compile for epk image file? (default : yes) : [y/n] ",
        x = getch()
        if (x == 'y') | (x == 'Y') | (ord(x) == 13):
            modi_stat["compile_to_epk"] = True

            print "Input the build type (default : flash)\n[1:flash, 2:flash-devel, 3:secured, 4:nfs, 5:nfs-devel] : ",
            x = getch()
            if (ord(x) == 13) | (x == '1'):
                modi_stat["build-type"] = 'flash'
            elif x == '2':
                modi_stat["build-type"] = 'flash-devel'
            elif x == '3':
                modi_stat["build-type"] = 'secured'
            elif x == '4':
                modi_stat["build-type"] = 'nfs'
            elif x == '5':
                modi_stat["build-type"] = 'nfs-devel'
            else:
                modi_stat["build-type"] = 'flash'
                print(":::Warning : Wrong input, built type set to flash")

            print "Select country (default : global) [1:global, 2:japan] : ",
            x = getch()
            if (ord(x) == 13) | (x == '1'):
                modi_stat["build_country"] = 'global'
            elif x == '2':
                modi_stat["build_country"] = 'arib'
            else:
                print(":::Warning : Wrong input, built country set to global")
                modi_stat["build_country"] = 'global'
        elif (x == 'n') | (x == 'N'):
            modi_stat["compile_to_epk"] = False
        else:
            modi_stat["compile_to_epk"] = False
            print(":::Warning : Wrong input, it won't make epk image.")
    elif (diff_dec =='n')|(diff_dec =='N'):
        print("It will execute as-like last time.")
    else:
        print(":::Warning : Wrong input, it will execute as-like last time.")

    with open('build_configure.json', 'w') as outfile:
        json.dump(modi_stat, outfile)
    if printable:
        print("\n\n################ Your Options are as followed ###################")
        print("------------------------- Build env. ----------------------------")
        print(" Checkout branch : %s\n Selected chip : %s\n Git pull : %s" % (
        modi_stat["checkout_branch"], modi_stat["chip"], pullable))
        print("--------------------- Output options ----------------------------")
        print(
            " Make libpqdb tar file : %s\n Compile libpqdb : %s\n Compile pqcontroller : %s\n Make epk image : %s\n Build country : %s\n Build-type : %s" % (
                modi_stat["make_libpqdb_tar"], modi_stat["compile_libpqdb"], modi_stat["compile_pqcontroller"],
                modi_stat["compile_to_epk"], modi_stat["build_country"], modi_stat["build-type"]))
        print("#################################################################")
    if modi_stat["checkout_branch"]!=build_stat["checkout_branch"]:
        proc_cmd("git checkout " + modi_stat["checkout_branch"], dbg)
    if pullable:
        proc_cmd("git pull", dbg)
    if (modi_stat["chip"]!=build_stat["chip"])|pullable:
        proc_cmd("./mcf -b 16 -p 16 " + modi_stat[
            "chip"] + " --premirror=file:///starfish/downloads --sstatemirror=file:///starfish/sstate-cache", dbg)
        conf_modi()

elif run_mode=='env_mode':
    with open('build_configure.json') as f:
        modi_stat = json.load(f)
    print(
        "\n\n#################################################################\n                   webOS PQ-Compiler v0.1             by PQ-Team")
    print("------------------------- Build env. ----------------------------")
    print(" Checkout branch : %s\n Selected chip : %s" % (build_stat["checkout_branch"], build_stat["chip"]))
    print(" Build country : %s\n Build-type : %s" % (build_stat["build_country"], build_stat["build-type"]))
    print("#################################################################")
    pullable = False
    print "\nWant to change environments? : [y/n] ",
    diff_dec = getch()
    if (diff_dec == 'y')|(diff_dec == 'Y')|(ord(diff_dec) == 13):
        print "Select your branch (defualt : %s) \n [" % build_stat["checkout_branch"],
        for branch_idx in range(len(branches)):
            if branch_idx == (len(branches) - 1):
                print "%d: %s ] : " % (branch_idx + 1, branches[branch_idx]),
            else:
                print "%d: %s, " % (branch_idx + 1, branches[branch_idx]),
        x = ord(getch())  # 48 = 0
        if x == 13:
            x = 0
        elif (x > (len(branches) + 48)) | (x <= 48):
            print(":::Warning : Wrong input, it will be set to '%s'" % build_stat["checkout_branch"])
        else:
            x = x - 48
            modi_stat["checkout_branch"] = branches[x - 1]

        print "Want to update your branch? (defualt : no) : [y/n] ",
        x = getch()
        if (x == 'y') | (x == 'Y'):
            pullable = True
        x = raw_input("Input chip name (default : %s) : " % build_stat["chip"])
        if x == '':
            x = build_stat["chip"]
        modi_stat["chip"] = x
        print "Input the build type (default : flash)\n[1:flash, 2:flash-devel, 3:secured, 4:nfs, 5:nfs-devel] : ",
        x = getch()
        if (ord(x) == 13) | (x == '1'):
            modi_stat["build-type"] = 'flash'
        elif x == '2':
            modi_stat["build-type"] = 'flash-devel'
        elif x == '3':
            modi_stat["build-type"] = 'secured'
        elif x == '4':
            modi_stat["build-type"] = 'nfs'
        elif x == '5':
            modi_stat["build-type"] = 'nfs-devel'
        else:
            modi_stat["build-type"] = 'flash'
            print(":::Warning : Wrong input, built type set to flash")

        print "Select country (default : global) [1:global, 2:japan] : ",
        x = getch()
        if (ord(x) == 13) | (x == '1'):
            modi_stat["build_country"] = 'global'
        elif x == '2':
            modi_stat["build_country"] = 'arib'
        else:
            print(":::Warning : Wrong input, built country set to global")
            modi_stat["build_country"] = 'global'
        print("\n################ Your Options are as followed ###################")
        print("------------------------- Build env. ----------------------------")
        print(" Checkout branch : %s\n Selected chip : %s\n Git pull : %s" % (
            modi_stat["checkout_branch"], modi_stat["chip"], pullable))
        print(" Build country : %s\n Build-type : %s " % (
            modi_stat["build_country"], modi_stat["build-type"]))
        print("#################################################################")
        with open('build_configure.json', 'w') as outfile:
            json.dump(modi_stat, outfile)
    elif (diff_dec =='n')|(diff_dec =='N'):
        print("It will execute as-like last time.")
    else:
        print(":::Warning : Wrong input, it will execute as-like last time.")

    if modi_stat["checkout_branch"]!=build_stat["checkout_branch"]:
        proc_cmd("git checkout " + modi_stat["checkout_branch"], dbg)
    if pullable:
        proc_cmd("git pull", dbg)
    if (modi_stat["chip"]!=build_stat["chip"])|pullable:
        proc_cmd("./mcf -b 16 -p 16 " + modi_stat[
            "chip"] + " --premirror=file:///starfish/downloads --sstatemirror=file:///starfish/sstate-cache", dbg)
        conf_modi()

elif run_mode=='tar_mode':
    if chip_type == "in_house":
        proc_cmd("bitbake lib32-pqdb -f -c package_sysrootdir_tar", dbg, bg_mode)
    else:
        proc_cmd("bitbake pqdb -f -c package_sysrootdir_tar", dbg, bg_mode)

elif run_mode=='pqdb_mode':
    if chip_type == "in_house":
        proc_cmd("bitbake lib32-libpqdb", dbg, bg_mode)
    else:
        proc_cmd("bitbake libpqdb", dbg, bg_mode)

elif run_mode=='pqc_mode':
    if chip_type == "in_house":
        proc_cmd("bitbake lib32-pqcontroller", dbg, bg_mode)
    else:
        proc_cmd("bitbake pqcontroller", dbg, bg_mode)

elif run_mode=='epk_mode':
    if chip_type == "in_house":
        proc_cmd("bitbake lib32-starfish-" + build_stat["build_country"] + "-" + build_stat["build-type"], dbg, bg_mode)
    else:
        proc_cmd("bitbake starfish-" + build_stat["build_country"] + "-" + build_stat["build-type"], dbg, bg_mode)

elif run_mode=='checker':
    # mode decision
    if (len(sys.argv) > 1) & (len(sys.argv) % 2 == 1):
        for idx in range(len(sys.argv)):
            if '-d' in sys.argv[idx]:
                if sys.argv[idx + 1] == '1':
                    dbg = True
            if '-m' in sys.argv[idx]:
                run_mode = sys.argv[idx + 1]
    else:
        sys.exit('NG2')

    if run_mode == False:
        sys.exit('NG1')
else :
    print('NG3')