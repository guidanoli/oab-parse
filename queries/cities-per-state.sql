SELECT state.name as Estado, count(city.id) as QtdCidades
FROM city, state
WHERE city.state = state.id
GROUP BY state.id
ORDER BY QtdCidades DESC