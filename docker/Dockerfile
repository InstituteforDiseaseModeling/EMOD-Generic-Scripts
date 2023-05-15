FROM ubuntu:20.04
#
RUN apt-get -y upgrade
RUN apt-get -y install python3
RUN apt-get -y install python-pip
#
RUN pip install pip          --upgrade
RUN pip install emodpy==1.21 --extra-index-url https://packages.idmod.org/api/pypi/pypi-production/simple