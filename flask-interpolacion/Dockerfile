FROM flask-dev
USER root
RUN apk add sdl-dev
RUN pip install flask-cors
COPY ./app /app
WORKDIR /app
#ENTRYPOINT [ "/bin/sh","entrypoint.sh" ]
CMD python3 run.py