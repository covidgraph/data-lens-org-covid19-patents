FROM debian:stable-slim

# Workaround JRE install bug https://stackoverflow.com/questions/58160597/docker-fails-with-sub-process-usr-bin-dpkg-returned-an-error-code-1
RUN mkdir -p /usr/share/man/man1


#install dependecies
RUN apt update && apt upgrade && apt install -y \
    wget \ 
    curl \
    jq \
    unzip \
    openjdk-11-jre-headless && \
    #curl -sLO https://github.com/neo4j/cypher-shell/releases/download/1.1.13/cypher-shell_1.1.13_all.deb && \
    #dpkg -i cypher-shell_1.1.13_all.deb
    curl -sLO https://github.com/neo4j/cypher-shell/releases/download/4.0.3/cypher-shell_4.0.3_all.deb && \
    dpkg -i cypher-shell_4.0.3_all.deb
RUN mkdir -p /opt/src
WORKDIR /opt/src
COPY ./src .
CMD ["./run.sh"]