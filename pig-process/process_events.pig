-- pig-process/process_events.pig

-- Cargar el CSV filtrado
events = LOAD '/data/eventos_filtrados.csv'
    USING PigStorage(',')
    AS (
        evento_id:chararray,
        tipo:chararray,
        subtipo:chararray,
        calle:chararray,
        city:chararray,
        lat:chararray,
        lon:chararray,
        timestamp:chararray,
        fecha_evento:chararray,
        hora_evento:chararray,
        fuente:chararray
    );

-- Conteo por tipo de evento
by_type = GROUP events BY tipo;
count_by_type = FOREACH by_type GENERATE group AS tipo, COUNT(events) AS cantidad;
STORE count_by_type INTO '/data/reporte_tipos.csv' USING PigStorage(',');

-- Conteo por calle
by_calle = GROUP events BY calle;
count_by_calle = FOREACH by_calle GENERATE group AS calle, COUNT(events) AS cantidad;
STORE count_by_calle INTO '/data/reporte_calles.csv' USING PigStorage(',');

-- Conteo por día
by_fecha = GROUP events BY fecha_evento;
count_by_fecha = FOREACH by_fecha GENERATE group AS fecha, COUNT(events) AS cantidad;
STORE count_by_fecha INTO '/data/reporte_fechas.csv' USING PigStorage(',');

-- Conteo por city
by_city = GROUP events BY city;
count_by_city = FOREACH by_city GENERATE group AS city, COUNT(events) AS cantidad;
STORE count_by_city INTO '/data/reporte_city.csv' USING PigStorage(',');

-- Conteo por subtipo
by_subtipo = GROUP events BY subtipo;
count_by_subtipo = FOREACH by_subtipo GENERATE group AS subtipo, COUNT(events) AS cantidad;
STORE count_by_subtipo INTO '/data/reporte_subtipos.csv' USING PigStorage(',');
