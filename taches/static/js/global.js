function creerLigneTable(data) {
    // Définition des valeurs
    const dateAffichage = data.date_due || '<span class="badge bg-secondary">Non définie</span>';
    const descriptionAffichage = data.description || '— Aucune description —';

    const monTr = document.createElement('tr');
    monTr.dataset.tacheId = data.id;

    const tdTitre = document.createElement("td");
    tdTitre.innerHTML = `<strong>${data.titre}</strong>`;
    monTr.appendChild(tdTitre);

    const tdDescription = document.createElement("td");
    tdDescription.innerHTML = descriptionAffichage;
    monTr.appendChild(tdDescription);

    const tdStatut = document.createElement("td");
    tdStatut.innerHTML = '<span class="badge bg-warning text-dark">En cours</span>';
    monTr.appendChild(tdStatut);

    const tdDate = document.createElement("td");
    tdDate.innerHTML = data.date_due || '<span class="badge bg-secondary">Non définie</span>';
    monTr.appendChild(tdDate);

    // 5. ACTIONS (IMPORTANT : Position 5 - La fin)
    const tdActions = document.createElement("td");
    tdActions.innerHTML = `
        <a href="/basculer-statut/${data.id}/" class="btn btn-sm btn-outline-success me-2">✅ Valider</a>
        <a href="/modifier-tache/${data.id}/" class="btn btn-sm btn-primary me-2">Modifier</a>
        <a href="/supprimer-tache/${data.id}/" class="btn btn-sm btn-danger">Supprimer</a>
    `;
    monTr.appendChild(tdActions);

    const noTaskRow = document.getElementById('no-task-row');
    if (noTaskRow) {
        noTaskRow.remove();
    }

    return monTr;
}

document.addEventListener('DOMContentLoaded', function() {

    // Initialisation compacte des variables de l'interface (éléments du DOM)
    const { btn, titre, description, dateDue, tBodyTache, csrfToken } = {
        btn: document.getElementById('btn-add-ajax'),
        titre: document.getElementById('titre-tache-ajax'),
        description: document.getElementById('description-tache-ajax'),
        dateDue: document.getElementById('due-date-ajax'),
        tBodyTache: document.getElementById('tbody_taches'),
        csrfToken: document.querySelector('input[name="csrfmiddlewaretoken"]').value
    };

    // Écoute de l'événement click sur le bouton d'ajout (Callback)
    btn.addEventListener('click', function() {
        // Initialisation des variables avec les données utilisateur
        const dataTitre = titre.value.trim();
        const dataDescription = description.value.trim();
        const dataDate = dateDue.value.trim();
        console.log('La tâche va être ajoutée via XHR !');

        // Validation du titre
        if (dataTitre === "") {
            alert("Le titre est obligatoire !");
            return;
        }

        const postData = JSON.stringify({
        titre: dataTitre,
        description: dataDescription || null,
        date_due: dataDate || null

        });

        // Création d'une requête XMLHttpRequest (similaire à l'exemple)
        var xhr = new XMLHttpRequest();
        // Configuration : POST sur l'URL, mode asynchrone (true)
        xhr.open("POST", '/api/ajouter_tache', true);

        // Ajout des Headers requis (Content-Type pour le JSON et X-CSRFToken pour Django)
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-CSRFToken', csrfToken);


        // Gestion de la réponse (Fonction de rappel asynchrone)
        xhr.onreadystatechange = function () {
            // Mettre à jour la variable une fois la réponse reçue (État 4 = TERMINE)
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    try {
                        // Tente de parser la réponse JSON
                        const data = JSON.parse(xhr.responseText);

                        // Test du statut logique renvoyé par le serveur
                        if (data.status === 'ok') {

                            // Création du nouveau nœud DOM <tr> (Manipulation du DOM)
                            const newRow = creerLigneTable(data);

                            // Insertion du nœud au début du tbody
                            tBodyTache.prepend(newRow); // <-- Ajout de nœud significatif

                            // Nettoyage des champs de formulaire
                            titre.value = description.value = dateDue.value = '';
                            console.log(`Réponse reçue. Tâche #${data.id} ajoutée avec succès!`);

                        } else {
                            // Erreur logique JSON
                            alert(`Erreur du serveur : ${data.message}` );
                        }
                    } catch (e) {
                        // Erreur si la réponse n'est pas un JSON valide
                        console.error("Erreur de parsing JSON:", e, xhr.responseText);
                        alert("Erreur: Réponse serveur non valide (non-JSON).");
                    }
                } else {
                    // Gère les erreurs HTTP (400, 500, etc.)
                    console.error(`Erreur HTTP: ${xhr.status} - ${xhr.statusText}`);
                    alert(`Échec de la requête: HTTP ${xhr.status}`);
                }
            }
        };

        // Envoi de la requête avec les données POST
        xhr.send(postData);

    });

});
