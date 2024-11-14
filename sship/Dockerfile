FROM python:3.14.0a1-slim
RUN apt-get update
RUN apt-get install zip unzip -y
RUN apt-get install openssh-server -y
RUN useradd -m -p $(perl -e 'print crypt("password", "salt")') 'Ship'
RUN useradd -m -p $(perl -e 'print crypt("password", "salt")') 'Captain'
RUN useradd -m -p $(perl -e 'print crypt("password", "salt")') 'Engineer'
RUN useradd -m -p $(perl -e 'print crypt("password", "salt")') 'Weapons'
WORKDIR /home/Ship
RUN touch resolv
COPY . .
RUN cp ./.profile /home/Captain/.profile
RUN cp ./.profile /home/Engineer/.profile
RUN cp ./.profile /home/Weapons/.profile
RUN chmod +x ./entrypoint.sh
EXPOSE 22
ENV TERM=xterm
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN sed -i 's/#ListenAddress 0.0.0.0/ListenAddress 0.0.0.0/' /etc/ssh/sshd_config
RUN service ssh start
ENTRYPOINT ["./entrypoint.sh"]
