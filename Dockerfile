FROM mundialis/esa-snap:ubuntu

COPY requirements.txt ./

RUN python3 -m pip install -r requirements.txt
