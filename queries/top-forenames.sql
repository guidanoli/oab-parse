SELECT *, 100.0*qnt/SUM(qnt) OVER() as pct
FROM (SELECT name.name, COUNT(*) as qnt
FROM person, has_name, name, city, state
WHERE has_name.person = person.id
AND has_name.name = name.id
AND name.type = "Forename"
GROUP BY name.id
ORDER BY qnt DESC)