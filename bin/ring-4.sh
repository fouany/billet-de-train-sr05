# Faire le ménage
killall clt.py
killall net.py
killall cat
killall tee
rm ./tmp/*

# Créer les pipes
mkfifo ./tmp/in1a ./tmp/out1a
mkfifo ./tmp/in1b ./tmp/out1b
mkfifo ./tmp/in2a ./tmp/out2a
mkfifo ./tmp/in2b ./tmp/out2b
mkfifo ./tmp/in3a ./tmp/out3a
mkfifo ./tmp/in3b ./tmp/out3b
mkfifo ./tmp/in4c ./tmp/out4c
mkfifo ./tmp/in4n ./tmp/out4n


# Créer les apps et redirection de stdin et out de chacune
./clt.py --auto --ident=node1 --whatwho --bas-dest=NET < ./tmp/in1a > ./tmp/out1a &
./net.py --auto --ident=node1 --whatwho < ./tmp/in1b > ./tmp/out1b &

./clt.py --auto --ident=node2 --whatwho --bas-dest=NET < ./tmp/in2a > ./tmp/out2a &
./net.py --auto --ident=node2 --whatwho  < ./tmp/in2b > ./tmp/out2b &

./clt.py --auto --ident=node3 --whatwho --bas-dest=NET < ./tmp/in3a > ./tmp/out3a &
./net.py --auto --ident=node3 --whatwho < ./tmp/in3b > ./tmp/out3b &

./clt.py --auto --ident=node4 --whatwho --bas-dest=NET < ./tmp/in4c > ./tmp/out4c &
./net.py --auto --ident=node4 --whatwho < ./tmp/in4n > ./tmp/out4n &


# Rediriger les pipes
# Liaison 1 -> 2, 1 -> 3, 2 -> 3 et 3 -> 1
cat ./tmp/out1a > ./tmp/in1b &
cat ./tmp/out1b | tee ./tmp/in1a > ./tmp/in2b ./tmp/in3b ./tmp/in4n &
cat ./tmp/out2a > ./tmp/in2b &
cat ./tmp/out2b | tee ./tmp/in2a > ./tmp/in3b &
cat ./tmp/out3a > ./tmp/in3b &
cat ./tmp/out3b | tee ./tmp/in3a > ./tmp/in4n &
cat ./tmp/out4c > ./tmp/in4n &
cat ./tmp/out4n | tee ./tmp/in4c > ./tmp/in1b &
