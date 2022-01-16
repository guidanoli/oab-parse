CREATE VIEW auxview AS
SELECT person.fullname as Nome, city.name as Cidade, state.name as Estado
FROM person, state, city
WHERE person.city = city.id
AND city.state = state.id
