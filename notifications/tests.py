import logging
from unittest import TestCase
from unittest.mock import MagicMock, Mock

from user import User
from message import Message
from delivery import DeliverySystem, LOSS_CHANCE, READ_CHANCE
import names as names_module
import text as text_module


logging.disable(logging.CRITICAL)


def get_mocks_with_code():
    users = (
        MagicMock(),
        MagicMock(),
        MagicMock()
    )
    for index in range(len(users)):
        users[index].code = index
    return users


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

    def test_inbox_property(self):
        messages = get_mocks_with_code()
        user = User(name=self.name, code=self.code)
        for message in messages:
            user.receive_message(message=message)
        self.assertEqual(user.inbox, list(reversed(messages)))


class MessageTestCase(TestCase):

    body = 'This is the body of this message'
    code = 1

    def test_message_creation(self):
        message = Message(body=self.body, code=self.code)
        self.assertEqual(message.body, self.body)
        self.assertEqual(message.code, self.code)
        self.assertEqual(message._sent, set())
        self.assertEqual(message._received, set())
        self.assertEqual(message._read, set())
        self.assertEqual(message.users_sent, [])
        self.assertEqual(message.users_received, [])
        self.assertEqual(message.users_read, [])

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
        message._sent.add(user)
        self.assertEqual(len(message.users_received), 0)
        self.assertFalse(message.is_received(user=user))
        message.mark_as_received(user=user)
        self.assertEqual(len(message.users_received), 1)
        self.assertTrue(message.is_received(user=user))
        self.assertIn(user, message.users_received)

    def test_mark_unsent_message_as_received(self):
        message = Message(body=self.body, code=self.code)
        user = MagicMock()
        with self.assertRaises(ValueError):
            message.mark_as_received(user=user)

    def test_mark_not_yet_received_message_as_read(self):
        message = Message(body=self.body, code=self.code)
        user = MagicMock()
        with self.assertRaises(ValueError):
            message.mark_as_read(user=user)

    def test_mark_message_as_read(self):
        message = Message(body=self.body, code=self.code)
        user = MagicMock()
        message._sent.add(user)
        message._received.add(user)
        self.assertEqual(len(message.users_read), 0)
        self.assertFalse(message.is_read(user=user))
        message.mark_as_read(user=user)
        self.assertEqual(len(message.users_read), 1)
        self.assertTrue(message.is_read(user=user))
        self.assertIn(user, message.users_read)

    def test_repeated_user(self):
        message = Message(body=self.body, code=self.code)
        user = MagicMock()
        for _ in range(2):
            message.send(user=user)
            self.assertEqual(len(message.users_sent), 1)
            message.mark_as_received(user=user)
            self.assertEqual(len(message.users_received), 1)
            message.mark_as_read(user=user)
            self.assertEqual(len(message.users_read), 1)

    def test_users_properties(self):
        users = get_mocks_with_code()
        message = Message(body=self.body, code=self.code)
        for user in users:
            message.send(user=user)
            message.mark_as_received(user=user)
            message.mark_as_read(user=user)
        self.assertEqual(message.users_sent, list(users))
        self.assertEqual(message.users_received, list(users))
        self.assertEqual(message.users_read, list(users))


class NamesTestCase(TestCase):

    def test_random_name_generation(self):
        name = names_module.get_random_name()
        self.assertIsInstance(name, str)
        self.assertTrue(name.istitle())
        self.assertEqual(len(name.split()), 2)
        first_name, surname = name.split()
        self.assertIn(first_name, names_module.NAMES)
        self.assertIn(surname, names_module.SURNAMES)


class TextTestCase(TestCase):

    def test_random_text_generation(self):
        for num_words in (1, 10, 100):
            text = text_module.get_random_text(num_words=num_words)
            self.assertIsInstance(text, str)
            self.assertEqual(len(text.split()), num_words)
            self.assertTrue(text[0].isupper())
            self.assertTrue(text[1:].islower())
            self.assertTrue(text.endswith('.'))


