# define a imagem base
FROM ubuntu:latest
# Atualiza a imagem com os pacotes
RUN apt-get update -y
# Instala o iw e o wpa-supplicant
RUN apt-get install iw wireless-tools wpasupplicant iproute2 iputils-ping -y
# Expoe a porta 80
EXPOSE 80
# Comando para iniciar
CMD ["/bin/bash"]
