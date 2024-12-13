/*
En excluant les commandes annulées, quelles sont les commandes
 récentes de moins de 3 mois que les clients ont reçues avec au moins 3
 jours de retard ?
*/ 

WITH latest_order AS(
 SELECT MAX(order_purchase_timestamp) AS max_purchase_date
 FROM orders
 )
SELECT * FROM orders
	WHERE not order_status = 'canceled'
	  AND order_purchase_timestamp > DATE(((SELECT max_purchase_date from latest_order)), '-3 months')
	  AND order_delivered_customer_date > DATE(order_estimated_delivery_date , '+3 days'); 

/*
Qui sont les vendeurs ayant généré un chiffre d'affaires de plus de 100 000
Real sur des commandes livrées via Olist ?
*/     

SELECT oi.seller_id, SUM(oi.price) as turnover 
	FROM order_items oi
	WHERE oi.order_id in (
		SELECT o.order_id 
			FROM orders o 
				where o.order_status = 'delivered'
	)			
	GROUP BY oi.seller_id
	HAVING SUM(oi.price) > 100000;

 /*
 Qui sont les nouveaux vendeurs (moins de 3 mois d'ancienneté) qui
 sont déjà très engagés avec la plateforme (ayant déjà vendu plus de 30
 produits) ?
*/

WITH latest_order as(
select max(order_purchase_timestamp) AS max_purchase_date
from orders
),
orders_join AS(
	SELECT DISTINCT oi.seller_id, oi.order_id, oi.product_id, o.order_purchase_timestamp
		FROM order_items oi
		INNER JOIN orders o ON o.order_id = oi.order_id
		WHERE o.order_status = 'delivered'
),
orders_agg AS(
	SELECT seller_id, COUNT(product_id) AS products_nb, min(order_purchase_timestamp) AS seniority_date
		FROM orders_join
		GROUP BY seller_id
)
SELECT * 
	FROM orders_agg
	WHERE products_nb > 30
	AND seniority_date > DATE((SELECT max_purchase_date FROM latest_order), '-3 months');

/*
 Question : Quels sont les 5 codes postaux, enregistrant plus de 30
 reviews, avec le pire review score moyen sur les 12 derniers mois

 Hypothèses :
 - Les codes postaux seront ceux des clients (customer)
 */        
WITH latest_order AS(
	SELECT max(order_purchase_timestamp) AS max_purchase_date
FROM orders
),
orders_join AS(
	SELECT c.customer_zip_code_prefix, or2.review_score
		FROM order_reviews or2
		INNER JOIN orders o ON o.order_id = or2.order_id
		INNER JOIN customers c ON o.customer_id = c.customer_id
		WHERE o.order_purchase_timestamp > DATE((SELECT max_purchase_date FROM latest_order), '-12 months')
),
orders_agg AS(
	SELECT customer_zip_code_prefix, COUNT(*) AS reviews_nb, AVG(review_score) AS avg_review_score
		FROM orders_join
		WHERE review_score IS NOT NULL
		GROUP BY customer_zip_code_prefix				
)
SELECT *
	FROM orders_agg
	WHERE reviews_nb > 30
	ORDER BY avg_review_score ASC
	LIMIT 5;

;

SELECT * FROM order_reviews or2;
SELECT * FROM orders o ;