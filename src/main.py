import sys, json, glob
from build_utils import conf_modi, getch, proc_cmd, pcolor, load_previous_status, program_ops

dbg = False
run_mode = False
bg_mode = 0

## loading previous status & options
build_stat = load_previous_status()
branches, chip_type = program_ops(build_stat["chip"])

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

if "chip_mode" in run_mode:
    chip_in = run_mode.split("%")[-1]
    run_mode = run_mode.split("%")[0]
if "branch_mode" in run_mode:
    branch_in = run_mode.split("%")[-1]
    run_mode = run_mode.split("%")[0]

if run_mode=='build':
    if chip_type == "SoC_64":
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
        proc_cmd("git pull --rebase", dbg)
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
        proc_cmd("git pull --rebase", dbg)
    if (modi_stat["chip"]!=build_stat["chip"])|pullable:
        proc_cmd("./mcf -b 16 -p 16 " + modi_stat[
            "chip"] + " --premirror=file:///starfish/downloads --sstatemirror=file:///starfish/sstate-cache", dbg)
        conf_modi()

elif run_mode=='branch_mode':
    if branch_in != build_stat["checkout_branch"]:
        proc_cmd("git checkout " + branch_in, dbg)
        proc_cmd("git pull --rebase", dbg)

elif run_mode=='chip_mode':
    if chip_in != build_stat["chip"]:
        proc_cmd("./mcf -b 16 -p 16 " + chip_in + " --premirror=file:///starfish/downloads --sstatemirror=file:///starfish/sstate-cache", dbg)

elif run_mode=='tar_mode':
    if chip_type == "SoC_64":
        proc_cmd("bitbake lib32-pqdb -f -c package_sysrootdir_tar", dbg, bg_mode)
    else:
        proc_cmd("bitbake pqdb -f -c package_sysrootdir_tar", dbg, bg_mode)

elif run_mode=='pqdb_mode':
    if chip_type == "SoC_64":
        proc_cmd("bitbake lib32-libpqdb", dbg, bg_mode)
    else:
        proc_cmd("bitbake libpqdb", dbg, bg_mode)

elif run_mode=='pqc_mode':
    if chip_type == "SoC_64":
        proc_cmd("bitbake lib32-pqcontroller", dbg, bg_mode)
    else:
        proc_cmd("bitbake pqcontroller", dbg, bg_mode)

elif run_mode=='epk_mode':
    if chip_type == "SoC_64":
        proc_cmd("bitbake lib32-starfish-" + build_stat["build_country"] + "-" + build_stat["build-type"], dbg, bg_mode)
    else:
        proc_cmd("bitbake starfish-" + build_stat["build_country"] + "-" + build_stat["build-type"], dbg, bg_mode)

elif run_mode=='del_epks':
    dirs = glob.glob('./BUILD/deploy/images/*')
    for idx in range(len(dirs)):
        if len(dirs[idx].split('images/')[-1]) < 6:
            epk_paths = glob.glob('%s/*' % dirs[idx])
            print(pcolor.yellow+"%s epks is deleting...%s"%(dirs[idx].split('images/')[-1],pcolor.clear))
            for epk_idx in range(len(epk_paths)):
                if '20' in epk_paths[epk_idx]:
                    cmd = 'rm -rf %s' % epk_paths[epk_idx]
                    proc_cmd(cmd,dbg, bg_mode)
                    print('%s was terminated.'%epk_paths[epk_idx].split(dirs[idx])[-1])

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