class DeliverySystemTestCase(TestCase):

    loss_chance = 0
    read_chance = 1

    def setUp(self):
        self.ds = DeliverySystem(loss_chance=self.loss_chance, read_chance=self.read_chance)

    def test_delivery_system_creation(self):
        ds = DeliverySystem(loss_chance=self.loss_chance, read_chance=self.read_chance)
        self.assertEqual(ds._loss_chance, self.loss_chance)
        self.assertEqual(ds._read_chance, self.read_chance)
        self.assertIsInstance(ds._users, set)
        self.assertEqual(len(ds._users), 0)
        self.assertIsInstance(ds._messages, set)
        self.assertEqual(len(ds._messages), 0)

    def test_default_chances(self):
        ds = DeliverySystem()
        self.assertEqual(ds.loss_chance, LOSS_CHANCE)
        self.assertEqual(ds.read_chance, READ_CHANCE)

    def test_chances_type_validation(self):
        for arguments in (
            {'loss_chance': None},
            {'read_chance': None},
            {'loss_chance': 'wrong'},
            {'read_chance': 'wrong'},
        ):
            with self.assertRaises(TypeError):
                DeliverySystem(**arguments)

    def test_chances_value_validation(self):
        for arguments in (
            {'loss_chance': -1},
            {'read_chance': -1},
            {'loss_chance': 1.1},
            {'read_chance': 1.1},
            {'loss_chance': 2},
            {'read_chance': 2},
        ):
            with self.assertRaises(ValueError):
                DeliverySystem(**arguments)

    def test_register_user(self):
        username = 'John Doe'
        self.assertEqual(len(self.ds.users), 0)
        user = self.ds.register_user(name=username)
        self.assertEqual(len(self.ds.users), 1)
        self.assertEqual(self.ds._user_count, 1)
        self.assertIn(user, self.ds.users)
        self.assertEqual(user.name, username)
        self.assertEqual(user.code, 1)

    def test_create_message(self):
        message_body = 'This is a message.'
        self.assertEqual(len(self.ds.messages), 0)
        message = self.ds.create_message(body=message_body)
        self.assertEqual(len(self.ds.messages), 1)
        self.assertEqual(self.ds._message_count, 1)
        self.assertIn(message, self.ds.messages)
        self.assertEqual(message.body, message_body)
        self.assertEqual(message.code, 1)

    def test_get_user_and_message_code(self):
        control_series = list(range(1, 11))
        for code_generator in (self.ds._get_user_code, self.ds._get_message_code):
            series = list(code_generator() for _ in range(10))
            self.assertEqual(series, control_series)

    def test_users_property(self):
        users = (
            self.ds.register_user(),
            self.ds.register_user(),
            self.ds.register_user()
        )
        self.assertEqual(self.ds.users, list(users))

    def test_messages_property(self):
        messages = (
            self.ds.create_message(),
            self.ds.create_message(),
            self.ds.create_message()
        )
        self.assertEqual(self.ds.messages, list(messages))

    def test_is_registered_user(self):
        registered_user = self.ds.register_user(name='John Smith')
        self.assertTrue(self.ds.is_registered_user(user=registered_user))
        unregistered_user = User(name='Jane Doe', code=registered_user.code + 1)
        self.assertFalse(self.ds.is_registered_user(user=unregistered_user))

    def test_is_registered_message(self):
        registered_message = self.ds.create_message(body='This message is registered')
        self.assertTrue(self.ds.is_registered_message(message=registered_message))
        unregistered_message = Message(body='This message is not registered', code=registered_message.code + 1)
        self.assertFalse(self.ds.is_registered_message(message=unregistered_message))

    def test_send_message(self):
        user = self.ds.register_user(name='John Doe')
        message = self.ds.create_message(body='This is a message')
        for iterable in (message.users_sent, message.users_received, message.users_read, user.inbox):
            self.assertEqual(len(iterable), 0)
        self.ds.send_message(user=user, message=message)
        for iterable in (message.users_sent, message.users_received, message.users_read, user.inbox):
            self.assertEqual(len(iterable), 1)
        for iterable in (message.users_sent, message.users_received, message.users_read):
            self.assertIn(user, iterable)
        self.assertIn(message, user.inbox)

    def test_send_message_creation(self):
        user = self.ds.register_user(name='John Doe')
        self.assertEqual(len(self.ds.messages), 0)
        self.ds.send_message(user=user)
        self.assertEqual(len(self.ds.messages), 1)
        self.assertEqual(len(user.inbox), 1)

    def test_send_message_user_validation(self):
        user = User(name='John Doe', code=1)
        self.assertNotIn(user, self.ds.users)
        with self.assertRaises(ValueError):
            self.ds.send_message(user=user, body='This should raise and exception.')

    def test_send_message_validation(self):
        user = self.ds.register_user()
        message = Message(body='This message is not registered.', code=1)
        with self.assertRaises(ValueError):
            self.ds.send_message(user=user, message=message)

    def test_broadcast_message(self):
        users = (
            self.ds.register_user(),
            self.ds.register_user(),
            self.ds.register_user()
        )
        self.assertEqual(len(self.ds.users), len(users))
        message = self.ds.broadcast_message(body='This message will be sent to every user.')
        for user in users:
            self.assertIn(message, user.inbox)

    def test_broadcast_message_creation(self):
        user = self.ds.register_user()
        self.assertEqual(len(self.ds.messages), 0)
        self.ds.broadcast_message()
        self.assertEqual(len(self.ds.messages), 1)
        self.assertEqual(len(user.inbox), 1)

    def test_broadcast_message_validation(self):
        self.ds.register_user()
        message = Message(body='This message is not registered.', code=1)
        with self.assertRaises(ValueError):
            self.ds.broadcast_message(message=message)

    def test_loss_chance(self):
        users = [self.ds.register_user() for _ in range(1000)]
        self.assertEqual(len(self.ds.users), len(users))
        self.ds.loss_chance = 0
        message = self.ds.broadcast_message()
        self.assertEqual(len(message.users_sent), len(message.users_received))
        self.ds.loss_chance = 1
        message = self.ds.broadcast_message()
        self.assertEqual(len(message.users_sent), len(users))
        self.assertEqual(len(message.users_received), 0)

    def test_read_chance(self):
        users = [self.ds.register_user() for _ in range(1000)]
        self.assertEqual(len(self.ds.users), len(users))
        self.ds.loss_chance = 0
        self.ds.read_chance = 1
        message = self.ds.broadcast_message()
        self.assertEqual(len(message.users_sent), len(message.users_read))
        self.ds.read_chance = 0
        message = self.ds.broadcast_message()
        self.assertEqual(len(message.users_sent), len(users))
        self.assertEqual(len(message.users_received), len(users))
        self.assertEqual(len(message.users_read), 0)
