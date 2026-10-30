# United States Postal Inspection Service — portail d'enquête

Socle initial du portail RedM, avec une identité administrative inspirée de 1890.

## Technologies
- Python et Flask
- Flask-Login pour les sessions
- Flask-WTF pour la protection CSRF
- SQLAlchemy pour les données
- PostgreSQL en hébergement (SQLite pour les essais locaux)
- Gunicorn pour le serveur web

## Démarrage local
1. Installer Python 3.11 ou plus récent.
2. Créer puis activer un environnement virtuel : `python -m venv .venv`
3. Installer les dépendances : `pip install -r requirements.txt`
4. Définir `SECRET_KEY` dans les variables d'environnement.
5. Initialiser les tables : `flask --app run.py init-db`
6. Créer le premier administrateur : `flask --app run.py create-admin`
7. Lancer : `python run.py`

## Déploiement Render
- Créer une base Render PostgreSQL.
- Créer un Web Service relié au dépôt GitHub privé.
- Build command : `pip install -r requirements.txt`
- Start command : `gunicorn run:app`
- Ajouter `SECRET_KEY`, `DATABASE_URL` et `COOKIE_SECURE=true` aux variables d'environnement.
- Utiliser l'URL PostgreSQL interne fournie par Render si le service et la base sont dans la même région.
- Après le premier déploiement, exécuter `flask --app run.py init-db` puis `flask --app run.py create-admin` dans le shell du service.

## État du projet
Cette version est un socle de départ : connexion, tableau de bord et modèles de données initiaux. Les rubriques Enquêtes, Suspects, Preuves, Rapports, Mandats, Personnel et Carte sont prévues dans la navigation et les modèles, mais leurs écrans de gestion restent à développer.

Avant toute utilisation réelle, compléter les contrôles d'accès par dossier, la limitation des tentatives de connexion, le journal d'audit, la politique de sauvegarde et la gestion sécurisée des pièces jointes. Ne pas y saisir de données personnelles réelles tant que ces éléments ne sont pas finalisés.
