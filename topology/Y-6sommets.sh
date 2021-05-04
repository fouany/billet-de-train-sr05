# Faire le ménage
killall clt.py
killall gch.py
killall net.py
killall cat
killall tee
rm ./tmp/*

# Créer les pipes
mkfifo ./tmp/in1c ./tmp/out1c
mkfifo ./tmp/in1n ./tmp/out1n
mkfifo ./tmp/in2c ./tmp/out2c
mkfifo ./tmp/in2n ./tmp/out2n
mkfifo ./tmp/in3c ./tmp/out3c
mkfifo ./tmp/in3n ./tmp/out3n
mkfifo ./tmp/in4c ./tmp/out4c
mkfifo ./tmp/in4n ./tmp/out4n
mkfifo ./tmp/in5c ./tmp/out5c
mkfifo ./tmp/in5n ./tmp/out5n
mkfifo ./tmp/in6c ./tmp/out6c
mkfifo ./tmp/in6n ./tmp/out6n



# Créer les apps et redirection de stdin et out de chacune
# Noeud 1
./gch.py --auto --appname=CLT --ident=gch --whatwho --bas-dest=NET < ./tmp/in1c > ./tmp/out1c &
./net.py --auto --ident=gch --whatwho < ./tmp/in1n > ./tmp/out1n &

# Noeud 2
./clt.py --auto --ident=clt1 --whatwho --bas-dest=NET < ./tmp/in2c > ./tmp/out2c &
./net.py --auto --ident=clt1 --whatwho  < ./tmp/in2n > ./tmp/out2n &

# Noeud 3
./clt.py --auto --ident=clt2 --whatwho --bas-dest=NET < ./tmp/in3c > ./tmp/out3c &
./net.py --auto --ident=clt2 --whatwho < ./tmp/in3n > ./tmp/out3n &

# Noeud 4
./clt.py --auto --ident=clt3 --whatwho --bas-dest=NET < ./tmp/in4c > ./tmp/out4c &
./net.py --auto --ident=clt3 --whatwho < ./tmp/in4n > ./tmp/out4n &

# Noeud 5
./clt.py --auto --ident=clt4 --whatwho --bas-dest=NET < ./tmp/in5c > ./tmp/out5c &
./net.py --auto --ident=clt4 --whatwho < ./tmp/in5n > ./tmp/out5n &

# Noeud 6
./clt.py --auto --ident=clt5 --whatwho --bas-dest=NET < ./tmp/in6c > ./tmp/out6c &
./net.py --auto --ident=clt5 --whatwho < ./tmp/in6n > ./tmp/out6n &



# Rediriger les pipes
# GCH -> CLT1
cat ./tmp/out1c > ./tmp/in1n &
cat ./tmp/out1n | tee ./tmp/in1c > ./tmp/in2n &

# CLT1 -> CLT2 et GCH <- CLT1
cat ./tmp/out2c > ./tmp/in2n &
cat ./tmp/out2n | tee ./tmp/in2c > ./tmp/in3n ./tmp/in1n &

# CLT2 -> CLT3 et CLT1 <- CLT2
cat ./tmp/out3c > ./tmp/in3n &
cat ./tmp/out3n | tee ./tmp/in3c > ./tmp/in4n ./tmp/in2n &

# CLT3 -> CLT4 et CLT3 -> CLT5 et CLT2 <- CLT3
cat ./tmp/out4c > ./tmp/in4n &
cat ./tmp/out4n | tee ./tmp/in4c > ./tmp/in5n ./tmp/in6n ./tmp/in3n &

# CLT4 -> CLT3
cat ./tmp/out5c > ./tmp/in5n &
cat ./tmp/out5n | tee ./tmp/in5c > ./tmp/in4n &

# CLT5 -> CLT3
cat ./tmp/out6c > ./tmp/in6n &
cat ./tmp/out6n | tee ./tmp/in6c > ./tmp/in4n &
