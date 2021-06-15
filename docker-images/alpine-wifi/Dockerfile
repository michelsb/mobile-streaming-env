# define a imagem base
FROM alpine:latest
# Atualiza a imagem com os pacotes
RUN apk update
# Instala o iw e o wpa-supplicant
RUN apk add iw wireless-tools wpa_supplicant iproute2 bash
# Expoe a porta 80
EXPOSE 80
# Comando para iniciar
CMD ["/bin/ash"]
