use Sakila;

-- 1a. first/last names of all actors
Select first_name, last_name from actor;

-- 1b. first/last name in single column in upper case
Select concat(actor.first_name, ' ' , actor.last_name) as 'Actor Name' from actor;

-- 2a. ID, first/last names with first name = Joe
Select actor_id, first_name, last_name from actor
where first_name = 'Joe';

-- 2b. All actors with last name containing "gen"
Select first_name, last_name from actor
where last_name like '%GEN%';

-- 2c. all actors with last name containing "LI", reverse first/last name column order
Select last_name, first_name from actor
where last_name like '%LI%';

-- 2d. Use IN to display country_id and country for Afghanistan, Bangladesh, China
Select country_id, country from country
where country in ('Afghanistan', 'Bangladesh', 'China');

-- 3a. Add column "description" as BLOB to actor table
Alter table actor
add description BLOB;
select * from actor;

-- 3b. Delete column from previous step
Alter table actor
drop column description;
select * from actor;

-- 4a. count of actor last names
SElect last_name, count(last_name) from actor
group by last_name;

-- 4b. same as above, but filter for shared names
SElect last_name, count(last_name) from actor
group by last_name
having count(last_name) > 1;

-- 4c. fix groucho williams to harbo williams
SET SQL_SAFE_UPDATES = 0;
Update actor
set first_name = "HARPO"
where first_name = "GROUCHO";

-- 4d. change the name back
Update actor
set first_name = "GROUCHO"
where first_name = "HARPO";

-- 5a. recreate address table schema
Show create table address;

-- 6a. show staff member name and address
Select staff.first_name, staff.last_name, address.address from address
JOIN staff on staff.address_id = address.address_id;

-- 6b. total amount rung up by each staff member
select staff.first_name, staff.last_name, sum(payment.amount) from payment
Join staff on staff.staff_id = payment.staff_id
where payment_date like "2005-08%"
group by first_name, last_name;

-- 6c. list film name and count of actors in film
select count(film_actor.actor_id), film.title from film
Join film_actor on film_actor.film_id = film.film_id
group by title;

-- 6d. # copies of Hunchback Impossible
select film.title, count(inventory.inventory_id) from inventory
Join film on film.film_id = inventory.film_id
where film.title = 'HUNCHBACK IMPOSSIBLE'
group by film.title;

-- 6e. list total paid by each customer alphabetically
select customer.last_name, customer.first_name, sum(payment.amount) from payment
Join customer on customer.customer_id = payment.customer_id
group by last_name, first_name;

-- 7a. Movies that start with "K" and "Q" in English
SELECT title
FROM film
WHERE (title like 'K%' OR title like 'Q%')
AND language_id IN
(
  SELECT distinct language_id
  FROM language
  WHERE name = "English"
  );
  
-- 7b. All actor in "Alone Trip"
SELECT first_name, last_name
FROM actor
WHERE actor_id IN
(
  SELECT actor_id
  FROM film_actor
  WHERE film_id IN
  (
   SELECT film_id
   FROM film
   WHERE title = 'ALONE TRIP'
  )
);

-- 7c. Names and emails of Canadian customers
SELECT first_name, last_name
FROM customer
WHERE address_id IN
(
  SELECT address_id
  FROM address
  WHERE city_id IN
  (
   SELECT city_id
   FROM city
   WHERE country_id IN
   (
   SELECT country_id
   FROM country
   WHERE country = 'Canada'
   )
  )
);

-- 7d. Movie names categorized as family films
SELECT title
FROM film
WHERE film_id IN
(
  SELECT film_id
  FROM film_category
  WHERE category_id IN
  (
   SELECT category_id
   FROM category
   WHERE name = 'Family'
  )
);

-- 7e. Most frequently rented movies in descending order
SELECT film.title, count(rental.rental_id) as rent_count
  FROM film
  JOIN inventory ON film.film_id = inventory.film_id
  JOIN rental  ON inventory.inventory_id = rental.inventory_id
  group by title
  order by rent_count desc;
  
-- 7f. $$ each store brought in 
  Select store.store_id, sum(payment.amount) as total_payment
  From payment
  Join store on payment.staff_id = store.manager_staff_id
  group by store_id;
  
  -- 7g. Query to display each store by ID, city, country
  Select store.store_id, city.city, country.country from store
  join address on store.address_id = address.address_id
  join city on address.city_id = city.city_id
  join country on city.country_id = country.country_id
  group by store_id;
  
  -- 7h. Top five genres in gross revenue
  Select category.name, sum(payment.amount) as gross_rev from category
  Join film_category on category.category_id = film_category.category_id
  join inventory on film_category.film_id = inventory.film_id
  join rental on inventory.inventory_id = rental.inventory_id
  join payment on rental.rental_id = payment.rental_id
  group by name
  order by gross_rev desc
  limit 5;
  
-- 8a. Create view of top 5 genres
Create view Top5Genres as
  Select category.name, sum(payment.amount) as gross_rev from category
  Join film_category on category.category_id = film_category.category_id
  join inventory on film_category.film_id = inventory.film_id
  join rental on inventory.inventory_id = rental.inventory_id
  join payment on rental.rental_id = payment.rental_id
  group by name
  order by gross_rev desc
  limit 5;
  
-- 8b. Display view
SELECT * FROM Top5Genres;

-- 8c. Delete view
DROP VIEW Top5Genres;