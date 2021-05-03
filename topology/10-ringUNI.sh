# Faire le ménage
killall clt.py
killall net.py
killall cat
killall tee
rm ./tmp/*

# Créer les pipes
mkfifo ./tmp/in1c ./tmp/out1c
mkfifo ./tmp/in1n ./tmp/out1n
mkfifo ./tmp/in2a ./tmp/out2a
mkfifo ./tmp/in2n ./tmp/out2n
mkfifo ./tmp/in3c ./tmp/out3c
mkfifo ./tmp/in3n ./tmp/out3n
mkfifo ./tmp/in4c ./tmp/out4c
mkfifo ./tmp/in4n ./tmp/out4n
mkfifo ./tmp/in5c ./tmp/out5c
mkfifo ./tmp/in5n ./tmp/out5n
mkfifo ./tmp/in6c ./tmp/out6c
mkfifo ./tmp/in6n ./tmp/out6n
mkfifo ./tmp/in7c ./tmp/out7c
mkfifo ./tmp/in7n ./tmp/out7n
mkfifo ./tmp/in8c ./tmp/out8c
mkfifo ./tmp/in8n ./tmp/out8n
mkfifo ./tmp/in9c ./tmp/out9c
mkfifo ./tmp/in9n ./tmp/out9n
mkfifo ./tmp/in10c ./tmp/out10c
mkfifo ./tmp/in10n ./tmp/out10n



# Créer les apps et redirection de stdin et out de chacune
# Noeud 1
./gch.py --auto --ident=gch --whatwho --bas-dest=NET < ./tmp/in1c > ./tmp/out1c &
./net.py --auto --ident=gch --whatwho < ./tmp/in1n > ./tmp/out1n &

# Noeud 2
./clt.py --auto --ident=clt1 --whatwho --bas-dest=NET < ./tmp/in2a > ./tmp/out2a &
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

# Noeud 7
./clt.py --auto --ident=clt6 --whatwho --bas-dest=NET < ./tmp/in7c > ./tmp/out7c &
./net.py --auto --ident=clt6 --whatwho < ./tmp/in7n > ./tmp/out7n &

# Noeud 8
./clt.py --auto --ident=clt7 --whatwho --bas-dest=NET < ./tmp/in8c > ./tmp/out8c &
./net.py --auto --ident=clt7 --whatwho < ./tmp/in8n > ./tmp/out8n &

# Noeud 9
./clt.py --auto --ident=clt8 --whatwho --bas-dest=NET < ./tmp/in9c > ./tmp/out9c &
./net.py --auto --ident=clt8 --whatwho < ./tmp/in9n > ./tmp/out9n &

# Noeud 10
./clt.py --auto --ident=clt9 --whatwho --bas-dest=NET < ./tmp/in10c > ./tmp/out10c &
./net.py --auto --ident=clt9 --whatwho < ./tmp/in10n > ./tmp/out10n &



# Rediriger les pipes 1-> 2 - > ...
cat ./tmp/out1c > ./tmp/in1n &
cat ./tmp/out1n | tee ./tmp/in1c > ./tmp/in2n &

cat ./tmp/out2a > ./tmp/in2n &
cat ./tmp/out2n | tee ./tmp/in2a > ./tmp/in3n &

cat ./tmp/out3c > ./tmp/in3n &
cat ./tmp/out3n | tee ./tmp/in3c > ./tmp/in4n &

cat ./tmp/out4c > ./tmp/in4n &
cat ./tmp/out4n | tee ./tmp/in4c > ./tmp/in5b &

cat ./tmp/out5c > ./tmp/in5n &
cat ./tmp/out5n | tee ./tmp/in5c > ./tmp/in6b &

cat ./tmp/out6c > ./tmp/in6n &
cat ./tmp/out6n | tee ./tmp/in6c > ./tmp/in7b &

cat ./tmp/out7c > ./tmp/in7n &
cat ./tmp/out7n | tee ./tmp/in7c > ./tmp/in8b &

cat ./tmp/out8c > ./tmp/in8n &
cat ./tmp/out8n | tee ./tmp/in8c > ./tmp/in9b &

cat ./tmp/out9c > ./tmp/in9n &
cat ./tmp/out9n | tee ./tmp/in9c > ./tmp/in10b &

cat ./tmp/out10c > ./tmp/in10n &
cat ./tmp/out10n | tee ./tmp/in10c > ./tmp/in1n &
