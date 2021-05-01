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


# Créer les apps et redirection de stdin et out de chacune
./clt.py --auto --ident=node1 --whatwho --bas-dest=NET --name=CLT1 < ./tmp/in1a > ./tmp/out1a &
./net.py --auto --ident=node1 --whatwho < ./tmp/in1b > ./tmp/out1b &

./clt.py --auto --ident=node2 --whatwho --bas-dest=NET --name=CLT2 < ./tmp/in2a > ./tmp/out2a &
./net.py --auto --ident=node2 --whatwho < ./tmp/in2b > ./tmp/out2b &

./clt.py --auto --ident=node3 --whatwho --bas-dest=NET --name=CLT3 < ./tmp/in3a > ./tmp/out3a &
./net.py --auto --ident=node3 --whatwho < ./tmp/in3b > ./tmp/out3b &

# Rediriger les pipes
# Liaison 1 -> 2, 1 -> 3, 2 -> 3 et 3 -> 1
cat ./tmp/out1a > ./tmp/in1b &
cat ./tmp/out1b | tee ./tmp/in1a > ./tmp/in2b ./tmp/in3b &
cat ./tmp/out2a > ./tmp/in2b &
cat ./tmp/out2b | tee ./tmp/in2a > ./tmp/in3b &
cat ./tmp/out3a > ./tmp/in3b &
cat ./tmp/out3b | tee ./tmp/in3a > ./tmp/in1b &
