FROM almalinux:9.2-minimal
#
RUN microdnf upgrade -y
#
RUN microdnf -y install python
RUN microdnf -y install python-pip
RUN microdnf clean all
#
RUN pip install pip          --upgrade
RUN pip install emodpy==1.21 --extra-index-url https://packages.idmod.org/api/pypi/pypi-production/simple