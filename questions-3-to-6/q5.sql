WITH sep_18th_records AS (
SELECT *
FROM public.green_september_2019
WHERE
	lpep_pickup_datetime::DATE = '2019-09-18'::DATE AND
	lpep_dropoff_datetime::DATE = '2019-09-18'::DATE
	
)

SELECT
	"Borough",
	SUM(total_amount)
FROM
	sep_18th_records
	INNER JOIN
	public.zones
	ON
	sep_18th_records."PULocationID" =
	public.zones."LocationID"
GROUP BY "Borough"
HAVING SUM(total_amount) > 50000