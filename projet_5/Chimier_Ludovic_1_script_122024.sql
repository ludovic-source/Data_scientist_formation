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

WITH latest_order AS (
    SELECT MAX(order_purchase_timestamp) AS max_purchase_date
    FROM orders
),
min_dates AS (
    SELECT seller_id, MIN(order_purchase_timestamp) AS first_order_date
    FROM order_items
    JOIN orders o ON order_items.order_id = o.order_id
    WHERE o.order_status = 'delivered'  -- Filtrer les commandes livrées
    GROUP BY seller_id
)
SELECT 
    oi.seller_id, 
    COUNT(oi.order_id) AS products_nb  -- Compte le nombre de produits vendus
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
    AND o.order_status = 'delivered'  -- Assurer que seule les commandes livrées sont comptées
JOIN min_dates
    ON oi.seller_id = min_dates.seller_id
WHERE min_dates.first_order_date > DATE((SELECT max_purchase_date FROM latest_order), '-3 months')
GROUP BY oi.seller_id
HAVING products_nb > 30;

/*
 Question : Quels sont les 5 codes postaux, enregistrant plus de 30
 reviews, avec le pire review score moyen sur les 12 derniers mois

 Hypothèses :
 - Les codes postaux seront ceux des clients (customer)
 - On ne tient compte que des commandes livrées
 */        

WITH recent_reviews AS (
    -- Récupérer les reviews des 12 derniers mois
    SELECT c.customer_zip_code_prefix, r.review_score
	    FROM order_reviews r
	    JOIN orders o ON r.order_id = o.order_id
	    JOIN customers c ON o.customer_id = c.customer_id
	    WHERE o.order_status = 'delivered'  -- Filtrer uniquement les commandes livrées
	    AND o.order_id IN (
	          SELECT order_id
		          FROM orders
		          WHERE o.order_delivered_customer_date >= DATE('now', '-12 months')
      )
),
aggregated_data AS (
    -- Calculer le score moyen et le nombre de reviews par code postal
    SELECT customer_zip_code_prefix, COUNT(*) AS review_count, AVG(review_score) AS avg_review_score
	    FROM recent_reviews
	    GROUP BY customer_zip_code_prefix
	    HAVING COUNT(*) > 30  -- Filtrer les codes postaux ayant plus de 30 reviews
)
-- Récupérer les 5 codes postaux avec le pire score moyen
SELECT 
    customer_zip_code_prefix,
    review_count,
    avg_review_score
FROM aggregated_data
ORDER BY avg_review_score ASC  -- Trier par score moyen croissant (pire score d'abord)
LIMIT 5;