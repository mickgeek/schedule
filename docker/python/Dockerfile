FROM python:3.9.10-alpine

EXPOSE 5000

COPY ./docker-entrypoint.sh /usr/local/bin/
RUN chmod 755 /usr/local/bin/docker-entrypoint.sh

WORKDIR /home/schedule/
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python"]
