FROM nvcr.io/nvidia/pytorch:22.08-py3

RUN echo -e "[global]\nindex-url = https://pypi.doubanio.com/simple\ntrusted-host = pypi.doubanio.com\n" > ~/.pip/pip.conf

COPY . .
RUN pip install -r requirements.txt && pip install cython 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'

RUN apt-get update && DEBIAN_FRONTEND="noninteractive" apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -r YOLOX/requirements.txt
RUN YOLOX
RUN python YOLOX/setup.py develop
