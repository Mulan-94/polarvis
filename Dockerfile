FROM ubuntu:22.04
SHELL ["/bin/bash", "-c"]
RUN apt-get update && apt-get upgrade -y

# Install apache2
RUN apt-get install -y apache2 \
    curl \
    wget \
    git \
    openssl

# Install dependencies of cfitsio
RUN apt-get install -y build-essential \
    gfortran \
    libbz2-dev \
    zlib1g-dev \
    libcfitsio-dev \
    libcurl3-dev

RUN apt-get clean; apt-get autoclean


# Install nodejs 16
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

RUN mkdir -p downloads
WORKDIR /downloads

# Download and build cfitsio from source
RUN wget http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio_latest.tar.gz
RUN tar -zxvf cfitsio_latest.tar.gz
RUN mv cfitsio*/ cfitsio
WORKDIR /downloads/cfitsio

# Run executables otherwise you will get an error
RUN ./configure --prefix=/usr/local --enable-sse2 --enable-reentrant
RUN make
RUN make utils
RUN make testprog
RUN make install


# Testing weather this install is ok the output of this should be nothing
RUN testprog > testprog.lis
RUN diff testprog.lis testprog.out
RUN cmp testprog.fit testprog.std
RUN rm cookbook fitscopy imcopy smem speed testprog


# Download and build funtools from source
WORKDIR /downloads
RUN git clone https://github.com/ericmandel/funtools.git funtools
WORKDIR /downloads/funtools
RUN ./mkconfigure
RUN ./configure --prefix=/usr/local
RUN make
RUN make install
RUN make clean

# Download and build regions from source
WORKDIR /downloads
RUN git clone https://github.com/ericmandel/regions.git regions
WORKDIR /downloads/regions
RUN ./configure --prefix=/usr/local --with-cfitsio=/downloads/cfitsio
RUN make
RUN make install

# Download and unzip JS9
WORKDIR /downloads
RUN wget https://js9.si.edu/downloads/js9-3.6.1.tgz
RUN tar -zxvf js9-3.6.1.tgz
RUN mv js9*/ js9

RUN rm -r /var/www/html

# create a directory that will host the website's files
RUN mkdir -p /var/www/example.com

#make a link to it for easy access from home
RUN ln -s /var/www/example.com /home/example.com

# copy polarvis my host machine into this dictionary in the container
COPY to-be-copied/polarvis /home/example.com/polarvis

# make a js9 isntallation directory
RUN mkdir -p /home/example.com/polarvis/js9install

WORKDIR /downloads/js9
# install JS9 into polarvis
RUN ./configure --with-webdir=/home/example.com/polarvis/js9install \
    --with-helper=nodejs \
    --with-cfitsio=/downloads/cfitsio \
    # --prefix=/home/example.com
    --prefix=/usr/local

RUN make
RUN make install

# copy the pref files into the js9install directory
WORKDIR /home/example.com/polarvis
RUN mv js9/js9Prefs.json js9install/
RUN mv js9/js9prefs.js js9install/

# Create a dictionary where to store logs from js9, incase of debugging stuff
RUN mkdir -p /home/logs
RUN echo "echo"
# copy virtual host files to /etc/apache2/sites-available
COPY to-be-copied/vhost-file /etc/apache2/sites-available/example.com.conf

RUN mkdir -p /home/daemons
COPY to-be-copied/start_js9.sh /home/daemons/
# make it executable
RUN chmod +x /home/daemons/start_js9.sh

# copy the daemon service
COPY to-be-copied/daemon.service /etc/systemd/system/startjs9.service

# copy the ssl certs
COPY to-be-copied/example.com-certs /etc/ssl/example.com-certs

WORKDIR /home


# start proxy tunnel modules for apache
RUN a2enmod proxy proxy_http proxy_wstunnel

# enabling https
RUN a2enmod ssl
RUN a2enmod rewrite

# enabling the website
COPY to-be-copied/vhost-file /etc/apache2/sites-available/example.com.conf

RUN a2dissite example.com.conf
RUN a2ensite example.com.conf

RUN apt install -y w3m
RUN apt clean

# # Start apache
# RUN service apache2 start

# In the actual server, run js9helper as a service. This will not work 
# in a docker container
# RUN sysctl start startjs9.service


# start the js9 helper as a bg
RUN a2dissite 000-default.conf

# Expose ports for HTTP (80) and HTTPS (443)
EXPOSE 80
EXPOSE 443

CMD ["/bin/bash", "-c", "/home/daemons/start_js9.sh && apache2ctl -D FOREGROUND"]