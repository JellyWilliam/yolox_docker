# YOLOX Docker

1) Склонировать YOLOX, скачать модель (веса):
   
    git clone git@github.com:Megvii-BaseDetection/YOLOX.git
2) Собрать образ:

    docker build -f .\Dockerfile.yolox -t yolox
3) Внутри контейнера открыть консоль:
    
    docker run -it yolox bash
4) Далее выполняем необходимые скрипты внутри контейнера
   
(docker cp <containerId>:/file/path/within/container /host/path/target - для сохранения результатов)