
document.getElementById("filtroKardex").addEventListener("change", renderKardex);

function renderKardex() {
  opciones("filtroKardex", db.productos, "Todos los productos");

  const filtro = document.getElementById("filtroKardex").value;
  const movimientos = db.movimientos
    .filter(m => !filtro || m.productoId === filtro)
    .slice().reverse();

  tabla("listaKardex",
    ["Fecha", "Producto", "Movimiento", "Cantidad", "Saldo", "Detalle"],
    movimientos.map(m => `<tr>
      <td>${new Date(m.fecha).toLocaleString("es-BO")}</td>
      <td>${escapar(nombreProducto(m.productoId))}</td>
      <td>${m.tipo}</td>
      <td>${m.cantidad}</td>
      <td>${m.saldo}</td>
      <td>${escapar(m.detalle)}</td>
    </tr>`));
}
