PyKQML
======

PyKQML is an implementation of KQML messaging in Python. It consists of
the following classes:

::

    KQMLToken
    KQMLString
    KQMLQuotation
    KQMLList
    KQMLPerformative
    KQMLReader
    KQMLDispatcher
    KQMLModule

PyKQML can be installed as

::

    pip install pykqml

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

You can run the tests with the following command:

.. code:: python

   python -m unittest discover tests
