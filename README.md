Tempest Integration of Tungsten Fabric (Contrail)
=================================================

This directory contains Tempest tests to cover the contrail project, as well
as a plugin to automatically load these tests into tempest. This is a set of
integration tests to be run against a live open-contrail cluster. Tempest has
testcases for Contrail API validation, scenarios, and other specific tests
useful in validating an open-contrail deployment.

See the tempest plugin docs for information on using it:
http://docs.openstack.org/developer/tempest/plugin.html#using-plugins

See the tempest docs for information on writing new tests etc:
http://docs.openstack.org/developer/tempest/

Quickstart
----------

To run tungstent-tempest, you must first have `Tempest`_ installed and configured
properly. Please reference Tempest's `Quickstart`_ guide to do so and for all
exact details. Follow all the steps outlined therein. 

   Here are some sample steps:

   $ git clone https://git.openstack.org/openstack/tempest
   $ cd tempest
   $ pip install -r requirements.txt
   $ pip install -r test-requirements.txt
   $ pip install tox
   $ pip install tempest

   Now below command should show you list of avaiable tempest test cases.

   $ ostestr -l

You can install all these including tempest in a virtual
environment. If virtual environment is not installed, then install it using
"sud apt-get install python-virtualenv". Afterward, proceed with the steps below.

#. Second, you need to install Patrole. This is done with pip after you check out
   the Patrole repo. Please reference `Patrole'`_'s `Quickstart`_ guide for further
   details.

    Here are some sample steps:

    $ git clone https://git.openstack.org/openstack/patrole
    $ cd patrole
    $ pip install -e .

   This can be done within a venv.

   Now below command should show you list of avaiable Patrole test cases.

   $ ostestr -l | grep patrole

#. Then you need to install tungsten-tempest. This is done with pip after you check out
   the tungsten-tempest repo::

   $ git clone https://git.openstack.org/tungsten/tungsten-tempest
   $ pip install -e tungsten_tempest/

   This can be done within a venv.

   Now below command should show you list of avaiable tungsten-tempest test cases.

   $ ostestr -l | grep tungsten
  
#. Next you must properly configure tempest, which is relatively
   straightforward. For details on configuring tempest refer to the
   :ref:`tempest-configuration`.

#. Next you must properly configure Patrole, which is relatively
   straightforward. For details on configuring Patrole refer to the
   :ref:`patrole-configuration`.

#. Next you must properly configure tungsten-fabric, which is relatively
   straightforward. For details on configuring tungsten-fabirc refer to the
   :ref:`tungsten-configuration`.

    After comfiguring tempmest.conf as per tempest and Patrole requirements, please
    make below changes too in the patrole section of tempest.conf

    enable_rbac must be true.
    test_custom_requirements must be true if you want to run tests against a
    ``custom_requirements_file`` which defines RBAC requirements.
    custom_requirements_file must be absolute path of file path of the YAML
    file that defines your RBAC requirements.

    For the details about these flags please refer ``patrole.conf.sample``_ file.

#. Make sure you have contrail endpoints in keystone catalog-list already like
   sdn-l-config-*. Otherwise configure below two keys under [sdn] section
   of tempest.conf.

     [sdn]
     endpoint_type = <public|admin|internal|publicURL|adminURL|internalURL>
     catalog_type = <Catalog type of the SDN service, default sdn-l-config>

#. Once the configuration is done you're now ready to run tungsten-fabric.
   This can be done using the `tempest_run`_ command. This can be done by running::

     $ tempest run --regex '^tungsten_tempest_plugin\.tests\.api'

   There is also the option to use testr directly, or any `testr`_ based test
   runner, like `ostestr`_. For example, from the workspace dir run::

     $ stestr --regex '(?!.*\[.*\bslow\b.*\])(^tungsten_tempest_plugin\.tests\.api))'

   will run the same set of tests as the default gate jobs.

   You can also run tungsten_tempest tests using `tox`_. To do so, ``cd`` into the
   **Tempest** directory and run::

     $ tox -eall-plugin -- tungstent_tempest_plugin.tests.api

#. Log information from tests is captured in ``tempest.log`` under the Tempest
   repository. Some Patrole debugging information is captured in that log
   related to expected test results and :ref:`role-overriding`.

   More detailed RBAC testing log output is emitted to ``tungsten_log``.
   To configure Patrole's logging, see the :ref:`tungsten-tempest-configuration` guide.

.. _Tempest: https://github.com/openstack/tempest
.. _Quickstart: https://docs.openstack.org/tempest/latest/overview.html#quickstart
.. _tempest_run: https://docs.openstack.org/tempest/latest/run.html
.. _testr: https://testrepository.readthedocs.org/en/latest/MANUAL.html
.. _ostestr: https://docs.openstack.org/os-testr/latest/
.. _tox: https://tox.readthedocs.io/en/latest/

RBAC Tests
----------

To change the role that the tungsten_tempest tests are being run as, edit
``rbac_test_role`` in the ``patrole`` section of tempest.conf: ::

    [patrole]
    rbac_test_role = member
    ...

.. note::

  The ``rbac_test_role`` is service-specific. member, for example,
  is an arbitrary role, but by convention is used to designate the default
  non-admin role in the system. Most tunsgtent_tempest tests should be run with
  **admin** and **member** roles. However, other services may use entirely
  different roles.

For more information about the member role and its nomenclature,
please see: `<https://ask.openstack.org/en/question/4759/member-vs-_member_/>`__.

