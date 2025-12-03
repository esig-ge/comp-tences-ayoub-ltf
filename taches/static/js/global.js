// Fonction principale (Callback attendu par le DOM)
document.addEventListener('DOMContentLoaded', function() {

    // --- VARIABLES & OBJETS ---
    const btn = document.getElementById('btn-envoyer');
    const input = document.getElementById('texte-commentaire');
    const zoneCommentaires = document.getElementById('zone-commentaires');

    // Critère : Utilisation d'objet de configuration
    const config = {
        url: '/api/ajouter-commentaire/',
        motsInterdits: ['nul', 'mauvais'] // Critère : Tableau
    };

    // --- FONCTIONS ---

    // Critère : Fonction assignée à une variable
    const validation = function(texte) {
        // Critère : Boucle et Condition
        for (let i = 0; i < config.motsInterdits.length; i++) {
            if (texte.includes(config.motsInterdits[i])) {
                alert("Restons polis !");
                return false;
            }
        }
        return true;
    };

    // Critère : Fonction de rappel (Callback) pour l'événement
    function gererClic(event) {
        let texte = input.value;
        let tacheId = btn.getAttribute('data-id');

        if (!validation(texte)) return; // Appel fonction interne

        console.log("1. Clic détecté, lancement AJAX...");

        // --- AJAX (fetch) ---
        // Critère : Données structurées JSON
        fetch(config.url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Fonction utilitaire Django standard
            },
            body: JSON.stringify({ 'contenu': texte, 'tache_id': tacheId })
        })
        .then(function(response) {
            // Critère : Asynchronisme (cette fonction s'exécute plus tard)
            console.log("3. Réponse du serveur reçue !");
            return response.json();
        })
        .then(function(data) {
            if (data.status === 'success') {
                ajouterAuDom(data.contenu, data.date); // Modification du DOM
                input.value = ""; // Reset input
            }
        });

        // Critère : Preuve d'asynchronisme
        console.log("2. Code exécuté APRES l'appel Fetch mais AVANT la réponse (Preuve Async)");
    }

    // Critère : Modification du DOM (Création de nœuds)
    function ajouterAuDom(texte, date) {
        // 1. Création de l'élément (Nœud enfant)
        let nouveauDiv = document.createElement('div');

        // 2. Configuration
        nouveauDiv.className = "commentaire";
        nouveauDiv.innerHTML = `<p><strong>${date}</strong> : ${texte}</p>`;
        nouveauDiv.style.backgroundColor = "#e0f7fa"; // Petit effet visuel

        // 3. Insertion dans l'arbre (Relation Parent/Enfant)
        // zoneCommentaires est le PARENT, nouveauDiv est l'ENFANT
        zoneCommentaires.appendChild(nouveauDiv);
    }

    // --- ÉVÉNEMENT ---
    // Critère : Gestionnaire d'événement (Event Handler)
    btn.addEventListener('click', gererClic);
});

// Fonction standard Django pour récupérer le cookie CSRF (nécessaire pour POST)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}