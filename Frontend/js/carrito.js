const API_URL = "http://localhost:8000";

async function cargarCarrito() {
    const usuarioId = localStorage.getItem("usuario_id");
    const contenedor = document.getElementById("lista-carrito");
    const spanTotal = document.getElementById("total-carrito");

    if (!usuarioId) {
        contenedor.textContent = "Debes iniciar sesión para ver tu carrito.";
        return;
    }

    try {
        const response = await fetch(`${API_URL}/compras/carrito/${usuarioId}`);
        if (response.ok) {
            const data = await response.json();
            
           
            while (contenedor.firstChild) {
                contenedor.removeChild(contenedor.firstChild);
            }

            if (data.items.length === 0) {
                const mensaje = document.createElement("p");
                mensaje.textContent = "Tu carrito está vacío.";
                contenedor.appendChild(mensaje);
                spanTotal.textContent = "0.00";
                return;
            }

            
            data.items.forEach(item => {
                const itemDiv = document.createElement("div");
                itemDiv.style.display = "flex";
                itemDiv.style.justifyContent = "space-between";
                itemDiv.style.marginBottom = "10px";
                itemDiv.style.borderBottom = "1px solid #eee";
                itemDiv.style.paddingBottom = "5px";

                const info = document.createElement("span");
                info.textContent = `${item.producto} (x${item.cantidad})`;

                const subtotal = document.createElement("span");
                subtotal.textContent = `$${item.subtotal.toFixed(2)}`;
                subtotal.style.fontWeight = "bold";

                itemDiv.appendChild(info);
                itemDiv.appendChild(subtotal);
                contenedor.appendChild(itemDiv);
            });

            spanTotal.textContent = data.total.toFixed(2);
        }
    } catch (error) {
        console.error("Error al cargar el carrito:", error);
    }
}


const btnComprar = document.getElementById("btn-comprar");
if (btnComprar) {
    btnComprar.addEventListener("click", async () => {
        const usuarioId = localStorage.getItem("usuario_id");
        if (!usuarioId) return;

        try {
            const response = await fetch(`${API_URL}/compras/pedidos/generar/${usuarioId}`, {
                method: "POST"
            });

            if (response.ok) {
                const data = await response.json();
                alert(`Tu compra fue realizada con éxito Tu número de pedido es el #${data.pedido_id}`);
                window.location.href = "index.html"; // Redirigimos a la tienda
            } else {
                const err = await response.json();
                alert("Error al generar pedido: " + err.detail);
            }
        } catch (error) {
            console.error("Error al comprar:", error);
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    cargarCarrito();
});