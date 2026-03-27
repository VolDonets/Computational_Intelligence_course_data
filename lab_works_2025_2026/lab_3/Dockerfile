FROM ubuntu:22.04
# Install system dependencies
RUN apt-get update && apt-get install -y openssh-server net-tools python3 python3-pip

# Setup SSH
RUN mkdir /var/run/sshd
RUN echo 'root:1234' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

# Set up the application directory
WORKDIR /app

# Copy your Python script and the startup script
# `COPY requirements.txt /app/requirements.txt
# Also, here you can `RUN pip3 install requirements.txt` -- check with GenAI this command
COPY async_server.py /app/async_server.py
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose both SSH and the TCP Server port
EXPOSE 22 8888

# Run the wrapper script
CMD ["/app/start.sh"]
