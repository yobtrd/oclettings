Déploiement
===========

Pipeline CI/CD
--------------

Le projet utilise **GitHub Actions** pour automatiser les contrôles de qualité,
les tests, la construction de l'image Docker et le déploiement en production.

Le pipeline est défini dans le fichier :

.. code-block:: text

   .github/workflows/ci-cd.yml

Le pipeline est composé de trois jobs successifs :

.. code-block:: text

   test
     │
     ▼
   container
     │
     ▼
   deploy

Le job ``test`` est exécuté sur les événements ``push`` et ``pull_request``.
Les jobs ``container`` et ``deploy`` sont exécutés uniquement lorsqu'un
``push`` est effectué sur la branche ``main``.

Tests et linting
~~~~~~~~~~~~~~~~

Le job ``test`` s'exécute sur un environnement Ubuntu et reproduit
l'environnement Python du projet.

La version de Python utilisée est celle définie dans le fichier
``.python-version``. Les dépendances du projet sont installées à partir du
fichier ``uv.lock`` avec :

.. code-block:: bash

   uv sync --locked --dev

L'option ``--locked`` garantit que le fichier de verrouillage n'est pas
modifié pendant l'installation.

Une variable ``SECRET_KEY`` spécifique à l'environnement CI est également
définie afin de permettre l'initialisation de Django pendant l'exécution
des tests. Cette clé est uniquement utilisée dans l'environnement CI et ne
correspond pas à un secret de production.

Le code est ensuite contrôlé avec **Flake8** :

.. code-block:: bash

   uv run flake8 .

Puis avec **Ruff** :

.. code-block:: bash

   uv run ruff check .

Enfin, la suite complète de tests est exécutée avec une vérification
automatique de la couverture :

.. code-block:: bash

   uv run pytest --cov=. --cov-fail-under=80

Le paramètre ``--cov-fail-under=80`` fait échouer le job si la couverture
globale du projet est inférieure à 80 %.

Le job ``test`` constitue donc une étape obligatoire du pipeline. Les étapes
suivantes ne peuvent être exécutées que si le linting, les tests et la
couverture respectent les exigences du projet.

Construction et publication de l'image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le job ``container`` dépend de la réussite du job ``test`` :

.. code-block:: yaml

   needs: test

Il est également limité aux ``push`` effectués sur la branche ``main``.
Les modifications apportées aux autres branches ou les pull requests
n'entraînent donc pas de construction ou de publication d'image Docker.

Le job commence par une authentification auprès de **Docker Hub** à l'aide
des identifiants stockés dans les secrets GitHub :

* ``DOCKERHUB_USERNAME`` : nom d'utilisateur Docker Hub ;
* ``DOCKERHUB_TOKEN`` : token d'authentification Docker Hub.

Un identifiant court est ensuite généré à partir du hash du commit Git :

.. code-block:: bash

   GITHUB_SHA::7

L'image Docker est construite à partir du ``Dockerfile`` du projet et
publiée sur Docker Hub avec deux tags :

.. code-block:: text

   <utilisateur>/oc-lettings:<commit-sha>
   <utilisateur>/oc-lettings:latest

Le tag correspondant au hash court du commit permet d'identifier précisément
la version du code utilisée pour construire une image.

Le tag ``latest`` permet quant à lui d'identifier l'image correspondant à la
version actuellement publiée comme dernière version.

Le pipeline utilise également le cache GitHub Actions de Docker BuildKit
afin de réutiliser les couches Docker entre plusieurs constructions et ainsi
réduire leur durée.

Le ``Dockerfile`` utilise l'image officielle **UV avec Python 3.12** comme
image de base. Les dépendances de production sont installées avec :

.. code-block:: bash

   uv sync --frozen --no-dev

L'option ``--frozen`` garantit que le fichier ``uv.lock`` n'est pas modifié
pendant la construction et que les versions verrouillées sont utilisées.

Les fichiers statiques sont ensuite collectés pendant la construction de
l'image :

.. code-block:: bash

   python manage.py collectstatic --noinput

L'image utilise un utilisateur système non privilégié nommé ``nonroot`` pour
exécuter l'application, afin de ne pas faire fonctionner le serveur avec les
privilèges ``root``.

