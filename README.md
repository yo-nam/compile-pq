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
>       maxium number of options : 5
> 
>       #options     #description   
>       dbg          debug mode (just print cmds)
>       epk          make epk image with previous options.
>       tar          make tar file with previous options.
>       pqdb         compile libpqdb
>       pqc          compile pqcontroller
>       env          settings for several build options.
>       bb           update the latest bb file (updated, 7/29)
>       .chip        change chip option (updated, 7/29)
>       @branch      change branch option (updated, 7/29)
