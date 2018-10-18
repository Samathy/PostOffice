import unittest
import time
import os
import gnupg
from parameterized import parameterized
from unittest import mock
import postoffice


class tests(unittest.TestCase):

    @parameterized.expand([
        (["01/02/2002 5\n", "30/44/1997 10\n", time.strftime("%d/%m/%Y")+" 20\n"], False, time.strftime("%d/%m/%Y"), str(20)), 
        (["01/02/2002 5\n", "30/44/1997 10\n"], True, time.strftime("%d/%m/%Y"), str(1)),
        (["01/02/2002 5\n", "30/44/1997 10\n", time.strftime("%d/%m/%Y")+" 10\n"], True, time.strftime("%d/%m/%Y"), str(11))
    ])
    def test_rate_limit(self, writable_lines, expected, lastline_date, lastline_value):
        '''First, test that if the number of hits for today is above 20, we return False.
           Second, test that if there is no rate for today, we we add it and return True.
           Last, test that if there is an existing rate for today, we increment it and return True.'''
        filename = "127.0.0.1.rate"
        rate_limit_file = open(filename, "w+")

        for line in writable_lines:
            rate_limit_file.writelines(line)

        rate_limit_file.close()

        assert postoffice.check_rate_limit("127.0.0.1") is expected

        rate_limit_file = open(filename, "r+")
        last = ""
        for last in rate_limit_file:
            pass
        rate_limit_file.close()

        last_date = last.split(" ")[0]
        last_count = last.split(" ")[1]

        assert last_date == lastline_date
        assert last_count.strip() == lastline_value

        os.remove(filename)

        return

    @mock.patch("postoffice.CUPS_CONNECTION", autospec=True)
    def test_print(self, cups_connection):

        filename = "testfile.txt"

        with open(filename, "w+") as testfile:
            testfile.write("Hello. This is a test string")

        postoffice.print_file(filename)

        cups_connection.getDefault.assert_called_once()

        cups_connection.printFile.assert_called_with(cups_connection.getDefault.return_value, filename, filename, {})

        os.remove(filename)

        return

    def test_write_file(self):
        filename = "logs/"+"192.168.0.0"+"_"+time.strftime("%d-%m-%Y-%H-%M%p")
        postoffice.write_file("hello", "192.168.0.0", time.strftime("%d-%m-%Y-%H-%M%p"))

        try:
            write_file = open(filename, "r")
        except FileNotFoundError:
            self.fail("Could not open file: "+ filename)

        lines = list()
        for line in write_file:
            lines.append(line)
        assert lines[-2] == "hello\n"

        write_file.close()

        os.remove(filename)

        return

    def test_parse_string(self):
        gpg = gnupg.GPG()

        message = "hello"

        encrypted_message = gpg.encrypt(message, "samathy@sbarratt.co.uk")
        decrypted_message = postoffice.parse_string(str(encrypted_message))

        assert str(decrypted_message) == "hello"


    def test_connection(self):
        return


if __name__ == "__main__":
    unittest.main()
