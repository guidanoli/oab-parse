CREATE VIEW auxview AS
SELECT person.name as nome, city.name as cidade, state.name as estado
FROM person, state, city
WHERE person.city = city.id
AND city.state = state.id