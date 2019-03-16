SELECT vendor, COUNT(*) as count
FROM requests
GROUP BY vendor;