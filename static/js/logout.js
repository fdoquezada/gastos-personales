document.addEventListener('DOMContentLoaded', function() {
    const logoutLinks = document.querySelectorAll('.logout-link');
    
    logoutLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const modal = document.createElement('div');
            modal.className = 'logout-modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <h3>Gracias por visitarnos</h3>
                    <p>¡Hasta pronto!</p>
                    <button class="btn btn-primary confirm-logout">Cerrar sesión</button>
                </div>
            `;
            
            document.body.appendChild(modal);
            
            const confirmButton = modal.querySelector('.confirm-logout');
            confirmButton.addEventListener('click', function() {
                window.location.href = link.href;
            });
            
            // Agregar animación de entrada
            modal.style.opacity = '0';
            modal.style.transform = 'scale(0.9)';
            setTimeout(() => {
                modal.style.opacity = '1';
                modal.style.transform = 'scale(1)';
            }, 10);
            
            // Agregar animación de salida al hacer clic fuera del modal
            modal.addEventListener('click', function(e) {
                if (e.target === modal) {
                    modal.style.opacity = '0';
                    modal.style.transform = 'scale(0.9)';
                    setTimeout(() => {
                        modal.remove();
                    }, 300);
                }
            });
        });
    });
});
