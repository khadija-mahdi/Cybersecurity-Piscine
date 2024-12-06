# Use debian as base image
FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y nginx openssh-server tor && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create user, setup .ssh directory, and set permissions
RUN useradd -m kmahdi && \
    mkdir -p /home/kmahdi/.ssh && \
    chmod 700 /home/kmahdi/.ssh && \
    chown -R kmahdi:kmahdi /home/kmahdi/.ssh

COPY id_rsa.pub /home/kmahdi/.ssh/authorized_keys
RUN chown kmahdi:kmahdi /home/kmahdi/.ssh/authorized_keys && \
    chmod 600 /home/kmahdi/.ssh/authorized_keys

# Copy configuration files
COPY nginx.conf /etc/nginx/sites-available/default
COPY sshd_config /etc/ssh/sshd_config
COPY torrc /etc/tor/torrc
COPY index.html /usr/share/nginx/html/index.html
COPY style.css /usr/share/nginx/html/style.css
COPY script.js /usr/share/nginx/html/script.js

EXPOSE 80 4242

# Start SSH and other services
CMD ["sh", "-c", "service tor start && service ssh restart && nginx -g 'daemon off;'"]
