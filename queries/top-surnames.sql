SELECT name.name, COUNT(*) as "#"
FROM person, has_name, name
WHERE has_name.person = person.id
AND has_name.name = name.id
AND name.type = "Surname"
/* Ignore prepositions */
AND name.name != "De"
AND name.name != "Da"
AND name.name != "Das"
AND name.name != "Do"
AND name.name != "Dos"
/***********************/
GROUP BY name.id
ORDER BY "#" DESC