L'application est finalement démarrée avec Gunicorn sur le port ``8000``.

Lancement d'une image en local
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Depuis le répertoire racine du projet, l'image peut être récupérée et lancée
en une seule commande :

.. code-block:: bash

   docker run --rm --pull always -p 8000:8000 \
       --env-file .env <utilisateur>/oc-lettings:<commit-sha>

L'option ``--pull always`` force Docker à vérifier et récupérer l'image depuis
Docker Hub avant son lancement.

Le fichier ``.env`` doit être présent dans le répertoire courant et contenir
la configuration nécessaire à l'application, notamment ``DEBUG=False``.

Le tag ``<commit-sha>`` permet d'utiliser précisément la version correspondant
à un commit donné. Pour lancer directement la dernière version publiée, le
tag ``latest`` peut être utilisé :

.. code-block:: bash

   docker run --rm --pull always -p 8000:8000 \
       --env-file .env <utilisateur>/oc-lettings:latest

L'application est alors accessible depuis le navigateur à l'adresse
``http://127.0.0.1:8000/``.


Déploiement sur Render
~~~~~~~~~~~~~~~~~~~~~~

Le job ``deploy`` dépend de la réussite du job ``container`` :

.. code-block:: yaml

   needs: container

Il est, comme le job de conteneurisation, limité aux ``push`` effectués sur
la branche ``main``.

Le déploiement est déclenché à l'aide d'un **Deploy Hook Render** stocké dans
les secrets GitHub sous le nom ``RENDER_DEPLOY_HOOK_URL``.

Le pipeline transmet à Render l'image Docker correspondant au commit qui
vient d'être publié sur Docker Hub :

.. code-block:: text

   docker.io/<utilisateur>/oc-lettings:<commit-sha>

Render utilise alors cette image pour mettre en service la nouvelle version
de l'application.

La chaîne de dépendances des jobs garantit l'ordre suivant :

.. code-block:: text

   Push sur main
       │
       ▼
   Tests + linting + couverture
       │
       │ succès
       ▼
   Construction + publication Docker
       │
       │ succès
       ▼
   Déploiement Render

Ainsi, une image Docker ne peut pas être publiée si les contrôles de qualité
ou les tests échouent. De même, un déploiement ne peut pas être déclenché si
la construction et la publication de l'image Docker ont échoué.

Les ``pull_request`` et les ``push`` effectués sur les autres branches
exécutent uniquement le job ``test``.

Mise en production
------------------

Base de données de production
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

L'application utilise PostgreSQL en production. La variable
``DATABASE_URL`` doit être configurée avec l'URL de connexion à la base
PostgreSQL cible.

Deux méthodes sont possibles pour effectuer les opérations Django sur cette
base.

Choix 1 : configurer ``DATABASE_URL`` dans l'hébergeur
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La variable ``DATABASE_URL`` est définie dans les variables d'environnement
de l'hébergeur :

- ``DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>``

Cette configuration permet à l'application déployée de se connecter
automatiquement à PostgreSQL.

Si l'hébergeur ne fournit pas d'accès à un shell, les commandes Django
destinées à la base de production peuvent être exécutées depuis
l'environnement local en définissant ``DATABASE_URL`` directement dans la
commande :

.. code-block:: bash

    DATABASE_URL="postgresql://<user>:<password>@<host>:<port>/<database>" \
    uv run python manage.py <commande>

Choix 2 : configurer ``DATABASE_URL`` dans ``.env``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La variable ``DATABASE_URL`` peut également être définie dans le fichier
``.env`` local :

- ``DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>``

Les commandes Django peuvent alors être exécutées depuis l'environnement
local sans modifier la commande elle-même.


Création d'un superutilisateur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Un superutilisateur Django doit être créé afin d'accéder à l'interface
d'administration de l'application.

Avec le choix 1, exécutez :

.. code-block:: bash

    DATABASE_URL="postgresql://<user>:<password>@<host>:<port>/<database>" \
    uv run python manage.py createsuperuser

Avec le choix 2, exécutez simplement :

.. code-block:: bash

    uv run python manage.py createsuperuser

Migration des données
~~~~~~~~~~~~~~~~~~~~~

