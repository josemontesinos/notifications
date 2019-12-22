import logging


logger = logging.getLogger(__name__)


class Message(object):
    """
    Message class. Each message has a text string as a body, a numeric code, a list of users to whom it has been sent,
    a list of users who received the message and a list of users that have opened and read it.
    """
    _body = ''
    _code = None
    _sent = None
    _received = None
    _read = None

    def __init__(self, body, code):
        """
        :param body: Text body of the message.
        :type body: str
        :param code: Numeric ID of the message.
        :type code: int
        """
        self.body = body
        self.code = code
        self._sent = set()
        self._received = set()
        self._read = set()
        logger.debug(f'Created new message with code {self.code} and body "{self.body}".')

    @property
    def body(self):
        """
        Getter method for the body of the message.
        :return: the text body of this message.
        :rtype: str
        """
        return self._body

    @body.setter
    def body(self, body):
        """
        Setter method for the message's body that validates it before assignation.
        :param body: New text body for this message.
        :type body: str
        """
        if not isinstance(body, str):
            raise TypeError('Message body must be string.')
        self._body = body

    @property
    def code(self):
        """
        Getter method for the message's code.
        :return: This message's code.
        :rtype: int
        """
        return self._code

    @code.setter
    def code(self, code):
        """
        Setter method for the message's code that validates it before assignation.
        :param code: New code for this message .
        :type code: str
        """
        if not isinstance(code, int):
            raise TypeError('Message code must be integer.')
        if code < 0:
            raise ValueError('Message code must be a positive integer.')
        self._code = code

    @property
    def users_sent(self):
        """
        Getter method for the set of users that this message was sent to.
        :return: Users to whom this message was sent.
        :rtype: set
        """
        return self._sent

    @property
    def users_received(self):
        """
        Getter method for the set of users that received this message.
        :return: Users who received this message.
        :rtype: set
        """
        return self._received

    @property
    def users_read(self):
        """
        Getter method for the set of users that read this message.
        :return: Users who read this message.
        :rtype: set
        """
        return self._read

    def send(self, user):
        """
        Sets the message as sent to this user.
        :param user: User object to send the message to.
        :type user: User
        """
        self._sent.add(user)
        logger.debug(f'Message "{self}" sent to user {user}.')

    def is_sent(self, user):
        """
        Check if the message was sent to this user.
        :param user: User object to check sent status.
        :type user: User
        :return: True if the message was sent to the user, False otherwise.
        :rtype: bool
        """
        return user in self._sent

    def mark_as_received(self, user):
        """
        Sets the message as received by this user.
        :param user: User object that received the message.
        :type user: User
        """
        self._received.add(user)
        logger.debug(f'Message "{self}" marked as received by user {user}.')

    def is_received(self, user):
        """
        Check if the message was received by this user.
        :param user: User object to check received status.
        :type user: User
        :return: True if the user received the message, False otherwise.
        :rtype: bool
        """
        return user in self._received

    def mark_as_read(self, user):
        """
        Sets the message as opened and read by this user.
        :param user: User object that read the message
        :type user: User
        """
        self._read.add(user)
        logger.debug(f'Message "{self}" marked as read by user {user}.')

    def is_read(self, user):
        """
        Check if the message was opened and read by this user.
        :param user: User object to check read status.
        :type user: User
        :return: True if the user read the message, False otherwise.
        :rtype: bool
        """
        return user in self._read

    def __repr__(self):
        """
        Representation method.
        :return: The body of this message.
        :rtype: str
        """
        return self._body
