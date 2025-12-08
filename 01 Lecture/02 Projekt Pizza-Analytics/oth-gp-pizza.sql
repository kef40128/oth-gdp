-- 01) Zeige alle Pizzen an
SELECT *
FROM pizzen;


-- 02) Zeige alle K-Namen und die Stadt an
SELECT name, stadt
FROM kunden;


-- 03 Zeige alle Kunden aus Regensburg an
SELECT name, stadt
FROM kunden
WHERE stadt = 'Regensburg';


-- 04) Sortiere Abfrage_03 nach Hausnummer aufsteigend
SELECT *
FROM (
	SELECT name, strasse, hausnummer, plz, stadt
	FROM kunden
	WHERE stadt = 'Regensburg')
ORDER BY hausnummer ASC;


-- 05) Wie viele Pizzen wurden verkauft?
SELECT sum(menge) AS Anzahl_Pizzen
FROM bestellungen;


-- 06) Wie viele Pizzen wurde von den einzelnen Sorten verkauft?
SELECT pizza_id, sum(menge) AS Anzahl_Pizzen
FROM bestellungen
GROUP BY pizza_id;


-- 07) Aus welchen Städten kommen unsere Kunden
SELECT Distinct stadt
FROM kunden
ORDER BY stadt;


-- 08) Wie viele Bestellungen wurden insgesamt getätigt?
SELECT count(*) As Anzahl
FROM bestellungen;


-- 09) Wie viele Pizzen (NAME) wurde von den einzelnen Sorten verkauft?
SELECT p.name, sum(b.menge) AS Anzahl_Pizzen
FROM bestellungen b 
INNER JOIN pizzen p
ON b.pizza_id = p.id
GROUP BY p.name
ORDER BY p.name;


