import logging
from unittest import TestCase
from unittest.mock import MagicMock, Mock

from notifications import User, Message


logging.disable(logging.CRITICAL)


class UserTestCase(TestCase):

    name = 'José Montesinos Navarro'
    code = 1

    def test_user_creation(self):
        user = User(name=self.name, code=self.code)
        self.assertEqual(user.name, self.name)
        self.assertEqual(user.code, self.code)
        self.assertEqual(user.inbox, [])

    def test_user_representation(self):
        user = User(name=self.name, code=self.code)
        for func in repr, str:
            self.assertEqual(func(user), user.name)

    def test_user_name_type_validation(self):
        wrong_name = 1234
        with self.assertRaises(TypeError):
            User(name=wrong_name, code=self.code)

    def test_user_code_type_validation(self):
        wrong_code = '1'
        with self.assertRaises(TypeError):
            User(name=self.name, code=wrong_code)

    def test_user_code_value_validation(self):
        wrong_code = -1
        with self.assertRaises(ValueError):
            User(name=self.name, code=wrong_code)

    def test_recieve_message(self):
        user = User(name=self.name, code=self.code)
        message = MagicMock()
        self.assertEqual(len(user.inbox), 0)
        user.receive_message(message=message)
        self.assertEqual(len(user.inbox), 1)
        message.mark_as_received.assert_called_with(user=user)

    def test_recieve_repeated_message(self):
        user = User(name=self.name, code=self.code)
        message = MagicMock()
        user.receive_message(message=message)
        user.receive_message(message=message)
        self.assertEqual(len(user.inbox), 1)
        message.mark_as_received.assert_called_once_with(user=user)

    def test_read_message(self):
        user = User(name=self.name, code=self.code)
        message = MagicMock()
        user.receive_message(message=message)
        message.mark_as_read.assert_not_called()
        user.read_message(message=message)
        message.mark_as_read.assert_called_with(user=user)

    def test_read_unreceived_message(self):
        user = User(name=self.name, code=self.code)
        message = MagicMock()
        with self.assertRaises(ValueError):
            user.read_message(message=message)
        message.mark_as_read.assert_not_called()

    def test_get_read_and_unread_messages(self):
        user = User(name=self.name, code=self.code)
        message = MagicMock()
        message.is_read = Mock(return_value=False)
        user.receive_message(message=message)
        self.assertEqual(len(user.get_read_messages()), 0)
        self.assertEqual(len(user.get_unread_messages()), 1)
        message.is_read = Mock(return_value=True)
        self.assertEqual(len(user.get_read_messages()), 1)
        self.assertEqual(len(user.get_unread_messages()), 0)


class MessageTestCase(TestCase):

    body = 'This is the body of this message'
    code = 1

    def test_message_creation(self):
        message = Message(body=self.body, code=self.code)
        self.assertEqual(message.body, self.body)
        self.assertEqual(message.code, self.code)
        self.assertEqual(message.users_sent, set())
        self.assertEqual(message.users_received, set())
        self.assertEqual(message.users_read, set())

    def test_message_representation(self):
        message = Message(body=self.body, code=self.code)
        for func in repr, str:
            self.assertEqual(func(message), message.body)

    def test_message_body_type_validation(self):
        wrong_body = 1234
        with self.assertRaises(TypeError):
            Message(body=wrong_body, code=self.code)

    def test_message_code_type_validation(self):
        wrong_code = '1'
        with self.assertRaises(TypeError):
            User(name=self.body, code=wrong_code)

    def test_message_code_value_validation(self):
        wrong_code = -1
        with self.assertRaises(ValueError):
            User(name=self.body, code=wrong_code)

    def test_send_message(self):
        message = Message(body=self.body, code=self.code)
        user = MagicMock()
        self.assertEqual(len(message.users_sent), 0)
        self.assertFalse(message.is_sent(user=user))
        message.send(user=user)
        self.assertEqual(len(message.users_sent), 1)
        self.assertTrue(message.is_sent(user=user))
        self.assertIn(user, message.users_sent)

    def test_mark_message_as_received(self):
        message = Message(body=self.body, code=self.code)
        user = MagicMock()
        self.assertEqual(len(message.users_received), 0)
        self.assertFalse(message.is_received(user=user))
        message.mark_as_received(user=user)
        self.assertEqual(len(message.users_received), 1)
        self.assertTrue(message.is_received(user=user))
        self.assertIn(user, message.users_received)

    def test_mark_message_as_read(self):
        message = Message(body=self.body, code=self.code)
        user = MagicMock()
        self.assertEqual(len(message.users_read), 0)
        self.assertFalse(message.is_read(user=user))
        message.mark_as_read(user=user)
        self.assertEqual(len(message.users_read), 1)
        self.assertTrue(message.is_read(user=user))
        self.assertIn(user, message.users_read)




