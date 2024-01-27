WITH sep_18th_records AS (
SELECT *
FROM public.green_september_2019
WHERE
	lpep_pickup_datetime::DATE = '2019-09-18'::DATE AND
	lpep_dropoff_datetime::DATE = '2019-09-18'::DATE
	
)

SELECT COUNT(1) FROM sep_18th_records