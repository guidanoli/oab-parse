SELECT state.name as Estado, count(person.id) as QtdPessoas
FROM person, city, state
WHERE person.city = city.id
AND city.state = state.id
GROUP BY state.id
ORDER BY QtdPessoas DESC
