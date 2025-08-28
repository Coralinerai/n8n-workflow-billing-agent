# 🧠 README – Workflow N8N : Agent IA de Facturation

Ce fichier accompagne le workflow `Wworkflow.json` et `alert-system.json` (exporté depuis N8N) et décrit les éléments à reconfigurer pour que le système fonctionne sur une autre instance.

---

## 🔐 Credentials

Les nœuds Gmail, Google Drive, Google Sheets et OpenAI utilisés dans ce workflow référencent des comptes par leur nom (ex : `Gmail account`, `Google Drive account 2`).

➡️ **Aucun secret ou clé n'est inclus** dans le fichier `.json`.  
➡️ Vous devez **reconfigurer les credentials manuellement** dans N8N.

### À faire dans N8N :
- Ajouter vos propres credentials (OAuth2, API key…)
- Leur donner les **mêmes noms** que dans le workflow si possible (ex: `Gmail account`) pour éviter de reconnecter chaque nœud

---

## 📁 Noms de dossiers Google Drive et fichiers

Des nœuds utilisent :
- Un **dossier Google Drive** (`n8n_test`)
- Une **feuille Google Sheets** (`factures_test`)

Ces ressources appartiennent à un compte Google personnel.

➡️ **Vous devez recréer vos propres dossiers et feuilles**, puis mettre à jour :
- les `folderId` dans les nœuds Google Drive
- les `documentId` et `sheetName` dans les nœuds Google Sheets

---
🐇 RabbitMQ

Le workflow utilise RabbitMQ pour la gestion des tâches.

➡️ À faire côté utilisateur :

Créer une queue RabbitMQ nommée factures_à_traiter

Vérifier que les credentials et la connexion RabbitMQ sont correctement configurés dans N8N

##  Fichier JSON du workflow

Le fichier `workflows/workflow.json` contient :
- Tous les nœuds du workflow 
- Les noms des credentials utilisés (mais pas les secrets)
- Les chemins des fichiers et noms de documents Google utilisés

Il peut être importé depuis N8N via **Workflows → Import from file**.


---
Le fichier `workflows/alert-system.json` contient :
- Tous les nœuds du système des alertes de paiement 
- Les noms des credentials utilisés (mais pas les secrets)
- Les chemins des fichiers et noms de documents Google utilisés

Il peut être importé depuis N8N via **Workflows → Import from file**.


## ❗ Points à adapter côté utilisateur

- Configurer **les credentials N8N**
- Créer ses **propres ressources Google Drive et Sheets**
- Vérifier les noms de fichiers générés (ils sont dynamiques, mais modifiables)

---

