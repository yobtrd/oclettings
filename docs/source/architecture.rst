Architecture
============

Technologies
------------

Application
~~~~~~~~~~~

- **Python 3.12+** — langage de programmation
- **Django 6.1+** — framework web
- **uv** — gestion du projet et des dépendances
- **SQLite** — base de données utilisée en développement
- **PostgreSQL** — base de données utilisée en production
- **Gunicorn** — serveur d'application WSGI
- **WhiteNoise** — gestion des fichiers statiques
- **Sentry** — monitoring et suivi des erreurs

Qualité et tests
~~~~~~~~~~~~~~~~

- **pytest** — tests automatisés
- **pytest-cov** — mesure de la couverture de code
- **Flake8** — linting
- **Ruff** — analyse statique

Déploiement
~~~~~~~~~~~

- **Docker** — conteneurisation
- **GitHub Actions** — CI/CD
- **Docker Hub** — registre d'images Docker
- **Render** — hébergement et déploiement


Structure de l'application
--------------------------

Le projet Django est organisé en trois applications :

- ``oc_lettings_site`` — configuration principale du projet et URLs globales.
- ``lettings`` — gestion des locations et des adresses.
- ``profiles`` — gestion des profils utilisateurs.

Les vues et URLs sont réparties entre les applications afin de conserver une
séparation claire des fonctionnalités.


Modèles de données
------------------

L'application repose sur les modèles suivants :

- ``User`` — modèle utilisateur fourni par Django.
- ``Profile`` — profil associé à un utilisateur.
- ``Address`` — adresse associée à une location.
- ``Letting`` — location associée à une adresse.

Les relations sont :

- ``User`` ↔ ``Profile`` : relation ``OneToOneField``.
- ``Address`` ↔ ``Letting`` : relation ``OneToOneField``.