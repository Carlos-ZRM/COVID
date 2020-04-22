FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN  apk add --no-cache build-base libffi-dev freetype freetype-dev curl python3 python3-dev libgfortran libpng
RUN pip3 install --upgrade pip
RUN pip3 install  -r requirements.txt
RUN pip3 install matplotlib
EXPOSE 5000
RUN  python3 run.py
#RUN echo "*/1 * * * * python3 /app/sslcheck.py >> ~/cron.log 2>&1" > crontab.tmp
#RUN crontab crontab.tmp
#RUN crond start
#CMD python ./index.py
#ENTRYPOINT [ "/bin/sh","entrypoint.sh" ]
#ENTRYPOINT ["crond start"]