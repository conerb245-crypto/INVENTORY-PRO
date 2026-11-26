document.getElementById("formCompra").addEventListener("submit", e => {
  e.preventDefault();

  const id = document.getElementById("compraProducto").value;
  const cantidad = Number(document.getElementById("compraCantidad").value);
  const proveedorId = document.getElementById("compraProveedor").value;
  const p = db.productos.find(x => x.id === id);

  if (!p || !Number.isInteger(cantidad) || cantidad < 1) {
    alert("Verifica el producto y la cantidad.");
    return;
  }

  p.stock += cantidad;

  db.movimientos.push({
    id: nuevoId(), productoId: id,
    tipo: "Entrada", cantidad,
    saldo: p.stock,
    detalle: "Compra: " +
      (db.proveedores.find(x => x.id === proveedorId)?.nombre || "Sin proveedor") +
      " · " + document.getElementById("compraNota").value,
    fecha: new Date().toISOString()
  });

  guardarDatos();
  e.target.reset();
  actualizarTodo();
  alert("Compra registrada correctamente.");
});

function renderCompras() {
  const movimientos = db.movimientos.filter(m => m.tipo === "Entrada").slice().reverse();
  tabla("listaCompras", ["Fecha", "Producto", "Cantidad", "Detalle"],
    movimientos.map(m => `<tr>
      <td>${new Date(m.fecha).toLocaleDateString("es-BO")}</td>
      <td>${escapar(nombreProducto(m.productoId))}</td>
      <td>${m.cantidad}</td>
      <td>${escapar(m.detalle)}</td>
    </tr>`));
}
