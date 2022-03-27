FROM ubuntu:20.04
RUN apt-get update \
  && apt-get install -y python3 nginx \
  && cd /usr/bin \
  && ln -s python3 python
ADD ./data /mnt/files
EXPOSE 81
CMD ["python", "-m", "http.server", "-d" ,"/mnt/" ,"81"]