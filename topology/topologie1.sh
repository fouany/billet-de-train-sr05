#!/bin/bash

# Create named pipes, one input and one output per process.
mkfifo in1 out1
mkfifo in2 out2
mkfifo in3 out3
mkfifo in4 out4
mkfifo in5 out5
mkfifo in6 out6
mkfifo in7 out7

# Starting the processes
./bas.py --auto --ident=node1 --whatwho --begin=CLT --dest=CLT < in1 > out1 &
./clt.py --auto --ident=node1 --whatwho --begin=BAS < /tmp/in1b > /tmp/out1b &
./bas.py --auto --ident=node1 --whatwho --begin=CLT --dest=CLT < /tmp/in2a > /tmp/out2a &
./clt.py --auto --ident=node1 --whatwho --begin=BAS < /tmp/in1b > /tmp/out1b &
./bas.py --auto --ident=node1 --whatwho --begin=CLT --dest=CLT < /tmp/in1a > /tmp/out1a &
./clt.py --auto --ident=node1 --whatwho --begin=BAS < /tmp/in1b > /tmp/out1b &
./bas.py --auto --ident=node1 --whatwho --begin=CLT --dest=CLT < /tmp/in1a > /tmp/out1a &
./clt.py --auto --ident=node1 --whatwho --begin=BAS < /tmp/in1b > /tmp/out1b &
./bas.py --auto --ident=node1 --whatwho --begin=CLT --dest=CLT < /tmp/in1a > /tmp/out1a &
./clt.py --auto --ident=node1 --whatwho --begin=BAS < /tmp/in1b > /tmp/out1b &
./bas.py --auto --ident=node1 --whatwho --begin=CLT --dest=CLT < /tmp/in1a > /tmp/out1a &
./clt.py --auto --ident=node1 --whatwho --begin=BAS < /tmp/in1b > /tmp/out1b &
./bas.py --auto --ident=node1 --whatwho --begin=CLT --dest=CLT < /tmp/in1a > /tmp/out1a &
./clt.py --auto --ident=node1 --whatwho --begin=BAS < /tmp/in1b > /tmp/out1b &


# Waiting for the link creation (security delay)
sleep 1

# Links creation: output -> input
# 1 -> 2 and 3
cat out1 | tee in2 in3 &
# 2 -> 1, 4 and 5
cat out2 | tee in1 in4 in5 &
# 3 -> 1 and 6
cat out3 | tee in1 in6 &
# 4 -> 2, 5 and 7
cat out4 | tee in2 in5 in7 &
# 5 -> 2 and 4
cat out5 | tee in2 in4 &
# 6 -> 3 and 7
cat out6 | tee in3 in7 &
# 7 -> 4 and 6
cat out7 | tee in4 in6 &


# Killing all applications
#killall wha.py cat tee

# Deleting all named pipes
#rm in* out*
