
document.getElementById("formProducto").addEventListener("submit", e => {
  e.preventDefault();

  if (!db.categorias.length) {
    alert("Primero registra una categoría.");
    return;
  }

  const codigo = document.getElementById("productoCodigo").value.trim();

  if (db.productos.some(p => p.codigo.toLowerCase() === codigo.toLowerCase())) {
    alert("El código ya existe.");
    return;
  }

  const p = {
    id: nuevoId(),
    nombre: document.getElementById("productoNombre").value.trim(),
    codigo,
    categoriaId: document.getElementById("productoCategoria").value,
    precio: Number(document.getElementById("productoPrecio").value),
    stock: Number(document.getElementById("productoStock").value),
    minimo: Number(document.getElementById("productoMinimo").value)
  };

  db.productos.push(p);

  if (p.stock > 0) {
    db.movimientos.push({
      id: nuevoId(), productoId: p.id,
      tipo: "Entrada", cantidad: p.stock,
      saldo: p.stock, detalle: "Stock inicial",
      fecha: new Date().toISOString()
    });
  }

  guardarDatos();
  e.target.reset();
  document.getElementById("productoMinimo").value = 5;
  actualizarTodo();
});

function renderProductos() {
  tabla("listaProductos",
    ["Producto", "Código", "Precio", "Stock", "Acción"],
    db.productos.map(p => `<tr>
      <td>${escapar(p.nombre)}</td>
      <td>${escapar(p.codigo)}</td>
      <td>${dinero(p.precio)}</td>
      <td>${p.stock}${p.stock <= p.minimo ? ' <span style="color:#f5b942">Stock bajo</span>' : ''}</td>
      <td><button class="danger" onclick="eliminarProducto('${p.id}')">Eliminar</button></td>
    </tr>`));

  opciones("compraProducto", db.productos, "Seleccionar producto");
  opciones("ventaProducto", db.productos, "Seleccionar producto");
}

function eliminarProducto(id) {
  if (confirm("¿Eliminar este producto? Se conservará su historial.")) {
    db.productos = db.productos.filter(p => p.id !== id);
    guardarDatos();
    actualizarTodo();
  }
}
