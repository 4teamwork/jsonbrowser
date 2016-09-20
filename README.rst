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
    . bin/activate


Clone the package and provide a configuration

.. code::

    mkdir src
    git clone git@github.com:4teamwork/jsonbrowser.git src/jsonbrowser

    mkdir -p var/jsonbrowser.flask_app-instance
    cp src/jsonbrowser/jsonbrowser.cfg.default var/jsonbrowser.flask_app-instance/jsonbrowser.cfg

    # Change SESSION_SECRET
    vim var/jsonbrowser.flask_app-instance/jsonbrowser.cfg


Install the package as a development egg:

.. code::

    cd jsonbrowser/
    python setup.py develop


Running JSONBrowser
^^^^^^^^^^^^^^^^^^^

.. code::

    bin/elasticsearch
    run-jsonbrowser     # (inside activated venv)

Add JSON datasets and index them
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TODO: Document!
