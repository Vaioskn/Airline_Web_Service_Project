FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install flask pymongo
RUN mkdir /app
RUN mkdir -p /app/data
COPY e20081_Airline_Service.py /app/e20081_Airline_Service.py
ADD data /app/data
EXPOSE 5000
WORKDIR /app
ENTRYPOINT [ "python3","-u", "e20081_Airline_Service.py" ]
