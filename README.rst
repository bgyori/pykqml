PyKQML
======

PyKQML is an implementation of KQML messaging in Python.

Installation
============

PyKQML can be installed as

::

    pip install pykqml

Note that releases of PyKQML up to 0.5 work in Python 2 only, whereas
releases after 0.5 work in Python 3 only.

To install for Python 2, use:

::

    pip install pykqml==0.5

To install for Python 3 (or force an upgrade to a compatible version),
use

::

    pip install "pykqml>0.5"

Usage
=====

PyKQML implements the following KQML classes, which allow constructing
and manipulating KQML messages programmatically:

::

    KQMLToken
    KQMLString
    KQMLQuotation
    KQMLList
    KQMLPerformative
    KQMLReader
    KQMLDispatcher
    KQMLModule

You can import KQML classes as, for instance,

.. code:: python

    from kqml import KQMLList

You can create a new KQML messaging agent as

.. code:: python

    from kqml import KQMLModule

    class MyAgent(KQMLModule):
        def __init__(self, argv):
            # Initialize the agent
            super(MyAgent, self).__init__(argv)
            self.ready()
            super(MyAgent, self).start()

        def receive_request(self, msg, content):
            # Handle request and construct a reply_msg
            # ...
            self.reply(msg, reply_msg)

Testing
=======

You can run all tests by running `nosetests` in the top level folder.
