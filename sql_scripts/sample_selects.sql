
SELECT 
    name,
    CASE WHEN x.mycount IS NULL THEN 0 ELSE x.mycount END AS non_flingers
FROM zoo LEFT JOIN (
    SELECT zoo_id, COUNT(*) AS mycount
    FROM monkey
        WHERE flings_poop = false
        GROUP BY zoo_id
    ) AS x
ON zoo.id = x.zoo_id;

SELECT DISTINCT zoo.name 
FROM zoo JOIN monkey ON zoo.id = monkey.zoo_id
WHERE monkey.flings_poop = TRUE;

SELECT monkey.name, zoo.name, zoo.opens, zoo.closes
FROM zoo INNER JOIN monkey ON zoo.id = monkey.zoo_id
WHERE TIME('09:00') BETWEEN opens AND closes;


