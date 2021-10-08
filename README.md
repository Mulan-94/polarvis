# polarvis
Musings on Polarimetric Vis

This is a repo for a website residing at: https://cygnus.ratt.center/cygnus. It gives an interactive visual representation of, among other things, fractional polarisation of various lines of sight on the Cygnus-A galaxy. The website is based on work done by Sebokolodi Et. Al (2020) in: A Wideband Polarization Study of Cygnus A with the Jansky Very Large Array. I. The Observations and Data. The FITS viewer used is JS9, which is browser based, and the server is Apache running on Linux. The requirements to setup are:
1. JS9
2. CFITSIO
3. Apache
4. Nodejs

## Setting Up Apache 
In the case of a limited number of public facing ports on a machine or a single port, set up a proxy server that tunnels traffic from the public port to the internal required port. This setup, which is included at **site.conf**, needs to be added to the apache virtual host file for the site, in addition to the basic virtual host configuration 

**N.B For the config file in this repo to become useful, the value XX on line 1 must be set to the public facing port number, e.g. 80 or 8080 or whatever, and from line 30-44, xxxx must be changed to a valid port number at which the js9helper will listen.**

The virtual host config files are found in `/etc/apache2/sites-available`. In the presence of a less constrained setup, the proxy arrangement is not necessary. The proxy module must then be enabled using

`sudo a2enmod proxy proxy_http proxy_wstunnel`

Enable the site:

`sudo a2ensite cygnus.ratt-ru.org.conf`

And then the server can be restarted by:

`sudo service apache2 reload`

Apache uses **.htaccess** files for access control. With these files, you can set up what is/isn't visible to the public by using the <Directory> directives. These can also be used to setup custom error pages for various HTTP status codes.

## Installing Nodejs

To install nodejs version 14, or whatever version:
```
curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -`

sudo apt-get install -y nodejs build-essential
```

## Setting Up JS9
It is necessary to load up smaller versions of FITS files for the purpose of visualisation only, while availing the entire image when necessary to run any image analysis. Smaller images mean faster loading time and less bandwidth for user. JS9 gives this functionality by use of representation files, which requires the presence of CFITSIO. The following commands can be used to install CFITSIO:

```
#To avoid errors
sudo apt-get install libcfitsio-dev

#Install a fortran compiler to avoid some errors
sudo apt install gfortran

#C compilation toolchain
sudo apt install build-essential
```

These are dependents required for CFITSIO to work properly. The download and install:

```
wget http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio_latest.tar.gz

tar xf cfitsio_latest.tar.gz

cd cfitsio-X.XX                   # Replace X.XX with version

#generate various build files
 ./configure --prefix=/usr/local --enable-sse2 --enable-reentrant

#build the cfitsio files
make

make utils

# test whether the installation is fine
make testprog

sudo make install
#if you don't run make install with sudo, you will get permission errors. 
#If you try to test testprog before install, you will get an error shared library not found.

 ./testprog > testprog.lis

diff testprog.lis testprog.out

cmp testprog.fit testprog.std

rm cookbook fitscopy imcopy smem speed testprog
```

Then install JS9. It can be downloaded from: https://js9.si.edu/downloads/ or from its Github repo.

```
./configure --with-webdir=/home/your/desired/installation/path \
                  --with-helper=nodejs \
                  --with-cfitsio=/usr/local/ \
                  --prefix=$HOME``

#build the JS9 system
make

#install JS9 to web tree

make install

#Clean up after install
make clean
```

## JS9 Site Preferences
After install, the JS9 site can be configured by files in your JS9 directory called JS9prefs.js/ json. These setup the intial state of the JS9 and can still be modified later. JS9 uses a backend nodejs server, called js9helper.js to generated representation files mentioned earlier. This server must be up and running for this to happen. A port is needed to enable js9helper listen for requests. Note that in the case of a proxy service in use, the client will listen at the public facing port (set this in js9Prefs.json), while the js9helper will listen at the private ports (set this in js9prefs.js) See https://js9.si.edu/js9/help/preferences.html and https://js9.si.edu/js9/help/helper.html for more details. The server is started as:

`nodejs js9/install/dir/js9helper.js`

The symbol `&` can be added at the end of this command to make it run in the background. Debugging can also be activated in 2 ways:
1. In js9prefs.js, set `globalOpts.debug` to any number greater than 0.
2. Run the server as follows: `DEBUG='*' nodejs js9Helper.js`
