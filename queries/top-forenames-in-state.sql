SELECT *, 100.0*qnt/SUM(qnt) OVER() as pct
FROM (SELECT name.name, COUNT(*) as qnt
FROM person, has_name, name, city, state
WHERE has_name.person = person.id
AND has_name.name = name.id
AND person.city = city.id
AND city.state = state.id
AND state.name = "RJ"
AND name.type = "Forename"
GROUP BY name.id
ORDER BY qnt DESC)