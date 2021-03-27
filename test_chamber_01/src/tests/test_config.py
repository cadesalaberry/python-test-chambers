# coding=utf-8

from config import Config
import unittest
import os


class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/')
        self.config.load_file(os.path.join(data_dir, 'config.base.json'))

    def test_should_work(self):
        self.assertEquals('me.local', self.config.get_key('domain'))
        self.assertEquals('mail.local', self.config.get_key('mail.host'))
        self.assertEquals('mysql_user', self.config.get_key('databases.mysql.user'))

    def test_should_return_None_when_keypath_does_not_exists(self):
        self.assertIsNone(self.config.get_key('fakekey'))
        self.assertIsNone(self.config.get_key('databases.mysql.user.fakekey'))
        self.assertIsNone(self.config.get_key('databases.mysql.options'))
        self.assertIsNone(self.config.get_key('databases.oracle.user'))
        self.assertIsNone(self.config.get_key('make.fakekey'))

    def test_should_return_None_when_key_in_keypath_is_not_a_dict(self):
        self.assertIsNone(self.config.get_key('databases.mysql.port.fakekey'))

    def test_key_could_be_empty(self):
        self.assertEquals('WARNING', self.config.get_key('loggers..level'))
        self.assertEquals('is_special', self.config.get_key('.special_key.'))
