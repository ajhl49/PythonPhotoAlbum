#!/bin/python

import albuminfo, unittest, json, sys
from unittest.mock import Mock, MagicMock, patch
from http.client import HTTPResponse
from contextlib import contextmanager
from io import StringIO

@contextmanager
def capture_stdout(command, *args, **kwargs):
    """Utility method for capturing stdout output.

    This method was sourced from:
    http://schinckel.net/2013/04/15/capture-and-test-sys.stdout-sys.stderr-in-unittest.testcase/
    """

    out, sys.stdout = sys.stdout, StringIO()
    try:
        command(*args, **kwargs)
        sys.stdout.seek(0)
        yield sys.stdout.read()
    finally:
        sys.stdout = out

class TestAlbumInfoFunctions(unittest.TestCase):
    """Tests for all global functions within the albuminfo package
    """

    @patch('albuminfo.urllib.request')
    def test_get_album_info(self, mock_urllib):
        expected_url = albuminfo.album_url % 1
        expected_string = ('[{"albumId": 1,'
                           '"id": 1,'
                           '"title": "accusamus beatae ad facilis cum similique qui sunt",'
                           '"url": "http://placehold.it/600/92c952",'
                           '"thumbnailUrl": "http://placehold.it/150/92c952"}]')

        http_mock = MagicMock(spec=HTTPResponse)
        http_mock.read().decode.return_value = expected_string
        mock_urllib.urlopen().__enter__.return_value = http_mock

        actual_json = albuminfo.get_album_info(1)
        self.assertEqual(actual_json, json.loads(expected_string))

        http_mock.read().decode.assert_called()
        mock_urllib.urlopen.assert_called_with(expected_url)

    def test_print_album_info__happy_path(self):
        test_string = ('[{"albumId": 1,'
                       '"id": 1,'
                       '"title": "accusamus beatae ad facilis cum similique qui sunt",'
                       '"url": "http://placehold.it/600/92c952",'
                       '"thumbnailUrl": "http://placehold.it/150/92c952"}]')
        test_json = json.loads(test_string)
        expected_output = "[1] accusamus beatae ad facilis cum similique qui sunt\n"

        with capture_stdout(albuminfo.print_album_info, test_json) as output:
            self.assertEqual(expected_output, output)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAlbumInfoFunctions, 'test'))
    return suite
