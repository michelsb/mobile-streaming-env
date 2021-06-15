# define a imagem base
FROM alpine:latest

RUN addgroup -g 1000 vlc
RUN adduser --disabled-password --gecos "" -h /data -s /bin/ash -u 1000 -G vlc vlc
# Atualiza a imagem com os pacotes
RUN apk update
# Instala o iw e o wpa-supplicant
RUN apk add iw wireless-tools wpa_supplicant iproute2 bash
# Instala o vlc
RUN apk add vlc

# Expoe a porta 80
EXPOSE 80

USER "vlc"

WORKDIR "/data"
VOLUME ["/data"]

ENTRYPOINT ["/usr/bin/vlc"]
