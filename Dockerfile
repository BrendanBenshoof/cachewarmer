FROM python:3

COPY . /usr/src/app/
WORKDIR /usr/src/app/

ENTRYPOINT [ "python3", "pyhp_server.py" ]
CMD [ "8001" ]
