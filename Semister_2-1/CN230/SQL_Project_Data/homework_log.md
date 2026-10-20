# CN230 A4 Homework: SQL Part 2 (Data Intake & Relational Algebra), work log

Environment: MySQL 8.1 in Docker (`sql_project_data-db-1`), database `production_crude_oil`.
Data: monthly oil production, Sirikit (Source 1, W09) and Erawan (Source 2, new). Unit: Barrels/day.

## Tables

| Table | Columns |
|---|---|
| production_crude_oil (flat) | production_id (PK, auto_increment), record_year, record_month, oil_field, production_volume, unit (default 'Barrels/day') |
| Field | Field_id (PK), Field_name |
| Product | Product_id (PK), Product_name |
| Field_Product | field_product_id (PK), production_id (FK -> Product), field_id (FK -> Field), volume, year, month, unit |

Mistakes fixed along the way:
- `show * from` is not SQL; use `SELECT * FROM`.
- `Field_Product` failed because of a stray `)` after the primary key and `REFERENCE` instead of `REFERENCES`.
- Id 21 skipped: auto_increment burns an id on a failed insert. Harmless.

## Part 1: Data intake log (what to write)

- Table: production_crude_oil. Old (W09): 20. New (W10): 20. Total 40.
- Source of new data: Source 2, Table 2.1-2M Production of Condensate, Erawan column, 1986-01 to 1987-10 (see Part 2 for the replaced months).
- Unpaired tuples: 4 (see Part 2). Schema change: added Field, Product, Field_Product.

## Part 2: DML

Insert 20 Erawan rows (1986-01 to 1987-08), then replace the last two so some tuples are unpaired:

```sql
DELETE FROM production_crude_oil
WHERE oil_field = 'Erawan' AND record_year = 1987 AND record_month IN (7, 8);

INSERT INTO production_crude_oil (record_year, record_month, oil_field, production_volume)
VALUES (1987, 9, 'Erawan', 16810), (1987, 10, 'Erawan', 15977);
```

Verify: `SELECT COUNT(*) FROM production_crude_oil;` -> 40.

Unpaired check (same year+month missing for the other field):

```sql
SELECT * FROM production_crude_oil a
WHERE NOT EXISTS (
  SELECT 1 FROM production_crude_oil b
  WHERE b.record_year = a.record_year AND b.record_month = a.record_month
    AND b.oil_field <> a.oil_field);
```

Result: 4 rows: Sirikit 1987-07, 1987-08; Erawan 1987-09, 1987-10.
Summary to write: inserted 20, unpaired 4, problem found: skipped auto_increment id.

## Setup for Parts 4-5 (normalise into 3 tables)

```sql
INSERT INTO Field (Field_id, Field_name) VALUES (1,'Sirikit'),(2,'Erawan'),(3,'Bongkot');
INSERT INTO Product (Product_id, Product_name) VALUES (1,'Crude oil'),(2,'Condensate');
INSERT INTO Field_Product
SELECT p.production_id, 1, f.Field_id, p.production_volume, p.record_year, p.record_month, p.unit
FROM production_crude_oil p JOIN Field f ON f.Field_name = p.oil_field;
```

Bongkot has no Field_Product rows; this is the unpaired row for the LEFT JOIN.
Open question: Source 2 is titled "Condensate". If Erawan is condensate, run
`UPDATE Field_Product SET production_id = 2 WHERE field_id = 2;`

## Part 3: Selection/Projection and Set Operations

3A. Question: months of 1987 where Erawan produced more than 15,000 barrels/day.
RA: pi[record_month, production_volume]( sigma[oil_field='Erawan' AND record_year=1987 AND production_volume>15000](P) )

```sql
SELECT record_month, production_volume FROM production_crude_oil
WHERE oil_field = 'Erawan' AND record_year = 1987 AND production_volume > 15000;
```
Result: months 6 (16245), 9 (16810), 10 (15977). Matches expectation.

