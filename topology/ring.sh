# Faire le ménage
killall bas.py
killall net.py
killall cat
killall tee

# Crée les pipes
mkfifo /tmp/in1a /tmp/out1a
mkfifo /tmp/in1b /tmp/out1b
mkfifo /tmp/in2a /tmp/out2a
mkfifo /tmp/in2b /tmp/out2b
mkfifo /tmp/in3a /tmp/out3a
mkfifo /tmp/in3b /tmp/out3b


# Crée les apps et redirection de stdin et out de chacune
./bas.py --auto --ident=node1 --whatwho --bas-dest=NET < /tmp/in1a > /tmp/out1a &
./net.py --auto --ident=node1 --whatwho < /tmp/in1b > /tmp/out1b &

./bas.py --auto --ident=node2 --whatwho --bas-dest=NET < /tmp/in2a > /tmp/out2a &
./net.py --auto --ident=node2 --whatwho  < /tmp/in2b > /tmp/out2b &

./bas.py --auto --ident=node3 --whatwho --begin=NET --bas-dest=NET < /tmp/in3a > /tmp/out3a &
./net.py --auto --ident=node3 --whatwho < /tmp/in3b > /tmp/out3b &

# redirection des pipes
cat /tmp/out1a > /tmp/in1b &
cat /tmp/out1b | tee /tmp/in1a > /tmp/in2b &
cat /tmp/out2a > /tmp/in2b &
cat /tmp/out2b | tee /tmp/in2a > /tmp/in3b &
cat /tmp/out3a > /tmp/in3b &
cat /tmp/out3b | tee /tmp/in3a > /tmp/in1b &
