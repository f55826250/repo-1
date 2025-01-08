document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("query-link").addEventListener("click", function(event) {
        event.preventDefault();
        var querySection = document.getElementById("query-section");
    
        // Se la sezione è nascosta, mostriamola
        if (querySection.style.display === "none") {
            querySection.style.display = "block"; // Mostra la sezione
        } else {
            querySection.style.display = "none"; // Nascondi la sezione
        }
    });
})
