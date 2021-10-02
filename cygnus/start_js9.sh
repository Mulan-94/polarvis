
#!/bin/bash

#Delete the tempfiles that are there
rm -r /home/andati/cygnus_website/public/cygnus/images/tmp/*

# daemon service at /etc/systemd/system/startjs9.service
node $HOME/cygnus_website/public/cygnus/js9install/js9Helper.js
