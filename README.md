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
