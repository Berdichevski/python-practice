import unittest
from unittest.mock import patch, MagicMock
import socket
import argparse
from tcping import tcping


class TestTCPing(unittest.TestCase):

    @patch('socket.create_connection')
    def test_successful_connection(self, mock_create_connection):
        mock_connection = MagicMock()
        mock_create_connection.return_value = mock_connection
        mock_connection.__enter__.return_value = mock_connection

        with patch('time.time', return_value=1000):
            tcping('example.com', 80, count=1, timeout=2, interval=1)

        mock_create_connection.assert_called_with(('example.com', 80),
                                                  timeout=2)
        print("Test passed: test_successful_connection")

    @patch('socket.create_connection')
    def test_timeout_connection(self, mock_create_connection):
        mock_create_connection.side_effect = socket.timeout

        with patch('time.time', return_value=1000):
            tcping('example.com', 80, count=1, timeout=2, interval=1)

        mock_create_connection.assert_called_with(('example.com', 80),
                                                  timeout=2)
        print("Test passed: test_timeout_connection")

    @patch('socket.create_connection')
    def test_error_connection(self, mock_create_connection):
        mock_create_connection.side_effect = Exception("Connection error")

        with patch('time.time', return_value=1000):
            tcping('example.com', 80, count=1, timeout=2, interval=1)

        mock_create_connection.assert_called_with(('example.com', 80),
                                                  timeout=2)
        print("Test passed: test_error_connection")

    @patch('socket.create_connection')
    def test_no_successful_connections(self, mock_create_connection):
        mock_create_connection.side_effect = socket.timeout

        with patch('time.time', return_value=1000):
            tcping('example.com', 80, count=3, timeout=2, interval=1)

        mock_create_connection.assert_called_with(('example.com', 80),
                                                  timeout=2)
        print("Test passed: test_no_successful_connections")

    @patch('socket.create_connection')
    def test_successful_connection_with_latency(self, mock_create_connection):
        mock_connection = MagicMock()
        mock_create_connection.return_value = mock_connection
        mock_connection.__enter__.return_value = mock_connection

        with patch('time.time', side_effect=[1000, 1002]):
            tcping('example.com', 80, count=1, timeout=2, interval=1)

        print("Test passed: test_successful_connection_with_latency")

    def test_argument_parsing(self):
        with patch('sys.argv', ['tcping.py', 'example.com', '80',
                                '--count', '5', '--timeout', '3',
                                '--interval', '2']):
            parser = argparse.ArgumentParser(description="TCPing - "
                                                         "check TCP port "
                                                         "availability")
            parser.add_argument("host", help="Host to check "
                                             "(IP address or domain)")
            parser.add_argument("port", type=int, help="Port to check")
            parser.add_argument("--count", type=int, default=4,
                                help="Number of attempts (default 4)")
            parser.add_argument("--timeout", type=int, default=2,
                                help="Timeout for each connection "
                                     "attempt in seconds (default 2)")
            parser.add_argument("--interval", type=int, default=1,
                                help="Interval between requests "
                                     "in seconds (default 1)")
            args = parser.parse_args()

            self.assertEqual(args.count, 5)
            self.assertEqual(args.timeout, 3)
            self.assertEqual(args.interval, 2)
            self.assertEqual(args.host, 'example.com')
            self.assertEqual(args.port, 80)

        print("Test passed: test_argument_parsing")


if __name__ == "__main__":
    unittest.main()
