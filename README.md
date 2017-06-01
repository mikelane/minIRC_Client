# minIRC_Client
#### Mike Lane
#### CS594 - Internetworking Protocols

---
## About 

This is a client implementation of the custom minIRC protocol.

## Installation

In order to run this client, you must install Python 3.6.0 or higher. I recommend using `pyenv` and `pyenv-virtualenv`
for this. For the test runs there are no non-standard libraries that must be installed. You will need to create a
file called `setings.ini`. Follow the formatting of `example_settings.ini`.

## Execution

The minIRC client can be executed one of two ways. First thing's first, though, you'll need to start up an instance of
the minIRC server or your client will attempt to connect and it will fail immediately. Refer to the minIRC_Server
package for more details.

Once the appropriate server is running and the Host IP and Port are in this client's `settings.ini` file, you can start
an example client test by executing this from the minIRC_Client root directory:

    $ python3 client_test.py <username>
   
This will connect to the server and run through a battery of tests including creating rooms, joining rooms, sending
messages, etc. The username `Admin` will create several rooms and then wait for a bit and then it will attempt to KICK
user `Mike`. 

To stop a client, simply hit ctrl-c. The KeyboardInterrupt exception will be caught and the client will close
gracefully.

To see how well the server handles several active users, run the following command:

    $ ./run-tests
    
The `run-tests` script starts the Admin user, waits a few seconds, then starts up 16 additional users, each of which
runs in the background (a screen process, so make sure that you have screen installed) and goes through the same 
non-admin test script as above. There is a lot of output and all of the features are tested. You can see the client-side 
output in the `logs/client.log` file.
