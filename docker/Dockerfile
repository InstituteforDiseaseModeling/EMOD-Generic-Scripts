FROM almalinux:9.1
#
RUN dnf -y upgrade
RUN dnf -y install python-devel
RUN dnf -y install python-pip
RUN dnf clean all
#
RUN pip install pip          --upgrade
RUN pip install emodpy==1.21 --extra-index-url https://packages.idmod.org/api/pypi/pypi-production/simple