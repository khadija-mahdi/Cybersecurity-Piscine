FROM debian:bullseye

RUN apt update && apt install -y vsftpd net-tools

COPY vsftpd.conf /etc/vsftpd.conf

RUN useradd -m ftpuser && echo "ftpuser:password" | chpasswd

CMD ["vsftpd", "/etc/vsftpd.conf"]
