function creerLigneTable(data) {
    // 1. Gestion de la date (si null, on met un badge)
    var dateAffichage = data.date_due;
    if (!dateAffichage) {
        dateAffichage = '<span class="badge bg-secondary">Non définie</span>';
        }

    // 2. Gestion de la description
    var descriptionAffichage = data.description;
    if (!descriptionAffichage) {
        descriptionAffichage = '— Aucune description —';
    }


    // Création de la ligne
    var monTr = document.createElement('tr');
    monTr.dataset.tacheId = data.id;

    // Colonne Titre
    var tdTitre = document.createElement("td");
    tdTitre.innerHTML = '<strong>' + data.titre + '</strong>';
    monTr.appendChild(tdTitre);

    // Colonne Description
    var tdDescription = document.createElement("td");
    tdDescription.innerHTML = descriptionAffichage;
    monTr.appendChild(tdDescription);

    // Colonne Statut
    var tdStatut = document.createElement("td");
    tdStatut.innerHTML = '<span class="badge bg-warning text-dark">En cours</span>';
    monTr.appendChild(tdStatut);

    // Colonne Date
    var tdDate = document.createElement("td");
    tdDate.innerHTML = dateAffichage;
    monTr.appendChild(tdDate);

    // Colonne Actions
    var tdActions = document.createElement("td");
    tdActions.innerHTML = '<a href="/basculer-statut/' + data.id + '/" class="btn btn-sm btn-outline-success me-2">✅ Valider</a>' +
                          '<a href="/modifier-tache/' + data.id + '/" class="btn btn-sm btn-primary me-2">Modifier</a>' +
                          '<a href="/supprimer-tache/' + data.id + '/" class="btn btn-sm btn-danger">Supprimer</a>';
    monTr.appendChild(tdActions);

    // Suppression de la ligne "Aucune tâche" si elle existe
    var noTaskRow = document.getElementById('no-task-row');
    if (noTaskRow) {
        noTaskRow.remove();
    }

    return monTr;
}

document.addEventListener('DOMContentLoaded', function() {

    // Sélection des éléments HTML
    var btn = document.getElementById('btn-add-ajax');
    var inputTitre = document.getElementById('titre-tache-ajax');
    var inputDesc = document.getElementById('description-tache-ajax');
    var inputDate = document.getElementById('due-date-ajax');
    var tBodyTache = document.getElementById('tbody_taches');
    var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    // Clic sur le bouton
    btn.addEventListener('click', function() {

        var valTitre = inputTitre.value.trim();
        var valDesc = inputDesc.value.trim();
        var valDate = inputDate.value.trim();

        console.log('La tâche va être ajoutée via XHR !');

        if (valTitre === "") {
            alert("Le titre est obligatoire !");
            return;
        }

        // Préparation des données
        var postData = JSON.stringify({
            titre: valTitre,
            description: valDesc || null,
            date_due: valDate || null
        });

        // Requête AJAX
        var xhr = new XMLHttpRequest();
        xhr.open("POST", '/api/ajouter_tache', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-CSRFToken', csrfToken);

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    try {
                        var data = JSON.parse(xhr.responseText);

                        if (data.status === 'ok') {
                            // Création et ajout de la ligne
                            var newRow = creerLigneTable(data);
                            tBodyTache.prepend(newRow);

                            // Vider les champs
                            inputTitre.value = '';
                            inputDesc.value = '';
                            inputDate.value = '';

                            console.log('Réponse reçue. Tâche #' + data.id + ' ajoutée avec succès!');

                        } else {
                            alert('Erreur du serveur : ' + data.message);
                        }
                    } catch (e) {
                        console.error("Erreur de parsing JSON:", e, xhr.responseText);
                        alert("Erreur: Réponse serveur non valide (non-JSON).");
                    }
                } else {
                    console.error('Erreur HTTP: ' + xhr.status + ' - ' + xhr.statusText);
                    alert('Échec de la requête: HTTP ' + xhr.status);
                }
            }
        };

        xhr.send(postData);
    });
});