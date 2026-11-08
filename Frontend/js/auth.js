console.log("¡El archivo auth.js sí está cargando!");
const API_URL = "http://localhost:8000";


const formRegistro = document.getElementById("form-registro");
if (formRegistro) {
    formRegistro.addEventListener("submit", async (e) => {
        e.preventDefault(); 

        
        const nombre = document.getElementById("nombre-reg").value;
        const correo = document.getElementById("email-reg").value;
        const password = document.getElementById("password-reg").value;

        try {
            const response = await fetch(`${API_URL}/usuarios/registro`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ nombre, correo, password })
            });

            if (response.ok) {
                alert("¡Registro exitoso! Ahora puedes iniciar sesión.");
                window.location.href = "login.html"; // Redirigimos al login
            } else {
                const errorData = await response.json();
                alert("Error: " + errorData.detail);
            }
        } catch (error) {
            console.error("Error al registrar:", error);
        }
    });
}


const formLogin = document.getElementById("form-login");
if (formLogin) {
    formLogin.addEventListener("submit", async (e) => {
        e.preventDefault();

        const correo = document.getElementById("email-login").value;
        const password = document.getElementById("password-login").value;

        try {
            const response = await fetch(`${API_URL}/usuarios/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ correo, password })
            });

            if (response.ok) {
                const data = await response.json();
                
                localStorage.setItem("token", data.access_token);
                localStorage.setItem("usuario_id", data.usuario_id);
                localStorage.setItem("usuario_nombre", data.nombre);

                alert(`¡Bienvenido ${data.nombre}!`);
                window.location.href = "index.html"; // Redirigimos a la página principal
            } else {
                alert("Correo o contraseña incorrectos. Revisa tus datos.");
            }
        } catch (error) {
            console.error("Error al iniciar sesión:", error);
        }
    });
}