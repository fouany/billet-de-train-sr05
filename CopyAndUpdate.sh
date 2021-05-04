# Copie des dossier
cp -R bin ~/AIRPLUG/
cp -R  CLTpy ~/AIRPLUG/
cp -R  GCHpy/ ~/AIRPLUG/
# copie des mod
cp mods/billet_mod.py  ~/AIRPLUG/LIBAPGpy/LIBAPGpy/
cp mods/msg_mod.py ~/AIRPLUG/LIBAPGpy/LIBAPGpy/
cp mods/outil_mod.py ~/AIRPLUG/LIBAPGpy/LIBAPGpy/
cp mods/snap_mod.py ~/AIRPLUG/LIBAPGpy/LIBAPGpy/
cp libapg.py ~/AIRPLUG/LIBAPGpy/LIBAPGpy/

# on va dans bin
cd ~/AIRPLUG/bin/

#update
source config.sh
source updateCLT.sh
source updateGCH.sh
#execution
chmod +x ring.sh
chmod +x ring-4.sh

#creation de tmp
mkdir tmp
