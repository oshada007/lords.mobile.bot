n=1 ;
while true ;
clear
echo "#$n: "
date
do python main.py;
  #echo "#$n: "
  sleep 20 ;
  n=$(( n + 1 )) ;
done
