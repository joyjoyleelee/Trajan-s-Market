<<<<<<< HEAD
FROM python:3.10.11
ENV HOME /root
WORKDIR /root
COPY . .
# Download dependancies
RUN pip3 install -r requirements.txt
EXPOSE 8080
#Add this for MongoDB
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

=======
FROM python:3.8.2
ENV HOME /root
WORKDIR /root
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait
>>>>>>> origin/front-end-react
CMD /wait && python3 -u server.py