/*
1. Productos más vendidos:
Escribe una consulta para listar los 5 productos más vendidos 
(por cantidad) junto con su categoría.
*/

SELECT p.nombre, p.categoria, SUM(v.cantidad) AS cantidad_total
FROM productos p
INNER JOIN ventas v ON p.producto_id = v.producto_id
GROUP BY p.producto_id, p.nombre, p.categoria
ORDER BY cantidad_total DESC
LIMIT 5;



/*
2.  Categorías más rentables:
Escribe una consulta para calcular la suma total de ingresos generados por cada 
categoría de productos y ordenarlas de mayor a menor.
*/

SELECT p.categoria, SUM(v.cantidad * p.precio) AS ingresos_totales
FROM productos p
INNER JOIN ventas v ON p.producto_id = v.producto_id
GROUP BY p.categoria
ORDER BY ingresos_totales DESC;



/*
3. Clientes más valiosos:
Escribe una consulta para identificar a los 5 clientes que más ingresos han
generado para la tienda. Incluye su nombre, correo y el monto total gastado.
*/

SELECT c.nombre, c.correo, SUM(v.cantidad * p.precio) AS total_gastado
FROM clientes c
INNER JOIN ventas v ON c.cliente_id = v.cliente_id
INNER JOIN productos p ON v.producto_id = p.producto_id
GROUP BY c.cliente_id, c.nombre, c.correo
ORDER BY total_gastado DESC
LIMIT 5;


/*
4. Tendencias por fecha:
Escribe una consulta para calcular las ventas totales (en términos de ingresos)
por mes.
*/

SELECT DATE_FORMAT(v.fecha, '%m') AS mes, SUM(v.cantidad * p.precio) AS ingresos_totales
FROM ventas v
INNER JOIN productos p ON v.producto_id = p.producto_id
GROUP BY mes
ORDER BY mes ASC;


/*
5. Inventario potencialmente insuficiente:
Suponiendo que cada producto tiene un inventario inicial de 500 unidades,
escribe una consulta para listar los productos cuya venta acumulada supera el
80% del inventario inicial.
*/

SELECT p.nombre, p.categoria, SUM(v.cantidad) AS cantidad_vendida, 
       500 AS inventario_inicial, 
       500 * 0.8 AS inventario_minimo_disponible
FROM productos p
JOIN ventas v ON p.producto_id = v.producto_id
GROUP BY p.producto_id, p.nombre, p.categoria
HAVING cantidad_vendida > 500 * 0.8;
