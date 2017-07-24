import albuminfo, unittest, json, sys, urllib.error
from unittest.mock import Mock, MagicMock, patch
from http.client import HTTPResponse
from contextlib import contextmanager
from io import StringIO

@contextmanager
def capture_stdout(command, *args, **kwargs):
    """Utility function for capturing stdout output.

    This function was sourced from:
    http://schinckel.net/2013/04/15/capture-and-test-sys.stdout-sys.stderr-in-unittest.testcase/
    """

    out, sys.stdout = sys.stdout, StringIO()
    try:
        command(*args, **kwargs)
        sys.stdout.seek(0)
        yield sys.stdout.read()
    finally:
        sys.stdout = out

def create_album_text(photo_count):
    """Utility function for creating a JSON string to test with.

    Values of zero or less will just return a string containing '[]'.
    """
    format_string = ('{"albumId": 1,'
                    '"id": %d,'
                    '"title": "accusamus beatae ad facilis cum similique qui sunt",'
                    '"url": "http://placehold.it/600/92c952",'
                    '"thumbnailUrl": "http://placehold.it/150/92c952"}')
    output_string = '['
    for i in range(photo_count):
        output_string += (format_string % (i + 1))
        if i < (photo_count - 1):
            output_string += ','
    return (output_string + ']')

class TestAlbumInfoFunctions(unittest.TestCase):
    """Tests for all global functions within the albuminfo package
    """

    ### Tests for albuminfo.get_album_info ###
    @patch('albuminfo.urllib.request')
    def test_get_album_info(self, mock_urllib):
        """Testing that albuminfo.get_album_info calls urllib and reads the JSON correctly.
        """

        expected_url = albuminfo.album_url % 1
        expected_string = create_album_text(1)

        http_mock = MagicMock(spec=HTTPResponse)
        http_mock.read().decode.return_value = expected_string
        mock_urllib.urlopen.return_value = http_mock

        actual_json = albuminfo.get_album_info(1)
        self.assertEqual(actual_json, json.loads(expected_string))

        http_mock.read().decode.assert_called()
        mock_urllib.urlopen.assert_called_with(expected_url)

    @patch('albuminfo.urllib.request')
    @patch('albuminfo.sys')
    def test_get_album_info__error(self, mock_sys, mock_urllib):
        """Testing that the error handling for get_album_info works as expected.
        """

        mock_urllib.urlopen.side_effect = urllib.error.URLError("Test error")

        with capture_stdout(albuminfo.get_album_info, 1) as output:
            self.assertEqual(output, "There was a problem connecting to the photo album server!\n")

        mock_urllib.urlopen.assert_called()
        mock_sys.exit.assert_called()

    ### Tests for albuminfo.print_album_info ###
    def test_print_album_info__happy_path(self):
        """Ensures function prints to stdout in the expected format.
        """

        test_string = create_album_text(1)
        test_json = json.loads(test_string)
        expected_output = '[1] accusamus beatae ad facilis cum similique qui sunt\n'
        was_captured = False

        with capture_stdout(albuminfo.print_album_info, test_json) as output:
            was_captured = True
            self.assertEqual(expected_output, output)
        self.assertTrue(was_captured) # Sanity test, to make sure the test is actually comparing output

    def test_print_album_info__multiple_lines(self):
        """Tests for output of multiple album results.
        """

        test_string = create_album_text(2)
        test_json = json.loads(test_string)
        expected_output = ('[1] accusamus beatae ad facilis cum similique qui sunt\n'
                           '[2] accusamus beatae ad facilis cum similique qui sunt\n')

        with capture_stdout(albuminfo.print_album_info, test_json) as output:
            self.assertEqual(expected_output, output)

    def test_print_album_info__empty_list(self):
        """Tests for cases of empty album results.
        """
        test_json = []
        expected_output = ''

        with capture_stdout(albuminfo.print_album_info, test_json) as output:
            self.assertEqual(expected_output, output)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAlbumInfoFunctions, 'test'))
    return suite
