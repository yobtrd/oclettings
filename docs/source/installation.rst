Installation
============

Prérequis
---------

Les éléments suivants doivent être installés sur la machine :

- `Python 3.12+ <https://www.python.org/>`_
- `uv <https://docs.astral.sh/uv/>`_ — pour la gestion de l'environnement et des dépendances
- `Git <https://git-scm.com/>`_ — pour cloner le dépôt (optionnel)


Installation
------------

Clonez le dépôt :

.. code-block:: bash

    git clone <URL_DU_DEPOT>

Placez-vous dans le répertoire du projet :

.. code-block:: bash

    cd oclettings

Installez les dépendances du projet :

.. code-block:: bash

    uv sync

Cette commande crée automatiquement l'environnement virtuel ``.venv`` s'il
n'existe pas et installe les dépendances de l'application ainsi que les
dépendances de développement nécessaires aux tests, au linting et à la
documentation.

.. _configuration:

Configuration
-------------

Variables d'environnement
~~~~~~~~~~~~~~~~~~~~~~~~~

La configuration de l'application est définie à l'aide de variables
d'environnement. Un fichier ``.env.example`` est fourni à la racine du
projet avec l'ensemble des variables nécessaires.

Copiez ce fichier afin de créer votre configuration locale :

.. code-block:: bash

    cp .env.example .env

Puis adaptez les valeurs à votre environnement.

Les principales variables sont :

- ``ENVIRONMENT`` — environnement d'exécution de l'application
  (``development``, ``test`` ou ``production``).
- ``SECRET_KEY`` — clé secrète utilisée par Django.
- ``DEBUG`` — active ou désactive le mode debug de Django.
- ``SENTRY_DSN`` — DSN Sentry utilisé pour le monitoring des erreurs.
- ``ALLOWED_HOSTS`` — liste des hôtes autorisés, séparés par des virgules.
- ``DATABASE_URL`` — URL de connexion à la base de données.

Base de données
~~~~~~~~~~~~~~~

Développement
^^^^^^^^^^^^^

En développement, l'application utilise SQLite. Si ``DATABASE_URL`` est
vide ou n'est pas définie, Django utilise automatiquement la base
``oc-lettings-site.sqlite3`` située à la racine du projet.

La base SQLite fournie avec le projet contient les données nécessaires au
fonctionnement de l'application.

Appliquer les migrations
^^^^^^^^^^^^^^^^^^^^^^^^

Après l'installation du projet, appliquez les migrations Django afin de
s'assurer que la structure de la base de données correspond à la version
actuelle de l'application :

.. code-block:: bash

    uv run python manage.py migrate

Sécurité
~~~~~~~~

La variable ``SECRET_KEY`` doit contenir une valeur unique et suffisamment
sécurisée pour chaque environnement.

Les variables d'environnement contenant des informations sensibles ne
doivent jamais être versionnées dans le dépôt. Utilisez le fichier
``.env.example`` comme modèle et conservez les valeurs réelles dans votre
fichier ``.env``.

Démarrage rapide
----------------

Une fois les variables d'environnement nécessaires configurées, lancez le serveur
de développement :

.. code-block:: bash

    uv run python manage.py runserver

