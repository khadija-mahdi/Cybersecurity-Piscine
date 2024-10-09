FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y nginx openssh-server tor && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY nginx.conf /etc/nginx/sites-available/default
COPY sshd_config /etc/ssh/sshd_config
COPY torrc /etc/tor/torrc
COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80 4242

CMD ["sh", "-c", "service tor start && service ssh start && nginx -g 'daemon off;'"]
# tor-webserver/Dockerfile
