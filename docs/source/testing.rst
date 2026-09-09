Tests
=====

L'application dispose d'une suite de tests automatisés permettant de vérifier le bon
fonctionnement de ses différentes fonctionnalités. Les tests couvrent notamment les
modèles, les vues et les URL des applications ``lettings`` et ``profiles``.

Les tests sont exécutés avec **pytest** et **pytest-django**, tandis que **pytest-cov**
permet de mesurer la couverture du code.

Les outils **Ruff** et **Flake8** sont également utilisés afin de contrôler la qualité
et la conformité du code source.

Exécution de la suite de tests
------------------------------

L'ensemble des tests peut être exécuté depuis la racine du projet avec la commande :

.. code-block:: bash

   pytest

La configuration de pytest est définie dans le fichier ``pyproject.toml`` :

.. code-block:: toml

   [tool.pytest.ini_options]
   DJANGO_SETTINGS_MODULE = "oc_lettings_site.settings"
   python_files = ["test_*.py", "tests.py"]
   addopts = "-v"

Le paramètre ``DJANGO_SETTINGS_MODULE`` indique à pytest la configuration Django à
utiliser pour les tests.

Le paramètre ``python_files`` permet à pytest de détecter les fichiers de tests selon
les conventions utilisées dans le projet.

L'option ``-v`` active le mode verbeux et permet d'afficher le détail des tests
exécutés.

Organisation des tests
~~~~~~~~~~~~~~~~~~~~~~

Les tests sont organisés au niveau de chaque application afin de conserver une
structure cohérente avec l'architecture du projet.

L'application principale ``oc_lettings_site`` contient un fichier ``tests.py`` pour
ses tests.

Les applications ``lettings`` et ``profiles`` disposent chacune d'un répertoire
``tests`` contenant trois fichiers dédiés :

.. code-block:: text

   lettings/
   └── tests/
       ├── test_models.py
       ├── test_url.py
       └── test_view.py

   profiles/
   └── tests/
       ├── test_models.py
       ├── test_url.py
       └── test_view.py

Cette organisation permet de séparer les tests selon la fonctionnalité testée :

* ``test_models.py`` vérifie le comportement des modèles Django ;
* ``test_url.py`` vérifie la configuration et le fonctionnement des URL ;
* ``test_view.py`` vérifie le comportement des vues.

Les tests peuvent également être exécutés individuellement en indiquant le fichier
ou le répertoire concerné. Par exemple :

.. code-block:: bash

   pytest lettings/tests/test_models.py
   pytest profiles/tests/test_view.py

Couverture
----------

La couverture du code est mesurée avec **pytest-cov**. Elle permet de déterminer la
proportion du code source exécutée par la suite de tests.

Pour afficher la couverture directement dans le terminal :

.. code-block:: bash

   pytest --cov=.

Un rapport détaillé au format HTML peut également être généré :

.. code-block:: bash

   pytest --cov=. --cov-report=html

Cette commande génère un répertoire ``htmlcov`` contenant le rapport de couverture.
Le fichier ``htmlcov/index.html`` peut ensuite être ouvert dans un navigateur afin
d'analyser la couverture fichier par fichier et ligne par ligne.

La couverture du projet doit être supérieure à **80 %**, conformément aux exigences
du projet.

Linting
-------

Deux outils sont utilisés pour contrôler la qualité du code Python : **Ruff** et
**Flake8**.

Ruff
~~~~

Ruff est utilisé pour effectuer une analyse statique du code et détecter différents
problèmes de qualité, de style et de bonnes pratiques.

La configuration de Ruff se trouve dans le fichier ``pyproject.toml`` :

.. code-block:: toml

   [tool.ruff]
   target-version = "py312"
   line-length = 99

   [tool.ruff.lint]
   select = ["E", "W", "F", "I", "B", "UP", "N"]

Les catégories activées correspondent aux contrôles suivants :

* ``E`` : erreurs de style selon les règles pycodestyle ;
* ``W`` : avertissements de style selon pycodestyle ;
* ``F`` : erreurs détectées par Pyflakes, notamment les imports inutilisés ou les
  variables non définies ;
* ``I`` : organisation et tri des imports ;
* ``B`` : détection de certaines mauvaises pratiques et erreurs potentielles avec
  flake8-bugbear ;
* ``UP`` : règles permettant de moderniser le code Python en fonction de la version
  utilisée ;
* ``N`` : conventions de nommage Python.

Le projet cible Python 3.12 et utilise une longueur maximale de ligne de 99 caractères.

Pour lancer l'analyse Ruff :

.. code-block:: bash

   ruff check .

Ruff peut également corriger automatiquement une partie des problèmes détectés :

.. code-block:: bash

   ruff check . --fix

Les migrations Django, les environnements virtuels et les fichiers temporaires sont
exclus de l'analyse conformément à la configuration du projet.

Flake8
~~~~~~

Flake8 est utilisé comme outil complémentaire de vérification du code source. Sa
configuration est définie dans ``setup.cfg`` :

.. code-block:: ini

   [flake8]
   max-line-length = 99
   exclude = **/migrations/*,venv,.venv

La configuration existante a été conservée et n'a pas été modifiée, conformément aux
exigences du projet.

Pour lancer l'analyse avec Flake8 :

.. code-block:: bash

   flake8 .

Cette vérification permet notamment de détecter les erreurs de syntaxe, les problèmes
de style et certaines erreurs courantes dans le code Python.
