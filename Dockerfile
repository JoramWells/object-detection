
FROM tensorflow/tensorflow



WORKDIR /tf



COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY . ./

EXPOSE 8000

CMD ["bash","entrypoint.prod.sh"]
