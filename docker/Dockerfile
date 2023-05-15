FROM ubuntu:20.04
#
RUN apt-get update
#
RUN apt-get -y install software-properties-common 
RUN apt-get update
RUN add-apt-repository universe
#
RUN apt-get -y upgrade
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
#
RUN pip3 install pip          --upgrade
RUN pip3 install emodpy==1.21 --extra-index-url https://packages.idmod.org/api/pypi/pypi-production/simple