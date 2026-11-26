
document.getElementById("formProveedor").addEventListener("submit", e => {
  e.preventDefault();

  db.proveedores.push({
    id: nuevoId(),
    nombre: document.getElementById("proveedorNombre").value.trim(),
    telefono: document.getElementById("proveedorTelefono").value.trim(),
    correo: document.getElementById("proveedorCorreo").value.trim(),
    direccion: document.getElementById("proveedorDireccion").value.trim()
  });

  guardarDatos();
  e.target.reset();
  actualizarTodo();
});

function renderProveedores() {
  tabla("listaProveedores", ["Proveedor", "Teléfono", "Correo", "Acción"],
    db.proveedores.map(p => `<tr>
      <td>${escapar(p.nombre)}</td>
      <td>${escapar(p.telefono)}</td>
      <td>${escapar(p.correo)}</td>
      <td><button class="danger" onclick="eliminarProveedor('${p.id}')">Eliminar</button></td>
    </tr>`));

  opciones("compraProveedor", db.proveedores, "Seleccionar proveedor");
}

function eliminarProveedor(id) {
  if (confirm("¿Eliminar proveedor?")) {
    db.proveedores = db.proveedores.filter(p => p.id !== id);
    guardarDatos();
    actualizarTodo();
  }
}
