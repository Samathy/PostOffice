import unittest
import time

import postoffice


class tests(unittest.TestCase):

    def test_rate_limit(self):
        return

    def test_print(self):
        return

    def parse_string(self):
        return

    def write_file(self):
        filename = "192.168.0.0"+"_"+time.strftime("%d-%m-%Y")
        postoffice.write_file("hello", "192.168.0.0", time.strftime("%d-%m-%Y"))

        try:
            f = open(filename, "r")
        except FileNotFoundError:
            self.fail("Could not open file: "+ filename)

        assert f.readline() == "hello"

        os.remove(filename)

        return


    def test_connection(self):
        return


if __name__ == "__main__":
    unittest.main()
