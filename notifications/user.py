import logging

logger = logging.getLogger(__name__)


class User(object):
    """
    User class. Each user has a name, a numeric code and an inbox with messages they have received.
    """
    _name = None
    _code = None
    _inbox = None

    def __init__(self, name, code):
        """
        :param name: Name of this user.
        :type name: str
        :param code: Code of this user.
        :type code: int
        """
        self.name = name
        self.code = code
        self._inbox = []

    @property
    def name(self):
        """
        Getter method for the user's name.
        :return: This user's name.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Setter method for the user's name that validates it before assignation.
        :param name: New name for this user.
        :type name: str
        """
        if not isinstance(name, str):
            raise TypeError('User name must be string.')
        self._name = name

    @property
    def code(self):
        """
        Getter method for the user's code.
        :return: This user's code.
        :rtype: int
        """
        return self._code

    @code.setter
    def code(self, code):
        """
        Setter method for the user's code that validates it before assignation.
        :param code: New code for this user .
        :type code: str
        """
        if not isinstance(code, int):
            raise TypeError('User code must be integer.')
        if code < 0:
            raise ValueError('User code must be a positive integer.')
        self._code = code

    @property
    def inbox(self):
        """
        Getter method for the user's inbox.
        :return: This user's inbox.
        :rtype: list
        """
        return self._inbox

    def receive_message(self, message):
        """
        Receive a message sent to this user and store it in the inbox.
        :param message: Message object received by this user.
        :type: Message
        """
        if message not in self._inbox:
            self._inbox.append(message)
            message.mark_as_received(user=self)
            logger.debug(f'User {self} received a new message: "{message}"')
        else:
            logger.warning(f'User {self} received a repeated message: "{message}".')

    def read_message(self, message):
        """
        Mark a message as read by this user.
        :param message: The message to mark as read.
        :type message: Message
        """
        try:
            inbox_message = next(msg for msg in self._inbox if msg == message)
            inbox_message.mark_as_read(user=self)
        except StopIteration:
            raise ValueError(f'User {self} cannot read this message because it is not in their inbox.')

    def get_read_messages(self):
        """
        Retrieve all read messages from the user's inbox.
        :return: All messages this user has read.
        :rtype: list
        """
        read_messages = list(filter(lambda x: x.is_read(user=self), self._inbox))
        return read_messages

    def get_unread_messages(self):
        """
        Retrieve all unread messages from the user's inbox.
        :return: All messages this user has not read yet.
        :rtype: list
        """
        unread_messages = list(filter(lambda x: not x.is_read(user=self), self._inbox))
        return unread_messages

    def __repr__(self):
        """
        Representation method.
        :return: This user's name.
        :rtype: str
        """
        return self.name
