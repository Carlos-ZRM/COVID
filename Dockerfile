FROM python:alpine3.7

RUN  apk add --no-cache gcc gfortran build-base libffi-dev freetype freetype-dev curl python3 python3-dev libgfortran libpng lapack openblas-dev sdl-dev openjpeg-dev py-pillow jpeg-dev 
RUN pip3 install --upgrade pip
RUN pip install  --no-cache-dir flask flask-cors 
RUN pip install  --no-cache-dir numpy 
RUN pip install  --no-cache-dir pandas
RUN pip install  --no-cache-dir cython
RUN pip install --no-cache-dir matplotlib 
RUN pip install  --no-cache-dir Pillow
COPY ./app/ /app
WORKDIR /app
CMD python3 run.py
