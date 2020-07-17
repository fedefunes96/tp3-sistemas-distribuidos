# COVID19-Statistics

Para utilizar este sistema, basta con ingresar el archivo de datos nombrado **data.csv** en la carpeta data dentro de **chunk_manager**, los resultados serán escritos en el archivo: **summary_controller/summary/summary.txt**

Para correr el programa, ejecutar:

**make docker-compose-up map_workers=< TotalMapWorkers > date_workers=< TotalDateWorkers > count_workers=< TotalCountWorkers >  processors= < TotalProcessors >**

Indicando la cantidad de trabajadores que se utilizarán.

Además, el cliente se corre con:
**make client-run processors=< TotalProcessors > && make client-logs**