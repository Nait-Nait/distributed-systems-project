#!/bin/bash
FILE=$1
TIMEOUT=${2:-60}  

echo "Esperando archivo: $FILE"
for i in $(seq 1 $TIMEOUT); do
    if [ -f "$FILE" ]; then
        echo "Archivo encontrado: $FILE"
        exec "${@:3}"  
        exit 0
    fi
    sleep 1
done

echo "Timeout esperando $FILE"
exit 1
