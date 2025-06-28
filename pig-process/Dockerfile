FROM openjdk:8-jdk

RUN apt-get update && \
    apt-get install -y wget unzip && \
    wget https://downloads.apache.org/pig/pig-0.17.0/pig-0.17.0.tar.gz && \
    tar -xvzf pig-0.17.0.tar.gz -C /opt && \
    rm pig-0.17.0.tar.gz && \
    ln -s /opt/pig-0.17.0 /opt/pig

ENV PATH="/opt/pig/bin:$PATH"

WORKDIR /scripts

COPY process_events.pig .
COPY wait-for-file.sh .
RUN chmod +x /scripts/wait-for-file.sh

ENTRYPOINT ["/scripts/wait-for-file.sh"]
CMD ["/data/eventos_filtrados.csv/part-r-00000", "60", "pig", "-x", "local", "process_events.pig"]

