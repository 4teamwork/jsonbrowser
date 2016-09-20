jsonbrowser
=============

Installation for local development
----------------------------------

Install Elasticsearch
^^^^^^^^^^^^^^^^^^^^^

Install ES via your preferred method. Installing the kopf plugin is recommended:

.. code::

    bin/plugin install lmenezes/elasticsearch-kopf


Install JSONBrowser
^^^^^^^^^^^^^^^^^^^

Create a virtualenv:

.. code::

    virtualenv-2.7 --no-site-packages jsonbrowser-env
    cd jsonbrowser-env/
    source bin/activate


Clone the package and install it as a development egg

.. code::

    mkdir src
    cd src
    git clone git@github.com:4teamwork/jsonbrowser.git
    cd jsonbrowser
    python setup.py develop
    cd ../..

Create a configuration

.. code::

    # Create the Flask instance folder - holds config and variable data
    mkdir -p var/jsonbrowser.flask_app-instance

    cp src/jsonbrowser/jsonbrowser.cfg.example var/jsonbrowser.flask_app-instance/jsonbrowser.cfg

    # Change SESSION_SECRET
    vim var/jsonbrowser.flask_app-instance/jsonbrowser.cfg


Add a JSON dataset and index it
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add a dataset (a collection of ``<portal_type>.json`` files) to
``var/jsonbrowser.flask_app-instance/dataset``, or use the provided example
dataset:

.. code::

    cp -r src/jsonbrowser/example_datasets/small var/jsonbrowser.flask_app-instance/dataset

Then run JSONBrowser and select `Manage > Reindex` from the menu. This will
(re)index the JSON dataset in that location into ES.

.. note::

    The ES index identified by ``ES_INDEX_NAME`` in the configuration will be
    **DROPPED** and and repopulated by the ``Reindex`` action!

Running JSONBrowser
^^^^^^^^^^^^^^^^^^^

.. code::

    bin/elasticsearch
    run-jsonbrowser     # (inside activated venv)

Open http://localhost:5000/
