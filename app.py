
import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(
    page_title="INVENTORY PRO",
    page_icon="📦",
    layout="wide"
)

db = sqlite3.connect("inventario.db", check_same_thread=False)
db.execute("""CREATE TABLE IF NOT EXISTS categorias(
    id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT UNIQUE)""")
db.execute("""CREATE TABLE IF NOT EXISTS proveedores(
    id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT,
    telefono TEXT, correo TEXT)""")
db.execute("""CREATE TABLE IF NOT EXISTS productos(
    id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT,
    codigo TEXT UNIQUE, categoria TEXT, precio REAL,
    stock INTEGER, minimo INTEGER)""")
db.execute("""CREATE TABLE IF NOT EXISTS movimientos(
    id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT,
    tipo TEXT, producto TEXT, cantidad INTEGER,
    referencia TEXT)""")
db.commit()

def consultar(sql, valores=()):
    return db.execute(sql, valores).fetchall()

def ejecutar(sql, valores=()):
    db.execute(sql, valores)
    db.commit()

st.markdown("""
<style>
.stApp {background:#101010;color:white}
h1,h2,h3 {color:#ff3434}
section[data-testid="stSidebar"] {background:#191919}
div.stButton > button {
    background:#d92332;color:white;border:0;
    border-radius:8px;font-weight:bold
}
div[data-testid="stMetric"] {
    background:#202020;padding:18px;border-radius:12px;
    border-left:4px solid #e52b39
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("# INVENTORY 🔴 PRO")
st.sidebar.caption("CONTROL INTELIGENTE · INVENTARIO EFICIENTE")

pagina = st.sidebar.radio(
    "MENÚ PRINCIPAL",
    ["Dashboard", "Categorías", "Productos",
     "Proveedores", "Compras", "Ventas", "Kardex"]
)

productos = consultar("SELECT * FROM productos")
categorias = consultar("SELECT * FROM categorias")
proveedores = consultar("SELECT * FROM proveedores")

st.title("INVENTORY PRO")
st.caption("Sistema empresarial de gestión y control de inventarios")

# DASHBOARD
if pagina == "Dashboard":
    st.header("Panel principal")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Productos", len(productos))
    c2.metric("Categorías", len(categorias))
    c3.metric("Proveedores", len(proveedores))
    c4.metric("Unidades disponibles",
              sum(p[5] for p in productos))

    st.subheader("Alertas de stock bajo")
    bajos = [p for p in productos if p[5] <= p[6]]
    if bajos:
        for p in bajos:
            st.warning(f"{p[1]}: quedan {p[5]} unidades")
    else:
        st.success("No hay productos con stock bajo.")

    st.subheader("Últimos movimientos")
    for m in consultar(
        "SELECT fecha,tipo,producto,cantidad FROM movimientos ORDER BY id DESC LIMIT 8"
    ):
        st.write(f"{m[0]} | {m[1]} | {m[2]} | {m[3]} unidades")

# CATEGORÍAS
elif pagina == "Categorías":
    st.header("Administrar categorías")
    with st.form("categoria"):
        nombre = st.text_input("Nombre de categoría")
        guardar = st.form_submit_button("Agregar categoría")
        if guardar:
            if nombre.strip():
                try:
                    ejecutar("INSERT INTO categorias(nombre) VALUES(?)",
                             (nombre.strip(),))
                    st.success("Categoría registrada")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("Esa categoría ya existe")
            else:
                st.error("Escribe un nombre")

    for c in consultar("SELECT * FROM categorias"):
        a,b = st.columns([4,1])
        a.write(f"**{c[1]}**")
        if b.button("Eliminar", key=f"cat{c[0]}"):
            ejecutar("DELETE FROM categorias WHERE id=?", (c[0],))
            st.rerun()

# PRODUCTOS
elif pagina == "Productos":
    st.header("Gestión de productos")
    nombres_cat = [c[1] for c in categorias]

    with st.form("producto"):
        nombre = st.text_input("Nombre del producto")
        codigo = st.text_input("Código")
        categoria = st.selectbox("Categoría", nombres_cat or ["Sin categoría"])
        precio = st.number_input("Precio unitario", min_value=0.0)
        stock = st.number_input("Stock inicial", min_value=0, step=1)
        minimo = st.number_input("Stock mínimo", min_value=0, step=1)
        guardar = st.form_submit_button("Registrar producto")

        if guardar:
            if nombre.strip() and codigo.strip():
                try:
                    ejecutar("""INSERT INTO productos
                    (nombre,codigo,categoria,precio,stock,minimo)
                    VALUES(?,?,?,?,?,?)""",
                    (nombre.strip(),codigo.strip(),categoria,
                     precio,stock,minimo))
                    st.success("Producto registrado")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("El código ya está registrado")
            else:
                st.error("Completa nombre y código")

    st.subheader("Inventario actual")
    st.dataframe(
        [{"Nombre":p[1],"Código":p[2],"Categoría":p[3],
          "Precio":p[4],"Stock":p[5],"Mínimo":p[6]}
         for p in productos],
        use_container_width=True
    )

    if productos:
        elegido = st.selectbox(
            "Producto para eliminar",
            productos, format_func=lambda p: f"{p[1]} ({p[2]})"
        )
        if st.button("Eliminar producto"):
            ejecutar("DELETE FROM productos WHERE id=?", (elegido[0],))
            st.rerun()

# PROVEEDORES
elif pagina == "Proveedores":
    st.header("Gestión de proveedores")
    with st.form("proveedor"):
        nombre = st.text_input("Nombre o empresa")
        telefono = st.text_input("Teléfono")
        correo = st.text_input("Correo electrónico")
        guardar = st.form_submit_button("Registrar proveedor")
        if guardar:
            if nombre.strip():
                ejecutar("""INSERT INTO proveedores(nombre,telefono,correo)
                VALUES(?,?,?)""", (nombre,telefono,correo))
                st.success("Proveedor registrado")
                st.rerun()
            else:
                st.error("Escribe el nombre")

    st.dataframe(
        [{"Nombre":p[1],"Teléfono":p[2],"Correo":p[3]}
         for p in proveedores],
        use_container_width=True
    )

# COMPRAS
elif pagina == "Compras":
    st.header("Compras / Entradas")
    if not productos:
        st.info("Primero registra un producto.")
    else:
        with st.form("compra"):
            elegido = st.selectbox(
                "Producto", productos,
                format_func=lambda p: p[1]
            )
            cantidad = st.number_input("Cantidad comprada", min_value=1, step=1)
            proveedor = st.selectbox(
                "Proveedor",
                [p[1] for p in proveedores] or ["No especificado"]
            )
            guardar = st.form_submit_button("Registrar compra")

            if guardar:
                ejecutar("UPDATE productos SET stock=stock+? WHERE id=?",
                         (cantidad,elegido[0]))
                ejecutar("""INSERT INTO movimientos
                (fecha,tipo,producto,cantidad,referencia)
                VALUES(?,?,?,?,?)""",
                (datetime.now().strftime("%Y-%m-%d %H:%M"),
                 "COMPRA",elegido[1],cantidad,proveedor))
                st.success("Compra registrada y stock actualizado")
                st.rerun()

# VENTAS
elif pagina == "Ventas":
    st.header("Ventas / Salidas")
    disponibles = [p for p in productos if p[5] > 0]
    if not disponibles:
        st.info("No hay productos disponibles para vender.")
    else:
        with st.form("venta"):
            elegido = st.selectbox(
                "Producto", disponibles,
                format_func=lambda p: f"{p[1]} - Stock: {p[5]}"
            )
            cantidad = st.number_input("Cantidad vendida", min_value=1, step=1)
            cliente = st.text_input("Cliente o referencia")
            guardar = st.form_submit_button("Registrar venta")

            if guardar:
                if cantidad > elegido[5]:
                    st.error("Stock insuficiente")
                else:
                    ejecutar("UPDATE productos SET stock=stock-? WHERE id=?",
                             (cantidad,elegido[0]))
                    ejecutar("""INSERT INTO movimientos
                    (fecha,tipo,producto,cantidad,referencia)
                    VALUES(?,?,?,?,?)""",
                    (datetime.now().strftime("%Y-%m-%d %H:%M"),
                     "VENTA",elegido[1],cantidad,cliente))
                    st.success("Venta registrada y stock actualizado")
                    st.rerun()

# KARDEX
elif pagina == "Kardex":
    st.header("Kardex - Historial de movimientos")
    historial = consultar(
        "SELECT fecha,tipo,producto,cantidad,referencia "
        "FROM movimientos ORDER BY id DESC"
    )
    st.dataframe(
        [{"Fecha":m[0],"Movimiento":m[1],"Producto":m[2],
          "Cantidad":m[3],"Referencia":m[4]} for m in historial],
        use_container_width=True
    )

st.divider()
st.caption("INVENTORY PRO · PROTOTIPO 1.0")

