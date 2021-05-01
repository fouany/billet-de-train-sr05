# Copie des dossier
cp -R bin ~/AIRPLUG/
cp -R  CLTpy ~/AIRPLUG/
cp -R  GCHpy/ ~/AIRPLUG/

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
