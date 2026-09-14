# Orange County Lettings

## Présentation

Orange County Lettings est une application web développée avec Django permettant
de consulter des annonces de locations immobilières et les profils associés.

Le projet a été refactorisé afin d'améliorer sa modularité et sa maintenabilité,
notamment grâce à la séparation des fonctionnalités en deux applications Django :
`lettings` et `profiles`.

## Fonctionnalités principales

- Consultation des locations et de leur adresse.
- Consultation des profils utilisateurs.
- Administration des données via l'interface Django.
- Monitoring des erreurs avec Sentry.

## Stack technique

- **Python 3.12+**
- **Django 6.1+**
- **SQLite** en développement
- **PostgreSQL** en production
- **uv** pour la gestion du projet et des dépendances
- **pytest / pytest-django / pytest-cov** pour les tests
- **Ruff / Flake8** pour le linting
- **Docker / Docker Hub** pour la conteneurisation
- **GitHub Actions** pour la CI/CD
- **Render** pour l'hébergement
- **Sentry** pour le monitoring

## Prérequis

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Git
- Docker, pour l'exécution depuis une image Docker

## Installation

Clonez le repository puis placez-vous dans le répertoire du projet :

    git clone <URL_DU_DEPOT>
    cd oclettings

Installez les dépendances avec `uv` :

    uv sync

Cette commande crée automatiquement l'environnement virtuel `.venv` et installe les dépendances du projet.

## Configuration

Copiez le fichier d'exemple des variables d'environnement :

    cp .env.example .env

Puis renseignez les valeurs adaptées à votre environnement, notamment `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` et, si nécessaire, `SENTRY_DSN` et `DATABASE_URL`.

En développement, l'application utilise SQLite par défaut.

## Démarrage rapide

Appliquez les migrations :

    uv run python manage.py migrate

Lancez le serveur de développement :

    uv run python manage.py runserver

L'application est alors accessible à l'adresse `http://127.0.0.1:8000/`.

L'interface d'administration est disponible à `http://127.0.0.1:8000/admin/`.

Pour l'environnement de développement fourni, les identifiants sont :

- **Utilisateur :** `admin`
- **Mot de passe :** `Abc1234!`

Ces identifiants sont réservés au développement et à la démonstration et ne doivent pas être utilisés en production.

## Tests

Exécutez la suite de tests avec :

    uv run pytest

La couverture peut être vérifiée avec :

    uv run pytest --cov=. --cov-fail-under=80

Un rapport HTML détaillé peut être généré avec :

    uv run pytest --cov=. --cov-report=html

## Docker

Une image Docker est publiée sur Docker Hub à chaque déploiement sur `main`.

Pour lancer une version précise de l'image depuis le répertoire du projet :

    docker run --rm --pull always -p 8000:8000 --env-file .env <utilisateur>/oc-lettings:<commit-sha>

Pour lancer directement la dernière version publiée :

    docker run --rm --pull always -p 8000:8000 --env-file .env <utilisateur>/oc-lettings:latest

Le fichier .env doit contenir les variables d'environnement nécessaires à l'application. Elles peuvent également être définies directement dans la commande docker run.

## CI/CD et déploiement

Le projet utilise **GitHub Actions** pour automatiser :

- les contrôles Flake8 et Ruff ;
- l'exécution des tests et la vérification de la couverture ;
- la construction et la publication de l'image Docker ;
- le déploiement sur Render.

Le pipeline est exécuté sur les `push` et `pull_request`. La construction de l'image et le déploiement sont déclenchés uniquement sur `main`.

## Documentation

La documentation technique complète du projet est disponible sur
[Read the Docs](https://ocl-oclettings.readthedocs.io/fr/latest/).
