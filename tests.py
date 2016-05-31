import unittest
import json
import tempfile
import functools
import logging
import sys
from unittest import mock
from random import choice, randint
from string import ascii_letters, digits

from webtest import TestApp

from pll import wsgi_app


app = TestApp(wsgi_app)


###############################################################################
# Logging ######################################################################
###############################################################################

class _LogTracer(object):
    def __init__(self):
        self._last_frame = None

    def tracer(self, frame, event, *extras):
        if event == 'return':
            self._last_frame = frame

    @property
    def last_frame(self):
        return self._last_frame


def log_locals_on_exit(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        log_tracer = _LogTracer()
        sys.setprofile(log_tracer.tracer)
        try:
            result = fn(*args, **kwargs)
        finally:
            sys.setprofile(None)
        frame = log_tracer.last_frame

        _locals = {}
        for k, v in frame.f_locals.items():
            _locals[k] = repr(v)
        logging.info(_locals)
        return result
    return inner


def generic_log(fn):
    fn = log_locals_on_exit(fn)
    #fn = log_entry(fn)
    return fn


###############################################################################
# Utility ######################################################################
###############################################################################

@generic_log
def string_generator(max_length):
    length = randint(1, max_length)
    return ''.join([choice(ascii_letters + digits) for _ in range(length)])


class RandomEnvelope(list):
    def __init__(self, max_keys, max_lines, max_key_size, max_value_size):
        super().__init__()
        self.key_count = randint(1, max_keys)
        self.line_count = randint(1, max_lines)
        self.key_size = randint(1, max_key_size)
        self.value_size = randint(1, max_value_size)

    def key_generator(self):
        return [string_generator(self.key_size) for _ in range(self.key_count)]

    def line_generator(self, keys):
        return dict((key, string_generator(self.value_size)) for key in keys)

    def letter_generator(self):
        keys = self.key_generator()
        return [self.line_generator(keys) for _ in range(self.line_count)]

    def envelope_generator(self):
        stamp = string_generator(self.value_size)
        return [stamp, self.letter_generator()]


###############################################################################
# Api Testing ##################################################################
###############################################################################

class TestLetterPosts(unittest.TestCase):
    def setUp(self):
        self.letter = RandomEnvelope(100, 100, 10, 25).letter_generator()

    @generic_log
    @mock.patch('pll.pile.add')
    def test_post_200(self, mock_pile_add):
        mock_pile_add.return_value = json.dumps(self.letter)
        response = app.post_json('/letter', self.letter)
        assert response.json == json.dumps(self.letter)

    def test_post_409(self):
        letter = ["stamp1", [{'column1': 'row1'}, {'column1': 'row2'}]]
        response = app.post_json('/letter', letter, status=409)
        self.assertEqual(response.status_int, 409)


###############################################################################
# Model Testing# ###############################################################
###############################################################################

class TestPile(unittest.TestCase):
    def setUp(self):
        self.db = tempfile.mktemp()

