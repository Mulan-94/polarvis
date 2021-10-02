#http://ratt.radiopadre.net/cygnus/

curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -

sudo apt-get install -y nodejs build-essential

sudo apt install libcfitsio-dev \
  gfortran \
  build-essential \
  zlib1g-dev \
  libbz2-dev \
  libcurl3-dev

sudo apt-get clean; sudo apt-get autoclean

#########################################################################
#		Installing CFITSIO
#########################################################################

wget http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio_latest.tar.gz

tar xf cfitsio_latest.tar.gz

cd cfitsio-X.XX

#generate various build files
./configure --prefix=/usr/local --enable-sse2 --enable-reentrant

#build the cfitsio files
make

make utils

# test whether the installation is fine
make testprog

sudo make install

./testprog > testprog.lis

diff testprog.lis testprog.out

cmp testprog.fit testprog.std

make clean

#copy whatever version of cfitsio linked object to /usr/lib as libcfitsio.so.9
sudo cp /usr/local/lib/libcfitsio.so.9.4.0.0 /usr/lib/libcfitsio.so.9


#########################################################################
#		Installing JS9
#########################################################################
cd ~/cygnus_website/public/cygnus/images

#ln -s /data/andati/images/nh-CYG-0.75-SLO-I.FITS 

cd ~/cygnus_website/public/cygnus/js9install/
rm -r *

tar -xf ~/cygnus_website/install_files/compressed/js9-3.6.1.tgz --directory .
mv js9-3.6.1/* .
rm -r js9-3.6.1


#rm -r ~/cygnus_website/bin/ ~/cygnus_website/include/ ~/cygnus_website/lib/

./configure --with-webdir=/$HOME/cygnus_website/public/cygnus/js9install --with-helper=nodejs --with-cfitsio=/usr/local/ --prefix=$HOME/cygnus_website

make

make install

rm js9Prefs.json js9prefs.js
ln -s ../js9/js9Prefs.json
ln -s ../js9/js9prefs.js
ln -s ../images data

#export PATH=/usr/local/lib:$PATH
export PATH=$HOME/cygnus_website/bin:$PATH


DEBUG="*" node $HOME/cygnus_website/public/cygnus/js9install/js9Helper.js 1> $HOME/cygnus_website/logs/js9node.log 2>&1&

rm $HOME/cygnus_website/logs/js9node.loghttp://ratt.radiopadre

#js9 install directory must be at homeeee!!!!!!!!!!1
ln -s ~/cygnus_website/public/cygnus/js9install/


grep -i exec: $HOME/cygnus_website/logs/js9node.log

ps guwax | egrep -i js9Helper

To debug rep file generation

uncomment line 2 of  js9install/analysis-wrappers/jsXeq
exec 1>$HOME/notfoo.log
echo "This is a testtingaglrflwslfmalnrtliahrlaht"

https://unix.stackexchange.com/questions/426862/proper-way-to-run-shell-script-as-a-daemon
https://stackoverflow.com/questions/37585758/how-to-redirect-output-of-systemd-service-to-a-file

PUT daemon at 

/etc/systemd/system/startjs9.service


systemctl status -l startjs9.service

start daemon at
sudo systemctl start startjs9.service
sudo systemctl stop startjs9.service

To always start at reboot
sudo systemctl enable startjs9.service

To disable
sudo systemctl enable startjs9.service
