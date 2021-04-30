#!/bin/bash
killall cat
killall tee
# Create named pipes, one input and one output per process.
mkfifo /tmp/in1a /tmp/out1a
mkfifo /tmp/in1b /tmp/out1b
mkfifo /tmp/in2a /tmp/out2a
mkfifo /tmp/in2b /tmp/out2b
mkfifo /tmp/in3a /tmp/out3a
mkfifo /tmp/in3b /tmp/out3b
mkfifo /tmp/in4a /tmp/out4a
mkfifo /tmp/in4b /tmp/out4b
mkfifo /tmp/in5a /tmp/out5a
mkfifo /tmp/in5b /tmp/out5b


# Starting the processes
./bas.py --auto --ident=node1 --whatwho --dest=NET < /tmp/in1a > /tmp/out1a &
./net.py --auto --ident=node1 --whatwho --source=BAS < /tmp/in1b > /tmp/out1b &

./bas.py --auto --ident=node2 --whatwho --dest=NET < /tmp/in2a > /tmp/out2a &
./net.py --auto --ident=node2 --whatwho --source=BAS < /tmp/in2b > /tmp/out2b &

./bas.py --auto --ident=node3 --whatwho --dest=NET < /tmp/in3a > /tmp/out3a &
./net.py --auto --ident=node3 --whatwho --source=BAS < /tmp/in3b > /tmp/out3b &

./bas.py --auto --ident=node4 --whatwho --dest=NET < /tmp/in4a > /tmp/out4a &
./net.py --auto --ident=node4 --whatwho --source=BAS < /tmp/in4b > /tmp/out4b &

./bas.py --auto --ident=node5 --whatwho --dest=NET < /tmp/in5a > /tmp/out5a &
./net.py --auto --ident=node5 --whatwho --source=BAS < /tmp/in5b > /tmp/out5b &


# Création des liens
cat /tmp/out1a > /tmp/in1b &
cat /tmp/out1b | tee /tmp/in1a > /tmp/in2b &

cat /tmp/out2a > /tmp/in2b &
cat /tmp/out2b | tee /tmp/in2a > /tmp/in3b &

cat /tmp/out3a > /tmp/in3b &
cat /tmp/out3b | tee /tmp/in3a | tee /tmp/in4b /tmp/in5b &

cat /tmp/out4a > /tmp/in4b &
cat /tmp/out4b | tee /tmp/in4a > /tmp/in5b &

cat /tmp/out5a > /tmp/in5b &
cat /tmp/out5b | tee /tmp/in5a >  /tmp/in1b &

# Waiting for the link creation (security delay)
sleep 1
