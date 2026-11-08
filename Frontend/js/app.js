const API_URL = "http://localhost:8000";

// Para obtener productos aleatorios de nuestro backend 
async function cargarProductosAleatorios() {
    try {
        const response = await fetch(`${API_URL}/productos/aleatorios?limite=4`);
        
        if (response.ok) {
            const productos = await response.json();
            const contenedor = document.getElementById("contenedor-aleatorios");
            
            if (!contenedor) return; 

            while (contenedor.firstChild) {
                contenedor.removeChild(contenedor.firstChild);
            }          
            productos.forEach(producto => {
                
                
                const card = document.createElement("div");
                card.className = "producto-card";

                const img = document.createElement("img");
                
                img.src = producto.imagen.includes("Assets") ? producto.imagen : `./Assets/${producto.imagen}`; 
                img.alt = producto.nombre;

                const titulo = document.createElement("h3");
                titulo.textContent = producto.nombre;

                const precio = document.createElement("p");
                precio.textContent = `$${producto.precio}`;
               
                card.appendChild(img);
                card.appendChild(titulo);
                card.appendChild(precio);
              

                contenedor.appendChild(card);
            });
        } else {
            console.error("Error en la respuesta del servidor");
        }
    } catch (error) {
        console.error("Error al conectar con la API:", error);
    }
}


document.addEventListener("DOMContentLoaded", () => {
    cargarProductosAleatorios();
});


async function cargarCatalogo() {
    const contenedor = document.getElementById("contenedor-catalogo");
    if (!contenedor) return; 
    try {
        
        const response = await fetch(`${API_URL}/productos/`);
        
        if (response.ok) {
            const todosLosProductos = await response.json();
            
            const dibujarProductos = (listaProductos) => {
                
                while (contenedor.firstChild) {
                    contenedor.removeChild(contenedor.firstChild);
                }

                listaProductos.forEach(producto => {
                    const card = document.createElement("div");
                    card.className = "producto-card";

                    const img = document.createElement("img");
                    img.src = producto.imagen.includes("Assets") ? producto.imagen : `./Assets/${producto.imagen}`;
                    img.alt = producto.nombre;

                    const titulo = document.createElement("h3");
                    titulo.textContent = producto.nombre;

                    const precio = document.createElement("p");
                    precio.textContent = `$${producto.precio}`;

                    const btnAgregar = document.createElement("button");
                    btnAgregar.textContent = "Agregar al Carrito";
                    btnAgregar.style.backgroundColor = "#28a745"; // Botón verdecito
                    
                    btnAgregar.addEventListener("click", async () => {
                        const usuarioId = localStorage.getItem("usuario_id");
                        
                        if (!usuarioId) {
                            alert("¡Debes iniciar sesión para agregar productos al carrito!");
                            window.location.href = "login.html";
                            return;
                        }

                        try {
                            const response = await fetch(`${API_URL}/compras/carrito/agregar`, {
                                method: "POST",
                                headers: { "Content-Type": "application/json" },
                                body: JSON.stringify({
                                    usuario_id: parseInt(usuarioId),
                                    producto_id: producto.id,
                                    cantidad: 1
                                })
                            });

                            if (response.ok) {
                                alert(`¡Agregaste ${producto.nombre} al carrito exitosamente!`);
                            } else {
                                const err = await response.json();
                                alert("Error: " + err.detail);
                            }
                        } catch (error) {
                            console.error("Error al agregar al carrito:", error);
                        }
                    });

                    card.appendChild(img);
                    card.appendChild(titulo);
                    card.appendChild(precio);
                    card.appendChild(btnAgregar);
                    contenedor.appendChild(card);
                });
            };

            dibujarProductos(todosLosProductos);

            //BUSCADOR
            const buscador = document.getElementById("buscador-productos");
            buscador.addEventListener("input", (e) => {
                const textoBusqueda = e.target.value.toLowerCase();
                // Se filtra la lista según lo que escriba el comprador
                const productosFiltrados = todosLosProductos.filter(prod => 
                    prod.nombre.toLowerCase().includes(textoBusqueda)
                );
                dibujarProductos(productosFiltrados);
            });

        }
    } catch (error) {
        console.error("Error al cargar el catálogo:", error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    cargarProductosAleatorios(); 
    cargarCatalogo(); // 
});