/*
 Завдання на SQL до лекції 03.
 */


/*
1.
Вивести кількість фільмів в кожній категорії.
Результат відсортувати за спаданням.
*/
WITH film_count_by_category AS (SELECT category_id, COUNT(*) AS count
                                FROM film_category
                                GROUP BY category_id)
SELECT c.name, f.count
FROM category c
         JOIN film_count_by_category f
              ON c.category_id = f.category_id
ORDER BY 2 DESC;


/*
2.
Вивести 10 акторів, чиї фільми брали на прокат найбільше.
Результат відсортувати за спаданням.
*/
WITH films_count_by_actor AS (SELECT fa.actor_id, COUNT(*) AS count
                              FROM rental r
                                       JOIN inventory i
                                            ON r.inventory_id = i.inventory_id
                                       JOIN film_actor fa
                                            ON i.inventory_id = fa.film_id
                              GROUP BY fa.actor_id)
SELECT a.first_name, a.last_name, fc.count
FROM films_count_by_actor fc
         JOIN actor a
              ON fc.actor_id = a.actor_id
ORDER BY 3 DESC
LIMIT 10;


/*
3.
Вивести категорію фільмів, на яку було витрачено найбільше грошей
в прокаті
*/
WITH box_office_by_category_id AS (SELECT fc.category_id AS category_id,
                                          SUM(p.amount)  AS box_office_sum
                                   FROM rental r
                                            JOIN inventory i
                                                 ON r.rental_id = i.inventory_id
                                            JOIN film_category fc
                                                 ON i.film_id = fc.film_id
                                            JOIN payment p
                                                 ON r.rental_id = p.rental_id
                                   GROUP BY fc.category_id)
SELECT c.name
FROM box_office_by_category_id bo
         JOIN category c
              ON bo.category_id = c.category_id
WHERE bo.box_office_sum = (SELECT MAX(box_office_sum) FROM box_office_by_category_id);


/*
4.
Вивести назви фільмів, яких не має в inventory.
Запит має бути без оператора IN
*/
SELECT f.title
FROM film f
         LEFT JOIN inventory i
                   ON f.film_id = i.film_id
WHERE i.film_id IS NULL;


/*
5.
Вивести топ 3 актори, які найбільше зʼявлялись в категорії фільмів “Children”.
*/
WITH actor_appearence_count AS (SELECT fa.actor_id, COUNT(*)
                                FROM film_actor fa
                                         JOIN film_category fc
                                              ON fa.film_id = fc.film_id
                                         JOIN category c
                                              ON fc.category_id = c.category_id
                                WHERE c.name = 'Children'
                                GROUP BY fa.actor_id
                                ORDER BY 2 DESC
                                LIMIT 3)

SELECT a.first_name, a.last_name
FROM actor a
         JOIN actor_appearence_count
              ON a.actor_id = actor_appearence_count.actor_id
