DATE_RESUMER_JAN_WORKER = "date_resumer_jan"
CITY_RESUMER_AM_WORKER = "city_resumer_am"
COUNT_RESUME_WORKER = "count_resume"
MAP_WORKER = "map_worker"
COUNT_WORKER = "count_worker"
DATE_WORKER = "date_worker"
MASTER_MAP_WORKER = "master_map_worker"
MASTER_DATE_WORKER = "master_date_worker"
MASTER_COUNT_WORKER = "master_count_worker"
DATE_SORTER_WORKER = "date_sorter"
TOP_CITIES_WORKER = "top_cities"
SUMMARY_WORKER = "summary_worker"

WORKER_TYPES = [
    DATE_RESUMER_JAN_WORKER,
    CITY_RESUMER_AM_WORKER,
    COUNT_RESUME_WORKER,
    MAP_WORKER,
    COUNT_WORKER,
    DATE_WORKER,
    MASTER_MAP_WORKER,
    MASTER_DATE_WORKER,
    MASTER_COUNT_WORKER,
    DATE_SORTER_WORKER,
    TOP_CITIES_WORKER,
    SUMMARY_WORKER
]

WORKER_MIN_NODES = {
    DATE_RESUMER_JAN_WORKER: 2,
    CITY_RESUMER_AM_WORKER: 2,
    COUNT_RESUME_WORKER: 2
    MAP_WORKER: 2,
    COUNT_WORKER: 2,
    DATE_WORKER: 2,
    MASTER_MAP_WORKER: 2,
    MASTER_DATE_WORKER: 2,
    MASTER_COUNT_WORKER: 2,
    DATE_SORTER_WORKER: 2,
    TOP_CITIES_WORKER: 2,
    SUMMARY_WORKER: 2     
}
