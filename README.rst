Tempest Integration of Tungsten Fabric (Contrail)
=================================================

This directory contains Tempest tests to cover the contrail project, as well
as a plugin to automatically load these tests into tempest. This is a set of
integration tests to be run against a live open-contrail cluster. Tempest has
test-cases for Contrail API validation, scenarios, and other specific tests
useful in validating an open-contrail deployment.

See the tempest plugin docs for information on using it:

[http://docs.openstack.org/developer/tempest/plugin.html#using-plugins](http://docs.openstack.org/developer/tempest/plugin.html#using-plugins)

See the tempest docs for information on writing new tests etc:

[http://docs.openstack.org/developer/tempest/](http://docs.openstack.org/developer/tempest/)


Quickstart
----------

#Tempest Installation

To run *tungsten-tempest*, you must first have `Tempest`_ installed and configured 
properly. Please reference Tempest's `Quickstart`_ guide to do so and for all
exact details. Follow all the steps outlined therein.

	Here are some sample steps:

	$ git clone https://git.openstack.org/openstack/tempest
	$ cd tempest
	$ pip install -r requirements.txt
	$ pip install -r test-requirements.txt
	$ pip install tox
	$ pip install tempest

Now below command should show you list of available tempest test cases.

	$ ostestr -l

You can install all these including tempest in a virtual
environment. If virtual environment is not installed, then install it using
"`sudo apt-get install python-virtualenv`". Afterward, proceed with the steps below.

#Patrole Installation

This is done with pip after you check out the [Patrole repo](https://github.com/openstack/patrole "Patrole repo"). Please reference `Patrole` [Quickstart](https://github.com/openstack/patrole/blob/master/README.rst "Quickstart") guide for further details.

    Here are some sample steps:

	$ git clone https://git.openstack.org/openstack/patrole
	$ cd patrole
	$ pip install -e .

NOTE: This can be done within a venv.
Now below command should show you list of available Patrole test cases.
	
	$ ostestr -l | grep patrole

#Tungsten-tempest Installation

This is done with pip after you check out the tungsten-tempest repo::

	$ git clone https://git.openstack.org/tungsten/tungsten-tempest
	$ pip install -e tungsten_tempest/

NOTE: This can be done within a venv.
Now below command should show you list of available tungsten-tempest test cases.

	$ ostestr -l | grep tungsten

#Configuration

You must properly configure tempest, which is relatively straightforward. For details on configuring tempest refer to the [tempest-configuration](https://github.com/openstack/tempest/blob/master/doc/source/configuration.rst "tempest-configuration").

Next you must properly configure Patrole, which is relatively straightforward. For details on configuring Patrole refer to the [patrole-configuration](https://github.com/openstack/patrole/blob/master/doc/source/configuration.rst "patrole-configuration")

Next you must properly configure tungsten-fabric, which is relatively straightforward too. For details on configuring tungsten-fabric refer to the :ref:`tungsten-configuration`.

After comfiguring tempmest.conf as per tempest and Patrole requirements, please make below changes too in the patrole section of tempest.conf:

    test_custom_requirements must be true if you want to run tests against a `custom_requirements_file` which defines RBAC requirements.

    custom_requirements_file must be absolute path of file path of the YAML file that defines your RBAC requirements.

For the details about these flags please refer [patrole.conf.sample](https://github.com/openstack/patrole/blob/master/etc/patrole.conf.sample "patrole.conf.sample") file.


**NOTE:** Make sure you have contrail endpoints in keystone catalog-list already like sdn-l-config-*. Otherwise configure below two keys under [sdn] section of tempest.conf.

     [sdn]
     endpoint_type = <public|admin|internal|publicURL|adminURL|internalURL>
     catalog_type = <Catalog type of the SDN service, default sdn-l-config>

#Running tungsten-tempest 

Once the configuration is done you're now ready to run tungsten-fabric.

The easiest way to run is using any testr utilities like below:

	$ ostestr run --regex tungsten_tempest_plugin.tests.api

This can also be done using the `tempest_run`_ command. This can be done by running::

	$ tempest run --regex '^tungsten_tempest_plugin\.tests\.api'

There is also the option to use testr directly, or any `testr`_ based test runner, like `ostestr`_. For example, from the work-space dir run::

	$ stestr --regex '(?!.*\[.*\bslow\b.*\])(^tungsten_tempest_plugin\.tests\.api))'

will run the same set of tests as the default gate jobs.

You can also run tungsten_tempest tests using `tox`_. To do so, ``cd`` into the **Tempest** directory and run::

	$ tox -eall-plugin -- tungstent_tempest_plugin.tests.api

#Log Information

Log information from tests is captured in ``tempest.log`` under the Tempest repository. Some Patrole debugging information is captured in that log related to expected test results and :ref:`role-overriding`.

More detailed RBAC testing log output is emitted to ``tungsten_log``.

To configure tungsten-tempest's logging, see the :ref:`tungsten-tempest-configuration` guide.


Tempest: [https://github.com/openstack/tempest](https://github.com/openstack/tempest)

Tempest Quickstart: [https://docs.openstack.org/tempest/latest/overview.html#quickstart](https://docs.openstack.org/tempest/latest/overview.html#quickstart)

tempest_run: [https://docs.openstack.org/tempest/latest/run.html](https://docs.openstack.org/tempest/latest/run.html)

testr: [https://testrepository.readthedocs.org/en/latest/MANUAL.html
](https://testrepository.readthedocs.org/en/latest/MANUAL.html)

ostestr: [https://docs.openstack.org/os-testr/latest/](https://docs.openstack.org/os-testr/latest/)

tox: [https://tox.readthedocs.io/en/latest/](https://tox.readthedocs.io/en/latest/)



#RBAC Tests
----------

To change the role that the tungsten_tempest tests are being run as, edit ``rbac_test_role`` in the ``patrole`` section of tempest.conf: ::

    [patrole]
    rbac_test_role = member
    ...

**NOTE**::

The ``rbac_test_role`` is service-specific. member, for example, is an arbitrary role, but by convention is used to designate the default non-admin role in the system. Most tunsgtent_tempest tests should be run with **admin** and **member** roles. However, other services may use entirely different roles.

For more information about the member role and its nomenclature,

please see: `<https://ask.openstack.org/en/question/4759/member-vs-_member_/>`__.

