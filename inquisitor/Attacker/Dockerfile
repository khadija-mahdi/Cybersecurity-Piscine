FROM debian:bullseye

RUN apt update
RUN apt install -y iproute2 iputils-ping net-tools nmap tcpdump python3 python3-pip libpcap-dev arp-scan
RUN apt install -y zsh curl git wget
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
RUN pip3 install scapy 
   
WORKDIR /app
COPY . /app

CMD ["sleep", "infinity"]
