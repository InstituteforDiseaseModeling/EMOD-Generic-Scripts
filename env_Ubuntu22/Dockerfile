FROM ubuntu:22.04
#
RUN apt-get update
RUN apt-get install software-properties-common -y
RUN apt-get update
RUN add-apt-repository universe
RUN apt-get upgrade -y
#
RUN apt-get clean
#
RUN apt-get install python3-dev -y
RUN apt-get install libmpich-dev -y
RUN apt-get install libsqlite3-dev -y
RUN apt-get install libboost-dev -y
RUN apt-get install git -y
RUN apt-get install libc-dev -y
RUN apt-get install g++ -y
#
RUN apt-get install scons -y
#
RUN apt-get clean
#
RUN git clone https://github.com/kfrey-idm/EMOD
#
RUN git --git-dir=/EMOD/.git fetch
RUN git --git-dir=/EMOD/.git checkout Generic-Ongoing
#
ARG USER=CalculonUser-EMOD
#
RUN scons --Release --jobs=4 --Disease=Generic --directory=/EMOD/
#
RUN mkdir outputs
RUN cp EMOD/build/x64/Release/Eradication/Eradication outputs/Eradication
#
RUN mkdir outputs/reporter_plugins
RUN cp EMOD/build/x64/Release/reporter_plugins/*.so outputs/reporter_plugins
#
RUN outputs/Eradication --get-schema --schema-path outputs/schema.json -P EMOD/Scripts
#
RUN rm -r EMOD