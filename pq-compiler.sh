argc=$#
debug_mode=0
run_mode=0
epk_mode=0
tar_mode=0
pqc_mode=0
pqdb_mode=0
env_mode=0
bg_mode=0

if [[ $argc > 5 ]]; then
  echo "please, enter less than 6 options. this program only allows 5 options"
else
  if [[ $1 == 'bg' ]]; then
    bg_mode=1
  elif [[ $2 == 'bg' ]]; then
    bg_mode=1
  elif [[ $3 == 'bg' ]]; then
    bg_mode=1
  elif [[ $4 == 'bg' ]]; then
    bg_mode=1
  elif [[ $5 == 'bg' ]]; then
    bg_mode=1
  fi

  if [[ $1 == 'env' ]]; then
    env_mode=1
  elif [[ $2 == 'env' ]]; then
    env_mode=1
  elif [[ $3 == 'env' ]]; then
    env_mode=1
  elif [[ $4 == 'env' ]]; then
    env_mode=1
  elif [[ $5 == 'env' ]]; then
    env_mode=1
  fi

  if [[ $1 == 'debug' ]]; then
    debug_mode=1
  elif [[ $2 == 'debug' ]]; then
    debug_mode=1
  elif [[ $3 == 'debug' ]]; then
    debug_mode=1
  elif [[ $4 == 'debug' ]]; then
    debug_mode=1
  elif [[ $5 == 'debug' ]]; then
    debug_mode=1
  fi

  if [[ $1 == 'epk' ]]; then
    epk_mode=1
  elif [[ $2 == 'epk' ]]; then
    epk_mode=1
  elif [[ $3 == 'epk' ]]; then
    epk_mode=1
  elif [[ $4 == 'epk' ]]; then
    epk_mode=1
  elif [[ $5 == 'epk' ]]; then
    epk_mode=1
  fi

  if [[ $1 == 'tar' ]]; then
    tar_mode=1
  elif [[ $2 == 'tar' ]]; then
    tar_mode=1
  elif [[ $3 == 'tar' ]]; then
    tar_mode=1
  elif [[ $4 == 'tar' ]]; then
    tar_mode=1
  elif [[ $5 == 'tar' ]]; then
    tar_mode=1
  fi

  if [[ $1 == 'pqc' ]]; then
    pqc_mode=1
  elif [[ $2 == 'pqc' ]]; then
    pqc_mode=1
  elif [[ $3 == 'pqc' ]]; then
    pqc_mode=1
  elif [[ $4 == 'pqc' ]]; then
    pqc_mode=1
  elif [[ $5 == 'pqc' ]]; then
    pqc_mode=1
  fi

  if [[ $1 == 'pqdb' ]]; then
    pqdb_mode=1
  elif [[ $2 == 'pqdb' ]]; then
    pqdb_mode=1
  elif [[ $3 == 'pqdb' ]]; then
    pqdb_mode=1
  elif [[ $4 == 'pqdb' ]]; then
    pqdb_mode=1
  elif [[ $5 == 'pqdb' ]]; then
    pqdb_mode=1
  fi

  if [ $env_mode == '1' ] || [ $tar_mode == '1' ] || [ $epk_mode == '1' ] || [ $pqc_mode == '1' ] || [ $pqdb_mode == '1' ];then
    run_mode=1
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
  else
    if [[ $env_mode == '1' ]];then
      python build_exec -m env_mode -d $debug_mode && echo ' '
    fi
    unset MACHINE MACHINES && echo ' '
    source oe-init-build-env && echo ' '
    if [[ $tar_mode == '1' ]];then
      python build_exec -m tar_mode -d $debug_mode -b $bg_mode && echo ' '
    fi
    if [[ $pqdb_mode == '1' ]];then
      python build_exec -m pqdb_mode -d $debug_mode -b $bg_mode && echo ' '
    fi
    if [[ $pqc_mode == '1' ]];then
      python build_exec -m pqc_mode -d $debug_mode -b $bg_mode && echo ' '
    fi
    if [[ $epk_mode == '1' ]];then
      python build_exec -m epk_mode -d $debug_mode -b $bg_mode && echo ' '
    fi
  fi
  if [ $debug_mode == '0' ] && [ $bg_mode == '0' ];then
    col_size=$(tput cols)
    lin_size=$(tput lines)
    reset
    printf $(echo "\033[8;${lin_size};${col_size}t")
  fi
  if [[ $bg_mode == '1' ]];then
    echo "your process run in background."
    echo "you can control your processes using followd commands"
    echo -e "\033[0;31m ps aux | grep user_name \033[0m : check PID number of your tasks"
    echo -e "\033[0;31m kill -9 PID_number \033[0m : kill your task"
  fi
fi