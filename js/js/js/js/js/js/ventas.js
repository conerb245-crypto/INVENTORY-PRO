document.getElementById("formVenta").addEventListener("submit", e => {
  e.preventDefault();

  const id = document.getElementById("ventaProducto").value;
  const cantidad = Number(document.getElementById("ventaCantidad").value);
  const p = db.productos.find(x => x.id === id);

  if (!p || !Number.isInteger(cantidad) || cantidad < 1) {
    alert("Verifica el producto y la cantidad.");
    return;
  }

  if (cantidad > p.stock) {
    alert("Stock insuficiente. Disponible: " + p.stock);
    return;
  }

  p.stock -= cantidad;

  db.movimientos.push({
    id: nuevoId(), productoId: id,
    tipo: "Salida", cantidad,
    saldo: p.stock,
    detalle: "Venta: " + document.getElementById("ventaNota").value,
    fecha: new Date().toISOString()
  });

  guardarDatos();
  e.target.reset();
  actualizarTodo();
  alert("Venta registrada correctamente.");
});

function renderVentas() {
  const movimientos = db.movimientos.filter(m => m.tipo === "Salida").slice().reverse();
  tabla("listaVentas", ["Fecha", "Producto", "Cantidad", "Detalle"],
    movimientos.map(m => `<tr>
      <td>${new Date(m.fecha).toLocaleDateString("es-BO")}</td>
      <td>${escapar(nombreProducto(m.productoId))}</td>
      <td>${m.cantidad}</td>
      <td>${escapar(m.detalle)}</td>
    </tr>`));
}
