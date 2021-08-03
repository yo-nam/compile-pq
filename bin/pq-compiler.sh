run_mode=0

if [[ $# -gt 10 ]]; then
  echo "please, enter less than 10 options. this program only allows 10 options"
else
  arg_in="$1 $2 $3 $4 $5 $6 $7 $8 $9 ${10}"
  bg_mode=$(python parse_opts "bg" $arg_in 2>&1) && echo ' '
  env_mode=$(python parse_opts "env" $arg_in 2>&1) && echo ' '
  debug_mode=$(python parse_opts "debug" $arg_in 2>&1) && echo ' '
  epk_mode=$(python parse_opts "epk" $arg_in 2>&1) && echo ' '
  tar_mode=$(python parse_opts "tar" $arg_in 2>&1) && echo ' '
  pqc_mode=$(python parse_opts "pqc" $arg_in 2>&1) && echo ' '
  pqdb_mode=$(python parse_opts "pqdb" $arg_in 2>&1) && echo ' '
  bb_cpy=$(python parse_opts "bb" $arg_in 2>&1) && echo ' '
  chip_mode=$(python parse_opts "." $arg_in 2>&1) && echo ' '
  branch_mode=$(python parse_opts "@" $arg_in 2>&1) && echo ' '
  del_mode=$(python parse_opts "del" $arg_in 2>&1) && echo ' '
  multi_soc=$(python parse_opts "multi" $arg_in 2>&1) && echo ' '
  if [ $chip_mode == 1 ]; then
    chip_in=$(python parse_opts "chip_mode" $arg_in 2>&1) && echo ' '
  fi
  if [ $branch_mode == 1 ]; then
    branch_in=$(python parse_opts "branch_mode" $arg_in 2>&1) && echo ' '
  fi
  if [[ $bb_cpy == 1 ]] || [ $del_mode == 1 ] ; then
    run_mode=1
  fi
  if [ $env_mode == 1 ] || [ $tar_mode == 1 ] || [ $epk_mode == 1 ] || [ $pqc_mode == 1 ] || [ $pqdb_mode == 1 ] || [ $chip_mode == 1 ] || [ $branch_mode == 1 ];then
    run_mode=1
  fi
  if [ $multi_soc == 1 ]; then
    run_mode=2
  fi

  if [[ $run_mode == '0' ]]; then
    STAT_BUILD=$(python build_exec -m checker 2>&1) && echo ' '
    if [[ $STAT_BUILD == "NG1" ]]; then
      echo 'Error : there is no options.'
    elif [[ $STAT_BUILD == "NG2" ]]; then
      echo 'Error : there is not enough arguments. please check it'
    elif [[ $STAT_BUILD == "NG2" ]]; then
      echo 'Error : there is wrong options (-m opts)'
    else
      python build_exec -m parse -d $debug_mode && echo ' '
      unset MACHINE MACHINES && echo ' '
      source oe-init-build-env && echo ' '
      python build_exec -m build -d $debug_mode -b $bg_mode && echo ' '
    fi
  elif [[ $run_mode == '2' ]]; then
    for var in $(seq $(($#-1)))
    do
      var2=$((var+1))
      python build_exec -m chip_mode%${!var2} -d $debug_mode && echo ' '
      unset MACHINE MACHINES && echo ' '
      source oe-init-build-env && echo ' '
      python build_exec -m tar_mode -d $debug_mode -b $bg_mode && echo ' '
    done
  else
    if [ $bb_cpy == 1 ]; then
      cp ../libpqdb/bb_file/pqdb.bb ./meta-lg-webos/meta-starfish/recipes-starfish/pqdb/
      echo 'bb_file has been updated'
    fi
    if [ $env_mode == 1 ] && ([ $chip_mode == 1 ] || [ $branch_mode == 1 ]);then
      echo "env_mode can't use with chip or branch selection."
    else
      if [[ $env_mode == 1 ]];then
        python build_exec -m env_mode -d $debug_mode && echo ' '
      fi
      if [[ $branch_mode == 1 ]];then
        python build_exec -m branch_mode%$branch_in -d $debug_mode && echo ' '
      fi
      if [[ $chip_mode == 1 ]];then
        python build_exec -m chip_mode%$chip_in -d $debug_mode && echo ' '
      fi
    fi
    unset MACHINE MACHINES && echo ' '
    source oe-init-build-env && echo ' '
    if [[ $tar_mode == 1 ]];then
      python build_exec -m tar_mode -d $debug_mode -b $bg_mode && echo ' '
    fi
    if [[ $pqdb_mode == 1 ]];then
      python build_exec -m pqdb_mode -d $debug_mode -b $bg_mode && echo ' '
    fi
    if [[ $pqc_mode == 1 ]];then
      python build_exec -m pqc_mode -d $debug_mode -b $bg_mode && echo ' '
    fi
    if [[ $epk_mode == 1 ]];then
      python build_exec -m epk_mode -d $debug_mode -b $bg_mode && echo ' '
    fi
    if [ $del_mode == 1 ]; then
      python build_exec -m del_epks -d $debug_mode -b $bg_mode && echo ' '
    fi
  fi
  if [ $bg_mode == 0 ]; then
    python build_exec -m kill -d $debug_mode -b $bg_mode && echo ' '
  fi
  if [ $debug_mode == 0 ] && [ $bg_mode == 0 ];then
    col_size=$(tput cols)
    lin_size=$(tput lines)
    reset
    printf $(echo "\033[8;${lin_size};${col_size}t")
  fi
  if [[ $bg_mode == 1 ]];then
    echo "your process run in background."
    echo "you can control your processes using followd commands"
    echo -e "\033[0;31m ps aux | grep user_name \033[0m : check PID number of your tasks"
    echo -e "\033[0;31m kill -9 PID_number \033[0m : kill your task"
  fi
fi