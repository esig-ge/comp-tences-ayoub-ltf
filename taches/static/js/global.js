function creerLigneTable(data) {

    const dateAffichage = data.date_due || '<span class="badge bg-secondary">Non définie</span>';
    const descriptionAffichage = data.description || '— Aucune description —';

     const monTr = document.createElement('tr');
     const monTd = document.createElement("td");

     monTr.textContent = data.titre
    monTd.href= "/modifier-tache/${data.id}/"
    monTd.appendChild(data.titre)
    monTd.appendChild(data.description)

    return `
        <tr data-tache-id="${data.id}">
            <td><strong>${data.titre}</strong></td>
            <td>${descriptionAffichage}</td>
            <td><span class="badge bg-warning text-dark">En cours</span></td>
            <td>
                <a href="/basculer-statut/${data.id}/" class="btn btn-sm btn-outline-success me-2">✅ Valider</a>
                <a href="/modifier-tache/${data.id}/" class="btn btn-sm btn-primary me-2">Modifier</a>
                <a href="/supprimer-tache/${data.id}/" class="btn btn-sm btn-danger">Supprimer</a>
            </td>
            <td>${dateAffichage}</td>
        </tr>
    `;
}

document.addEventListener('DOMContentLoaded', function() {

    const btn = document.getElementById('btn-add-ajax');
    const inputTitre = document.getElementById('titre-tache-ajax');
    const inputDescription = document.getElementById('description-tache-ajax');
    const inputDateDue = document.getElementById('due-date-ajax');
    const tBodyTache = document.getElementById('tbody_taches');
    const inputCSRF = document.querySelector('input[name="csrfmiddlewaretoken"]').value;


    btn.addEventListener('click', function() {
        const titre = inputTitre.value.trim();
        const description = inputDescription.value.trim();
        const date = inputDateDue.value.trim();
        console.log('La tâche va être ajoutée !');

        if(titre === ""){
            alert("Le titre est obligatoire !");
            return;
        }

        fetch('/api/ajouter_tache', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': inputCSRF
            },
            body: JSON.stringify({
                titre: titre,
                description: description || null,
                date: date || null
            })
        })

        .then(response => {
            if (!response.ok) {
                // Si le serveur renvoie 400 ou 500, on passe au .catch()
                throw new Error(`HTTP Error: ${response.status} - Vérifiez la console serveur (Django).`);
            }
            return response.json();
        })
        .then(data => {
            // 1. Vérifie si le serveur a retourné un succès
            if (data.status === 'ok') {

                // 2. Création du nouveau nœud HTML
                const newRowHtml = creerLigneTable(data);

                // 3. Ajout du nœud au début du tbody (Modification significative du DOM)
                tBodyTache.insertAdjacentHTML('afterbegin', newRowHtml);

                inputTitre.value = '';
                inputDescription.value = '';
                inputDateDue.value = '';
                console.log(`Tâche #${data.id} ajoutée avec succès!`);

            } else {
                // Erreur logique renvoyée par le JSON de Django
                alert(`Erreur du serveur (400) : ${data.message}` );
            }
        })
        .catch(error => {
            // Gère les erreurs réseau, parsing JSON, ou celles lancées par le throw ci-dessus
            console.error(error);
            alert(`Échec de la requête: ${error.message || error}`);
        });

    });

});