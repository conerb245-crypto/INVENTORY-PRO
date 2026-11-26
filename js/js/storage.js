
const STORAGE_KEY = "inventory_pro_v1";

let db = JSON.parse(localStorage.getItem(STORAGE_KEY)) || {
  categorias: [],
  productos: [],
  proveedores: [],
  movimientos: []
};

function guardarDatos() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(db));
}

function nuevoId() {
  return Date.now().toString(36) +
    Math.random().toString(36).slice(2, 7);
}

function escapar(valor) {
  return String(valor ?? "").replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;",
    '"': "&quot;", "'": "&#39;"
  })[c]);
}

function dinero(valor) {
  return "Bs " + Number(valor).toFixed(2);
}
