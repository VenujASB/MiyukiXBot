FROM python:3.9.10

WORKDIR /Miyuki
COPY . /Miyuki
 
RUN pip install -r requirements.txt
 
ENTRYPOINT ["python"]
CMD ["-m", "Miyuki"]
