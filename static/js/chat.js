    // Fonction requise par Django pour sécuriser les requêtes POST (CSRF Token)
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

    async function sendMessage() {
        const inputField = document.getElementById('chat-input');
        const message = inputField.value;
        const chatHistory = document.getElementById('chat-history');

        if (!message) return; // Ne rien faire si c'est vide

        // 1. Afficher le message de l'utilisateur
        chatHistory.innerHTML += `<p style="margin: 5px 0; text-align: right;"><span style="background: #e3f2fd; padding: 5px 10px; border-radius: 15px; display: inline-block;">${message}</span></p>`;
        inputField.value = ''; // On vide le champ

        // Petit message d'attente
        const typingId = "typing-" + Date.now();
        chatHistory.innerHTML += `<p id="${typingId}" style="margin: 5px 0; font-size: 12px; color: gray;"><em>ProCoach réfléchit...</em></p>`;
        chatHistory.scrollTop = chatHistory.scrollHeight; // Scroll automatique vers le bas

        // 2. Envoyer la requête à notre vue Django 'chat_with_coach'
        try {
            const response = await fetch('/chat-coach/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Sécurité Django obligatoire
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            // On retire le message "réfléchit..."
            document.getElementById(typingId).remove();

            if (response.ok) {
                // 3. Afficher la réponse de l'IA
                // On remplace les sauts de ligne par des balises <br> pour un bel affichage
                const formattedReply = data.reply.replace(/\n/g, '<br>');
                chatHistory.innerHTML += `<p style="margin: 5px 0;"><span style="background: #fff; border: 1px solid #ddd; padding: 5px 10px; border-radius: 15px; display: inline-block;">${formattedReply}</span></p>`;

                // --- 4. GESTION D'ÉTAT (Le critère de célébration !) ---
                // Si l'IA a utilisé un outil, nos fonctions Python renvoient "Action réussie".
                // Si on voit ce mot-clé, on rafraîchit la page pour voir la nouvelle tâche apparaître !
                if (data.reply.includes("Action réussie")) {
                    setTimeout(() => {
                        window.location.reload();
                    }, 1500); // On attend 1,5 seconde pour laisser le temps de lire
                }

            } else {
                chatHistory.innerHTML += `<p style="color: red; font-size: 12px;">Erreur serveur: ${data.error}</p>`;
            }
        } catch (error) {
            document.getElementById(typingId).remove();
            chatHistory.innerHTML += `<p style="color: red; font-size: 12px;">Erreur de connexion.</p>`;
        }

        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    // Permet d'envoyer le message en appuyant sur la touche "Entrée"
    document.getElementById('chat-input').addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
