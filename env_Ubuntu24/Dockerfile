FROM ubuntu:24.04
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
RUN apt-get install git -y
RUN apt-get install libc-dev -y
RUN apt-get install g++ -y
#
RUN apt-get install scons -y
#
RUN apt-get clean
#
RUN git clone https://github.com/InstituteforDiseaseModeling/EMOD-Generic
#
RUN git --git-dir=/EMOD-Generic/.git fetch
RUN git --git-dir=/EMOD-Generic/.git checkout Generic-Ongoing
#
ARG USER=JenkinsUser
#
RUN scons --Release --jobs=4 --Disease=Generic --directory=/EMOD-Generic/
#
RUN mkdir outputs
RUN cp EMOD-Generic/build/x64/Release/Eradication/Eradication outputs/Eradication
#
RUN mkdir outputs/reporter_plugins
RUN cp EMOD-Generic/build/x64/Release/reporter_plugins/*.so outputs/reporter_plugins
#
RUN outputs/Eradication --get-schema --schema-path outputs/schema.json -P EMOD-Generic/Scripts
#
RUN rm -r EMOD-Generic