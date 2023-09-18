FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install flask pymongo
RUN mkdir /app
RUN mkdir -p /app/data
COPY Airline_Service.py /app/Airline_Service.py
ADD data /app/data
EXPOSE 5000
WORKDIR /app
ENTRYPOINT [ "python3","-u", "Airline_Service.py" ]
