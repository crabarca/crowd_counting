SELECT vendor, COUNT(*) as freq
FROM (
	SELECT DISTINCT macaddr, vendor
	FROM requests
	)
GROUP BY vendor;
