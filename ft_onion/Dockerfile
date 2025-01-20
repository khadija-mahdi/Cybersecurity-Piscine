# Use debian as base image
FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y nginx openssh-server tor

RUN useradd -m kmahdi && \
    mkdir -p /home/kmahdi/.ssh && \
    chmod 700 /home/kmahdi/.ssh && \
    chown -R kmahdi:kmahdi /home/kmahdi/.ssh



COPY nginx.conf /etc/nginx/sites-available/default
COPY sshd_config /etc/ssh/sshd_config
COPY torrc /etc/tor/torrc
COPY index.html /usr/share/nginx/html/index.html
COPY style.css /usr/share/nginx/html/style.css
COPY script.js /usr/share/nginx/html/script.js

CMD ["sh", "-c", "service tor start && service ssh restart && nginx -g 'daemon off;'"]
