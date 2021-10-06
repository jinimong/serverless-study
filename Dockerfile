FROM amazonlinux:latest
COPY . .
RUN yum update -y
RUN yum install python3.7 -y
RUN pip3 install awscli
