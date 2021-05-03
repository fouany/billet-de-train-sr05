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
mkfifo ./tmp/in5c ./tmp/out5c
mkfifo ./tmp/in5n ./tmp/out5n
mkfifo ./tmp/in6c ./tmp/out6c
mkfifo ./tmp/in6n ./tmp/out6n



# Créer les apps et redirection de stdin et out de chacune
# Noeud 1
./gch.py --auto --ident=gch --whatwho --bas-dest=NET < ./tmp/in1a > ./tmp/out1a &
./net.py --auto --ident=gch --whatwho < ./tmp/in1b > ./tmp/out1b &

# Noeud 2
./clt.py --auto --ident=clt1 --whatwho --bas-dest=NET < ./tmp/in2a > ./tmp/out2a &
./net.py --auto --ident=clt1 --whatwho  < ./tmp/in2b > ./tmp/out2b &

# Noeud 3
./clt.py --auto --ident=clt2 --whatwho --bas-dest=NET < ./tmp/in3a > ./tmp/out3a &
./net.py --auto --ident=clt2 --whatwho < ./tmp/in3b > ./tmp/out3b &

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
cat ./tmp/out1a > ./tmp/in1b &
cat ./tmp/out1b | tee ./tmp/in1a > ./tmp/in2b &

# CLT1 -> CLT2 et GCH <- CLT1
cat ./tmp/out2a > ./tmp/in2b &
cat ./tmp/out2b | tee ./tmp/in2a > ./tmp/in3b ./tmp/in1b &

# CLT2 -> CLT3 et CLT1 <- CLT2
cat ./tmp/out3a > ./tmp/in3b &
cat ./tmp/out3b | tee ./tmp/in3a > ./tmp/in4n ./tmp/in2a &

# CLT3 -> CLT4 et CLT3 -> CLT5 et CLT2 <- CLT3
cat ./tmp/out4c > ./tmp/in4n &
cat ./tmp/out4n | tee ./tmp/in4c > ./tmp/in5b ./tmp/in6b ./tmp/in3b &

# CLT4 -> CLT3
cat ./tmp/out5c > ./tmp/in5n &
cat ./tmp/out5n | tee ./tmp/in5c > ./tmp/in4b &

# CLT5 -> CLT3
cat ./tmp/out6c > ./tmp/in6n &
cat ./tmp/out6n | tee ./tmp/in6c > ./tmp/in4b &
