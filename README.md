# Notification Simulator

## Specifications
The objective of this exercise is to develop a simulator for delivering notifications to users. The simulator will allow 
you to define an environment with several users to whom notifications can be delivered, and each of these notifications 
will have a series of statistics related to the messages sent, received and open.

* **User** registration:
    * Each user will have a name, which will be used for its representation. 
    * A user will be registered in a unique list and assigned a code.
    * Each user will have an inbox with the messages they have received.
    * Each user can check their inbox and mark a message as read.

* Create and send **messages**:
    * The messages will have a text string as a body, which will be used for its representation.
    * The messages will have a list of users to whom the message has been sent.
    * The messages will have a list of users who have received the message.
    * Messages will have a list of users who have opened the message.
    * Given a message, it will be possible to obtain the statistics of message opening and receiving.
    
* The **message delivery system** shall be separate from users and messages and shall:
    * Maintain a list of registered users, assigning their codes.
    * Publish a message to all registered users, assigning a unique code to eachmessage in the process, and adding each 
    message to the user's inbox.
    * Simulate a message loss ratio, that is, that there is a probability that amessage will not be received by a user.
    
## Help

To simulate the loss ratio we can do something similar to the following code:

```python
# simulate loss ratio
loss = random.random() < self.loss_ratio
if not loss:
...
```

## Evaluation

In addition to the necessary class definitions, a simulation (i.e. an example run) of sending messages to 1000 users 
will have to be implemented and message statistics (message number, message reception and message opening) displayed.

In this exercise, the programming style, good practices and resources used (types, libraries, etc.) will be evaluated. 
The exercise should be performed using only Python, without the need for any other tools, databases or messaging queue 
managers...

## Solution

The proposed solution implements a delivery system, with both a message loss and a message read chance, that allows
users to be registered and messages to be published to one user or broadcasted to all of them. If no user name of 
message body is specified, random ones will be generated.

This delivery system assigns a unique and incremental numeric code to every registered user, as well as to any created 
message. These codes keep an independent sequence to each other. 

In order to develop this solution only native Python 3 packages and resources have been used, so there is no need to 
install or use any third-party dependency. 

**IMPORTANT**: this solution has been developed making use of features present only on the latest versions of Python,
such as f-string or other latest native package tools, so only **Python 3.7+** is supported.

### Statistics

The delivery system also provides a method to display its current statistics. This method accepts as a parameter the 
function used to display this information. By default this is the *info()* function of the Python native *logging* 
package. 

The statistics displayed by this method include:

* Number of registered users.
* Message loss chance.
* Message read chance.
* Number of created messages.
* And for every created message:
    * Message code and body.
    * Number of users to whom this message has been sent.
    * Number of users who have received this message.
    * Number of users who have opened and read this message.
    
#### Example
````text
DELIVERY SYSTEM STATISTICS
-------------------------------
USERS: 1000 unique users registered.
-------------------------------
LOSS CHANCE: chance that a message will be lost is set to 0.1
-------------------------------
READ CHANCE: chance that a message will be read is set to 0.5
-------------------------------
MESSAGES: 1 unique messages created.
-------------------------------
Message 1: Neque, pellentesque vestibulum vestibulum diam commodo non euismod maximus nulla.
Sent to 1000 users.
Received by 891 users.
Read by 453 users.
````

### Simulation

The developed solution provides a running file, named "main.py" that runs a simulation where a number of users are
registered and an amount of messages are broadcasted to all of them. When all messages have been sent and 
processed by the users, system statistics are displayed to either the console or a log file.

This simulation is highly customizable, as different command line parameters allow to change its behaviour and adapt it
to different needs. All this parameters are optional and will take default values if they are omitted.
These default values will run a simulation where 1000 users will be registered and 10 different messages will be 
created and broadcasted to all of them, displaying statistics to the console once all messages have been processed.

#### Usage

````text
usage: Notification Simulator [-h] [-u NUMUSERS] [-m NUMMESSAGES] [-lc [0-1]]
                              [-rc [0-1]] [-o {console,logfile}] [-f LOGFILE]
                              [-lv {debug,info,error,warning,critical}]
                              [-ls LOGSIZE] [-lb LOGBACKUP]

Simulator for delivering notifications to users.

optional arguments:
  -h, --help            show this help message and exit
  -u NUMUSERS, --numusers NUMUSERS
                        Number of users to register. Defaults to 1000.
  -m NUMMESSAGES, --nummessages NUMMESSAGES
                        Number of messages to send. Defaults to 10.
  -lc [0-1], --losschance [0-1]
                        Message loss chance. Defaults to 0.1.
  -rc [0-1], --readchance [0-1]
                        Message read chance. Defaults to 0.5.
  -o {console,logfile}, --output {console,logfile}
                        Set program output. Defaults to "console".
  -f LOGFILE, --logfile LOGFILE
                        Path to log file. Defaults to "notifications.log".
  -lv {debug,info,error,warning,critical}, --loglevel {debug,info,error,warning,critical}
                        Logging level. Defaults to "info".
  -ls LOGSIZE, --logsize LOGSIZE
                        Max log size in bytes before rotation. Defaults to
                        10000000.
  -lb LOGBACKUP, --logbackup LOGBACKUP
                        Max number of backup logs. Defaults to 1.
````

#### Example

````bash
python main.py -u 1000 -m 10 -o console -lc 0.1 -rc 0.5 -lv info
````

Thanks to the set default values, the above command is equal to:

 ````bash
python main.py
````

### Tests

A thorough set of unit tests has been developed and can be checked on the "tests.py" file. These tests are implemented 
over the native Python *unittest* package and can be run with the following command:

````bash
python -m unittest tests.py
````

### Contact

* **Author**: José Salvador Montesinos Navarro
* **Email**: jmontesinos@hotmail.es 

 
