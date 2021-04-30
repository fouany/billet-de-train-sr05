./bas.py --whatwho --ident=writer --auto --bas-delay=1000 --bas-autosend --bas-dest=NET | \
./net.py --whatwho --ident=writer --auto | \
./net.py --whatwho --ident=reader --auto | \
./bas.py --whatwho --ident=reader --auto
