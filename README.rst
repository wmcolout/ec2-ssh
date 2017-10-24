=======
ec2-ssh
=======

A pair of command line utilities for finding and SSH-ing into your Amazon EC2
instances by tag (such as 'Name').

Forked from Instagram original code by YPlan.

Installation
------------

Clone from GitHub:

.. code-block:: bash

    git clone git@github.com:colout/ec2-ssh.git


Install the app:

.. code-block:: bash

    cd ec2-ssh
    python setup.py install


Usage
-----

This client allows you to filter on ec2 "Roles" or "Environment" tags (Rather than ssh'ing to an IP address or hostname directly).

List all instances in the "staging" environment and choose one to ssh to:

.. code-block:: bash

    ec2-ssh -e staging
    [?] Which host?: ['staging', 'appserver', '10.11.7.186']
     > ['staging', 'appserver', '10.11.7.186']
       ['staging', 'appserver', '10.11.0.140']
       ['staging', 'database', '10.11.0.15']

    ec2-ssh connecting to 10.11.7.186

List all "appserver" instances regardless of environment and choose one to ssh to:

.. code-block:: bash

    ec2-ssh -r appserver
    [?] Which host?: ['staging', 'appserver', '10.11.7.186']
     > ['staging', 'appserver', '10.11.7.186']
       ['staging', 'appserver', '10.11.0.140']
       ['production', 'appserver', '10.12.0.41']

    ec2-ssh connecting to 10.11.7.186

SSH into the "database" instance in the "staging" environment (no selection screen since it's the only one):

.. code-block:: bash

    ec2-ssh -e staging -r appserver

    ec2-ssh connecting to 10.11.0.15

