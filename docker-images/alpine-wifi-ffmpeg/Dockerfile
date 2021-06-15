# define a imagem base
FROM alpine:latest

#RUN addgroup -g 1000 ffmpeg
#RUN adduser --disabled-password --gecos "" -h /data -s /bin/ash -u 1000 -G ffmpeg ffmpeg
# Atualiza a imagem com os pacotes
RUN apk update
# Instala o iw e o wpa-supplicant
RUN apk add iw wireless-tools wpa_supplicant iproute2 bash
# Instala o ffmpeg
RUN apk add ca-certificates ffmpeg libva-intel-driver
RUN rm -rf /var/cache/*

# Expoe a porta 80
EXPOSE 80

#USER "ffmpeg"

WORKDIR "/data"
VOLUME ["/data"]

# Comando para iniciar
CMD ["/bin/ash"]
#ENTRYPOINT ["/usr/bin/ffmpeg"]
