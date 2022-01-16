SELECT city.name as Cidade, count(person.id) as QtdPessoas
FROM person, city
WHERE person.city = city.id
GROUP BY city.id
ORDER BY QtdPessoas DESC
