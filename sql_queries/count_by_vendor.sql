SELECT vendor, COUNT(*)
FROM requests
GROUP BY vendor;