Les données existantes peuvent être transférées de la base SQLite locale
vers la base PostgreSQL de production.

Export des données
^^^^^^^^^^^^^^^^^^

Depuis l'environnement local, exportez les données avec :

.. code-block:: bash

    uv run python manage.py export_data

Cette commande génère un fichier ``data.json`` contenant les données de
l'application, à l'exception des superutilisateurs.

Import des données
^^^^^^^^^^^^^^^^^^

Avec le choix 1, si l'import est effectué depuis l'environnement local,
définissez ``DATABASE_URL`` directement dans la commande :

.. code-block:: bash

    DATABASE_URL="postgresql://<user>:<password>@<host>:<port>/<database>" \
    uv run python manage.py loaddata data.json

Avec le choix 2, exécutez simplement :

.. code-block:: bash

    uv run python manage.py loaddata data.json

Monitoring et Sentry
--------------------

L'application utilise **Sentry** pour surveiller les erreurs et faciliter
leur diagnostic. Le SDK Sentry est installé comme dépendance de production
et utilise la variable d'environnement ``SENTRY_DSN`` pour identifier le
projet Sentry auquel les événements doivent être transmis.

Configuration de Sentry
~~~~~~~~~~~~~~~~~~~~~~~

La variable ``SENTRY_DSN`` peut être configurée dans chaque environnement.
Sa configuration générale est décrite dans la section
:ref:`configuration <configuration>`.

En développement, le DSN peut être renseigné dans le fichier ``.env`` :

.. code-block:: text

    SENTRY_DSN=<DSN_SENTRY>

Cela permet notamment de vérifier le fonctionnement de l'intégration Sentry
depuis l'environnement local.

En production, le DSN est configuré directement dans les variables
d'environnement de Render. Il n'est donc pas nécessaire de l'intégrer à
l'image Docker ou au dépôt Git.

Configuration du logging
~~~~~~~~~~~~~~~~~~~~~~~~

L'application utilise le module standard ``logging`` de Python afin de
suivre son activité et de faciliter le diagnostic des problèmes.

Les loggers Django, ``lettings`` et ``profiles`` sont configurés avec un
niveau ``INFO`` et écrivent leurs messages vers la sortie standard.

Des logs sont ajoutés aux endroits pertinents du code afin de signaler les
opérations importantes et les situations inhabituelles.

Par exemple, la consultation d'une location est enregistrée au niveau
``INFO`` tandis qu'une location inexistante génère un avertissement :

.. code-block:: python

    logger.info("Viewing letting with id %s", letting_id)

    try:
        letting = get_object_or_404(Letting, id=letting_id)
    except Http404:
        logger.warning("Letting not found with id %s", letting_id)
        raise

Ces logs permettent de disposer d'informations complémentaires lors de
l'analyse du comportement de l'application.

Vérification
~~~~~~~~~~~~

Après le déploiement, le bon fonctionnement du monitoring peut être vérifié
depuis l'interface Sentry en s'assurant que les événements générés par
l'application sont correctement reçus.

Les logs de l'application peuvent également être consultés depuis
l'environnement d'hébergement afin de vérifier que les messages de
journalisation sont correctement produits.

Vérification après déploiement
------------------------------

Après le déploiement, les éléments suivants doivent être vérifiés afin de
s'assurer que l'application fonctionne correctement en production.

Application
~~~~~~~~~~~

- Accéder à l'URL de l'application et vérifier que la page d'accueil
  s'affiche correctement.
- Vérifier la navigation vers les locations et les profils.
- Vérifier qu'une page inexistante renvoie correctement une erreur 404.
- Vérifier qu'une erreur serveur est correctement prise en charge par la
  page 500.

Fichiers statiques
~~~~~~~~~~~~~~~~~~

Vérifier que les fichiers statiques sont correctement chargés :

- feuilles de style CSS ;
- images ;
- autres ressources statiques nécessaires à l'interface.

Administration
~~~~~~~~~~~~~~

Accéder à l'interface d'administration avec le superutilisateur créé
précédemment et vérifier :

- l'accès à l'interface ;
- l'affichage correct des pages ;
- la présence des modèles ``Address``, ``Letting`` et ``Profile`` ;
- la bonne gestion de la pluralisation de ``Address``.

