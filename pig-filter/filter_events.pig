-- Cargar el CSV exportado
events = LOAD '/data/eventos.csv'
    USING PigStorage(',')
    AS (evento_id:chararray, tipo:chararray, subtipo:chararray, calle:chararray, lat:chararray, lon:chararray,
        timestamp:chararray, fecha_evento:chararray, hora_evento:chararray, fuente:chararray, procesado:chararray);

-- Eliminar encabezado (evita considerar la fila de títulos)
data_wo_header = FILTER events BY evento_id != 'evento_id';

-- Filtro avanzado:
--   - Excluye registros SIN tipo (null o string vacío)
--   - Excluye registros SIN lat o lon (null o string vacío)
--   - Puedes agregar más filtros similares aquí (ej: excluye sin calle, fecha, etc.)
filtered = FILTER data_wo_header BY 
    (tipo is not null) AND (tipo != '') AND
    (lat is not null) AND (lat != '') AND
    (lon is not null) AND (lon != '');

-- Eliminar duplicados por evento_id
unique = DISTINCT filtered;

-- Guardar el resultado
STORE unique INTO '/data/eventos_filtrados.csv' USING PigStorage(',');
