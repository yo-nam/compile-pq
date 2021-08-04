# Dev-required
os-system : Linux only

interpreter : python2 (not python3)

external library : gitpython

# Setup

input command on terminal as followed:
>#### ex) ../compile-pq$   ./setup_pq.sh

# Useage
## Basic : Excute shell script
>#### ex) ../build-starfish$ ./pq-compiler.sh
## Fast : Add options
> #### ex) ../build-starfish$ ./pq-compiler.sh opts1 opts2 opts3....
>       maxium number of options : 10
> 
>       #options     #description   
>       dbg          debug mode (just print cmds)
>       epk          make epk image with previous options
>       tar          make tar file with previous options
>       pqdb         compile libpqdb
>       pqc          compile pqcontroller
>       env          settings for several build options
>       bg           execute in background
>       bb           update the latest bb file (updated, 7/29)
>       .chip        change chip option (updated, 7/29)
>       @branch      change branch option (updated, 7/29)
>       del          delete epks except the latest image (updated, 8/1)
>       multi        make tar file for multi SoCs (updated, 8/3)
>                    * multi mode is special mode. 
>                    * useage : ./pq-compiler.sh multi o20 o22 k8hp ...
>                     >> 1st arg must multi, and others are SoC name without "." mark