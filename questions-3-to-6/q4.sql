SELECT lpep_pickup_datetime::DATE
FROM public.green_september_2019
ORDER BY trip_distance DESC
LIMIT 1