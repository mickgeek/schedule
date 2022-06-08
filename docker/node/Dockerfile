FROM node:17-alpine

EXPOSE 3000

COPY ./docker-entrypoint.sh /usr/local/bin/
RUN chmod 755 /usr/local/bin/docker-entrypoint.sh

WORKDIR /home/schedule/
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["node"]
