FROM python:3.6.1
WORKDIR /Zendesk-assignment
ADD . /Zendesk-assignment
RUN pip install -r requirements.txt
CMD ["python", "server.py"]