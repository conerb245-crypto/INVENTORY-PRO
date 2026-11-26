
document.getElementById("formCategoria").addEventListener("submit", e => {
  e.preventDefault();
  const nombre = document.getElementById("categoriaNombre").value.trim();

  if (db.categorias.some(c => c.nombre.toLowerCase() === nombre.toLowerCase())) {
    alert("La categoría ya existe.");
    return;
  }

  db.categorias.push({ id: nuevoId(), nombre });
  guardarDatos();
  e.target.reset();
  actualizarTodo();
});

function renderCategorias() {
  tabla("listaCategorias", ["Categoría", "Acción"],
    db.categorias.map(c => `<tr>
      <td>${escapar(c.nombre)}</td>
      <td><button class="danger" onclick="eliminarCategoria('${c.id}')">Eliminar</button></td>
    </tr>`));

  opciones("productoCategoria", db.categorias, "Seleccionar categoría");
}

function eliminarCategoria(id) {
  if (db.productos.some(p => p.categoriaId === id)) {
    alert("Primero cambia o elimina los productos asociados.");
    return;
  }
  if (confirm("¿Eliminar categoría?")) {
    db.categorias = db.categorias.filter(c => c.id !== id);
    guardarDatos();
    actualizarTodo();
  }
}
