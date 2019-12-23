import logging
import random

from user import User
from message import Message
from names import get_random_name
from text import get_random_text
from decorators import sort_by_code

logger = logging.getLogger(__name__)

LOSS_CHANCE = 0.1
READ_CHANCE = 0.5


class DeliverySystem(object):
    """
    System of notifications that registers users and sends messages to them.
    """
    _users = None
    _messages = None
    _user_count = 0
    _message_count = 0

    def __init__(self, loss_chance=LOSS_CHANCE, read_chance=READ_CHANCE):
        """
        :param loss_chance: Chance (0-1) that a sent message will not be received.
        :type loss_chance: float
        :param read_chance: Chance (0-1) that a received message will be read.
        :type read_chance: float
        """
        self.loss_chance = loss_chance
        self.read_chance = read_chance
        self._users = set()
        self._messages = set()

    @property
    def loss_chance(self):
        """
        Getter method for the loss chance.
        :return: Loss chance.
        :rtype: float
        """
        return self._loss_chance

    @loss_chance.setter
    def loss_chance(self, loss_chance):
        """
        Setter method for the message loss chance that validates it before assignation.
        :param loss_chance: Value in the range [0-1] representing the chance that a sent message will not be received.
        :type loss_chance: float
        """
        if not isinstance(loss_chance, (int, float)):
            raise TypeError('Loss chance must be a number.')
        if loss_chance < 0 or loss_chance > 1:
            raise ValueError('Loss chance must be in range [0-1].')
        self._loss_chance = loss_chance

    @property
    def read_chance(self):
        return self._read_chance

    @read_chance.setter
    def read_chance(self, read_chance):
        """
        Setter method for the message read chance that validates it before assignation.
        :param read_chance: Value in the range [0-1] representing the chance that a received message will be read.
        :type read_chance: float
        """
        if not isinstance(read_chance, (int, float)):
            raise TypeError('Read chance must be a number.')
        if read_chance < 0 or read_chance > 1:
            raise ValueError('Read chance must ne in range [0-1].')
        self._read_chance = read_chance

    @property
    @sort_by_code()
    def messages(self):
        """
        Getter method to retrieve the created messages.
        :return: List of messages, ordered by their code.
        :rtype: list
        """
        return self._messages

    @property
    @sort_by_code()
    def users(self):
        """
        Getter method to retrieve the registered users.
        :return: List of users, ordered by their code.
        :rtype: list
        """
        return self._users

    def _get_user_code(self):
        """
        Increments the user counter and returns its value to be used as the code of a new user.
        :return: New user's code.
        :rtype: int
        """
        self._user_count += 1
        return self._user_count

    def _get_message_code(self):
        """
        Increments the message counter and returns its value to be used as the code of a new message.
        :return: New message's code.
        :rtype: int
        """
        self._message_count += 1
        return self._message_count

    def register_user(self, name=None):
        """
        Creates a new user with the specified name (or a random one if omitted) and registers it into the delivery
        system, assigning a unique numeric code.
        :param name: Full name of the user to be registered.
        :type name: str
        :return: The user that was created and registered.
        :rtype: User
        """
        user = User(name=name or get_random_name(), code=self._get_user_code())
        self._users.add(user)
        return user

    def is_registered_user(self, user):
        """
        Check if this user is registered.
        :param user: User whose register status is being checked
        :type user: User
        :return: Whether the user is registered or not.
        :rtype: bool
        """
        return user in self._users

    def create_message(self, body=None):
        """
        Creates a new message and adds it to the message list.
        :param body: Text to be used as the body of the message. A random text will be generated if this is not set.
        :type body: str
        :return: The new message.
        :rtype: Message
        """
        message = Message(body=body or get_random_text(num_words=10), code=self._get_message_code())
        self._messages.add(message)
        return message

    def is_registered_message(self, message):
        """
        Checks if this message is registered within the system.
        :param message: Message to check.
        :type message: Message
        :return: Whether the message is registered within the system or not.
        :rtype: bool
        """
        return message in self.messages

    def send_message(self, user, message=None, body=None):
        """
        Sends this message to this user, creating it first if the message is not specified, and marks it as received
        and read by this user if it passes the respective random rolls.
        :param user: The user to whom the message will be sent.
        :type user: User
        :param message: The message to send. If not specified, a new one will be created.
        :type message: Message
        :param body: The body of the message if a new one is created. IF not specified, a random text will be set.
        :type body: str
        :return: The message that was sent.
        :rtype: Message
        """
        if not self.is_registered_user(user=user):
            raise ValueError(f'User {user} is not registered.')
        message = message or self.create_message(body=body)
        if not self.is_registered_message(message=message):
            raise ValueError(f'Message "{message}" is not registered within the system.')
        message.send(user=user)
        if random.random() > self._loss_chance:
            user.receive_message(message=message)
            if random.random() < self._read_chance:
                user.read_message(message=message)
        return message

    def broadcast_message(self, message=None, body=None):
        """
        Sends this message to every registered user, creating it first if the message is not specified, and marks it
        as received and read by each user if they pass the respective random rolls.
        :param message: The message to send. If not specified, a new one will be created.
        :type message: Message
        :param body: The body of the message if a new one is created. IF not specified, a random text will be set.
        :type body: str
        :return: The message that was sent.
        :rtype: Message
        """
        message = message or self.create_message(body=body)
        for user in self.users:
            self.send_message(user=user, message=message)
        return message

    def show_statistics(self, display_func=logger.info):
        """
        Gathers and displays statistics about the current status of the delivery system: number of users registered,
        loss and read chance values, number of messages created and number of times every message has been sent,
        received and read.
        :param display_func: function used to display the statistics.
        :type display_func: function
        """
        display_func('-------------------------------')
        display_func('DELIVERY SYSTEM STATISTICS')
        display_func('-------------------------------')
        display_func(f'USERS: {self._user_count} unique users registered.')
        display_func('-------------------------------')
        display_func(f'LOSS CHANCE: chance that a message will be lost is set to {self._loss_chance}')
        display_func('-------------------------------')
        display_func(f'READ CHANCE: chance that a message will be read is set to {self._read_chance}')
        display_func('-------------------------------')
        display_func(f'MESSAGES: {self._message_count} unique messages created.')
        display_func('-------------------------------')
        for message in self.messages:
            times_sent, times_received, times_read  = message.get_statistics()
            display_func(f'Message {message.code}: {message.body}')
            display_func(f'Sent to {times_sent} users.')
            display_func(f'Received by {times_received} users.')
            display_func(f'Read by {times_read} users.')
            display_func('-------------------------------')
