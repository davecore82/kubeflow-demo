FROM tensorflow/serving:latest
RUN apt-get update && apt-get install -y  python-pip
RUN pip install kafka-python requests numpy pandas

COPY source/ /usr/bin/



ENTRYPOINT ["/usr/bin/entrypoint.sh"]
 

