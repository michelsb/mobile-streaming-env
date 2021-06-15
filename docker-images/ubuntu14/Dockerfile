# define a imagem base
FROM ubuntu:trusty
# Atualiza a imagem com os pacotes
RUN apt-get update -y
# Instala o iw e o wpa-supplicant
RUN apt-get install iw wpasupplicant -y
# Expoe a porta 80
EXPOSE 80
# Comando para iniciar
CMD ["/bin/bash"]