3B. Question: months with Sirikit data but no Erawan data (and the reverse).
RA: S = rho_S(pi[year,month](sigma[field='Sirikit'](P))), E = rho_E(pi[year,month](sigma[field='Erawan'](P))); S - E, and (S - E) U (E - S).

```sql
SELECT record_year, record_month FROM production_crude_oil WHERE oil_field = 'Sirikit'
EXCEPT
SELECT record_year, record_month FROM production_crude_oil WHERE oil_field = 'Erawan';
```
Result: (1987,7), (1987,8). The symmetric UNION version returns the 4 unpaired months (1987-07, 08, 09, 10).

## Part 4: JOIN

4A. R = Field, S = Field_Product. RA: R join[Field_id=field_id] S and R left-outer-join[Field_id=field_id] S.

```sql
SELECT f.Field_name, fp.`year`, fp.`month`, fp.volume
FROM Field f INNER JOIN Field_Product fp ON f.Field_id = fp.field_id;   -- 40 rows
SELECT f.Field_name, fp.`year`, fp.`month`, fp.volume
FROM Field f LEFT JOIN Field_Product fp ON f.Field_id = fp.field_id;    -- 41 rows
```
Explanation: INNER = 40, LEFT = 41. Bongkot has no Field_Product row. INNER drops it; LEFT keeps it with NULLs.

4B. RA: pi[Field_name, Product_name, year, month, volume]( Field join Field_Product join Product ).

```sql
SELECT f.Field_name, pr.Product_name, fp.`year`, fp.`month`, fp.volume, fp.unit
FROM Field_Product fp
JOIN Field f    ON f.Field_id = fp.field_id
JOIN Product pr ON pr.Product_id = fp.production_id
ORDER BY f.Field_name, fp.`year`, fp.`month`;
```
Business question: each field's monthly production volume for each product. 40 rows.

## Part 5: Aggregates and query tree

5A. RA: oil_field gamma[COUNT(*), SUM, AVG, MIN, MAX](P)

```sql
SELECT oil_field, COUNT(*) AS n, SUM(production_volume) AS total,
       ROUND(AVG(production_volume)) AS avg_vol,
       MIN(production_volume) AS min_vol, MAX(production_volume) AS max_vol
FROM production_crude_oil GROUP BY oil_field;
```
Expected: Sirikit n=20, total 374583, avg ~18729, min 14879, max 21231. Erawan n=20, total 292233, avg ~14612, min 12615, max 16810.

5B. Fields/products with average monthly volume above 15,000.

```sql
SELECT f.Field_name, pr.Product_name, COUNT(*) AS months, ROUND(AVG(fp.volume)) AS avg_volume
FROM Field_Product fp
JOIN Field f    ON f.Field_id = fp.field_id
JOIN Product pr ON pr.Product_id = fp.production_id
GROUP BY f.Field_name, pr.Product_name
HAVING AVG(fp.volume) > 15000;
```
Expected: 1 row, Sirikit / Crude oil / 20 / ~18729 (Erawan removed by HAVING).

Query tree, bottom to top: Field_Product join Field, then join Product, then gamma (GROUP BY), then sigma (HAVING), then pi (SELECT).
HAVING is a sigma above gamma; WHERE would be a sigma below gamma.

## Part 6: Reflection (draft answers)

1. RA first: helped a lot. It made us decide tables, conditions and operators before writing SQL, and showed where WHERE and HAVING belong.
2. Source 2 problems: numbers with thousands separators (15,981), YTD and empty-field columns to skip, same unit (no mismatch), skipped auto_increment id, deliberately unpaired months and a Field (Bongkot) with no data.
3. LCI mapping: SOURCE = the two source tables, PROCESS = Field, FLOW = Product, LCI_EXCHANGE = Field_Product (amount, unit, period linking a process to a flow).

## Still to do by hand

- Handwritten RA photos for 3A, 3B, 4A, 4B, 5A and a query tree for 5B.
- CLI screenshots for each query above; Source 2 screenshot for Part 1 Evidence 01.
- Fill the team info page, then submit one PDF per team via MS Teams (Turn-In). Check the late policy.
