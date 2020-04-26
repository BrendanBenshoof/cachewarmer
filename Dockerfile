FROM python:3

COPY ./requirements.txt /usr/src/app/
WORKDIR /usr/src/app/
RUN pip install -r requirements.txt --no-cache-dir

COPY . /usr/src/app/

ENTRYPOINT [ "python3", "pyhp_server.py" ]
CMD [ "8001" ]
