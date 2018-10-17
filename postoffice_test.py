import unittest
import time
import os
import gnupg

import postoffice


class tests(unittest.TestCase):

    def test_rate_limit(self):
        #Test irate_limit_file the number orate_limit_file rates is over 20, we are limited.
        filename = "127.0.0.1.rate"
        rate_limit_file = open(filename, "w+")
        rate_limit_file.writelines("01/02/2002 5\n")
        rate_limit_file.writelines("30/44/1997 10\n")
        rate_limit_file.writelines(time.strftime("%d/%m/%Y")+" 20\n")
        rate_limit_file.close()

        assert postoffice.check_rate_limit("127.0.0.1") is False

        os.remove(filename)

        #Test irate_limit_file we don't have an entry yet for today, one is added.

        rate_limit_file = open(filename, "w+")
        rate_limit_file.writelines("01/02/2002 5\n")
        rate_limit_file.writelines("30/44/1997 10\n")
        rate_limit_file.close()

        assert postoffice.check_rate_limit("127.0.0.1") is True

        rate_limit_file = open(filename, "r+")
        last = ""
        for last in rate_limit_file:
            pass
        rate_limit_file.close()

        last_date = last.split(" ")[0]
        last_count = last.split(" ")[1]

        assert last_date == time.strftime("%d/%m/%Y")
        assert last_count.strip() == str(1)

        rate_limit_file.close()

        os.remove(filename)

        #Test irate_limit_file we already have an entry, it is incremented

        filename = "127.0.0.1.rate"
        rate_limit_file = open(filename, "w+")
        rate_limit_file.writelines("01/02/2002 5\n")
        rate_limit_file.writelines("30/44/1997 10\n")
        rate_limit_file.writelines(time.strftime("%d/%m/%Y")+" 10\n")
        rate_limit_file.close()

        assert postoffice.check_rate_limit("127.0.0.1") is True

        rate_limit_file = open(filename, "r+")
        last = ""
        for last in rate_limit_file:
            pass
        rate_limit_file.close()
        last_date = last.split(" ")[0]
        last_count = last.split(" ")[1]

        assert last_date == time.strftime("%d/%m/%Y")
        assert last_count.strip() == str(11)

        os.remove(filename)

        return

    def test_print(self):
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
