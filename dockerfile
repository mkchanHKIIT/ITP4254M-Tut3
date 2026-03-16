FROM python:3.10.2
 
WORKDIR /
 
ADD . /
 
RUN pip install -r requirements.txt
 
CMD python server.py