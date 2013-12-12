# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
from haproxy.haproxy import create_parser
from haproxy.haproxy import parse_arguments

import unittest


class ArgumentParsingTest(unittest.TestCase):

    def setUp(self):
        self.parser = create_parser()
        self.default_arguments = [
            '-c', 'counter', 'haproxy/tests/files/dummy.log',
        ]

    def test_arg_parser_start_valid(self):
        """Check that 'start' argument is validated as a datetime object."""
        arguments = ['-s', '11/Dec/2013', ] + self.default_arguments
        data = parse_arguments(self.parser.parse_args(arguments))
        self.assertEqual(datetime(2013, 12, 11), data['start'])

        arguments = ['-s', '11/Dec/2013:13', ] + self.default_arguments
        data = parse_arguments(self.parser.parse_args(arguments))
        self.assertEqual(datetime(2013, 12, 11, hour=13),
                         data['start'])

        arguments = ['-s', '11/Dec/2013:14:15', ] + self.default_arguments
        data = parse_arguments(self.parser.parse_args(arguments))
        self.assertEqual(datetime(2013, 12, 11, hour=14, minute=15),
                         data['start'])

        arguments = ['-s', '11/Dec/2013:14:15:16', ] + self.default_arguments
        data = parse_arguments(self.parser.parse_args(arguments))
        self.assertEqual(datetime(2013, 12, 11, hour=14, minute=15, second=16),
                         data['start'])

    def test_arg_parser_start_invalid(self):
        """Check that if a 'start' argument is not valid an exception is
        raised.
        """
        arguments = ['-s', '/Dec/2013:14:15:16', ] + self.default_arguments
        with self.assertRaises(ValueError):
            parse_arguments(self.parser.parse_args(arguments))

    def test_arg_parser_delta_valid_deltas(self):
        """Check that deltas are correctly checked and processed as timedelta
        values.
        """
        arguments = ['-d', '45s', ] + self.default_arguments
        data = parse_arguments(self.parser.parse_args(arguments))
        self.assertEqual(timedelta(seconds=45), data['delta'])

        arguments = ['-d', '2m', ] + self.default_arguments
        data = parse_arguments(self.parser.parse_args(arguments))
        self.assertEqual(timedelta(minutes=2), data['delta'])

        arguments = ['-d', '13h', ] + self.default_arguments
        data = parse_arguments(self.parser.parse_args(arguments))
        self.assertEqual(timedelta(hours=13), data['delta'])

        arguments = ['-d', '1d', ] + self.default_arguments
        data = parse_arguments(self.parser.parse_args(arguments))
        self.assertEqual(timedelta(days=1), data['delta'])

    def test_arg_parser_delta_invalid(self):
        """Check that if an invalid delta argument is passed an exception is
        raised.
        """
        arguments = ['-d', 'invalid', ] + self.default_arguments
        with self.assertRaises(ValueError):
            parse_arguments(self.parser.parse_args(arguments))

    def test_arg_parser_filename_valid(self):
        """Check that any filename passed does exist before handling it
        further.
        """
        arguments = ['-c', 'counter', 'haproxy/tests/test_argparse.py', ]
        data = parse_arguments(self.parser.parse_args(arguments))
        self.assertEqual('haproxy/tests/test_argparse.py', data['filename'])

    def test_arg_parser_filename_invalid(self):
        """Check that if the filename passed does not exist an exception is
        raised.
        """
        arguments = ['-c', 'counter', 'non_existing.log', ]
        with self.assertRaises(ValueError):
            parse_arguments(self.parser.parse_args(arguments))

    def test_arg_parser_commands_valid(self):
        """Test that valid commands are correctly parsed"""
        arguments = ['-c', 'http_methods', 'haproxy/tests/files/dummy.log', ]
        data = parse_arguments(self.parser.parse_args(arguments))
        self.assertEqual(['http_methods', ], data['commands'])

    def test_arg_parser_commands_invalid(self):
        """Test that trying to input non existing commands raises an
        exception.
        """
        with self.assertRaises(ValueError):
            arguments = ['-c', 'non_existing_method',
                         'haproxy/tests/files/dummy.log', ]
            parse_arguments(self.parser.parse_args(arguments))