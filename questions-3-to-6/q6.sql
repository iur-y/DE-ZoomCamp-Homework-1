WITH pickups_at_astoria AS (
SELECT *
FROM 
	public.green_september_2019
	INNER JOIN
	public.zones
	ON
		public.green_september_2019."PULocationID" =
		public.zones."LocationID"
WHERE public.zones."Zone" = 'Astoria'
),

largest_astoria_tip AS (
SELECT tip_amount, "DOLocationID"
FROM pickups_at_astoria
WHERE
	lpep_pickup_datetime::DATE
	BETWEEN
		'2019-09-01'::DATE AND
		'2019-09-30'::DATE
ORDER BY tip_amount DESC
LIMIT 1
)

SELECT "Zone"
FROM
	largest_astoria_tip
	INNER JOIN
	public.zones
	ON
		largest_astoria_tip."DOLocationID" =
		public.zones."LocationID"
