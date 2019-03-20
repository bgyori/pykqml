PyKQML
======

PyKQML is an implementation of KQML messaging in Python.

Installation
============

PyKQML can be installed as

::

    pip install pykqml

Note that releases of PyKQML up to 0.5 work in Python 2 only, whereas
releases above and including 1.0 work in Python 3 only.

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

You can create a new KQML messaging agent in the context of the TRIPS
system as

.. code:: python

    from kqml import KQMLModule

    class MyAgent(KQMLModule):
        name = "MyAgent" # This is the name of the agent to register with

        def __init__(self, **kwargs):
            # Call the parent class' constructor which sends a registration
            # message, setting the agent's name to be recognized by the
            # Facilitator.
            super(MyAgent, self).__init__(name=self.name, **kwargs)

            # Subscribe to REQUESTs of interest. The list will change
            # depending on the role of the agent
            for req in ('what-next', 'commit', 'evaluate'):
                self.subscribe_request(req)

            # Subscribe to TELLs of interest if needed. This list will change
            # depending on the role of the agent
            for tell in ('log-speechact', ):
                self.subscribe_tell(tell)

            # Now signal that the agent is ready to receive messages
            self.ready()

            # Finally, start the listener for incoming messages
            self.start()


        def receive_request(self, msg, content):
            # First, figure out what kind of request this is
            task = content.head().upper()
            # Here you typically decide what to do based on the
            # type of request.

            # Construct reply message's content
            reply_content = KQMLList()
            # Set whatever needs to be set in the reply content

            # Finally, wrap the content in a message and reply
            reply_msg = KQMLPerformative('reply')
            reply_msg.set('content', reply_content)
            self.reply(msg, reply_msg)

Testing
=======

You can run all tests by running `nosetests` in the top level folder.
