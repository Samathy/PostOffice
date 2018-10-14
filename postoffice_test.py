import unittest
import time
import os

import postoffice


class tests(unittest.TestCase):

    def test_rate_limit(self):
        
        #Test if the number of rates is over 20, we are limited.
        filename = "127.0.0.1.rate"
        f = open(filename, "w+")
        f.writelines("01/02/2002 5\n")
        f.writelines("30/44/1997 10\n")
        f.writelines(time.strftime("%d/%m/%Y")+" 20\n")
        f.close()

        assert postoffice.check_rate_limit("127.0.0.1") == False

        os.remove(filename)

        #Test if we don't have an entry yet for today, one is added.

        f = open(filename, "w+")
        f.writelines("01/02/2002 5\n")
        f.writelines("30/44/1997 10\n")
        f.close()

        assert postoffice.check_rate_limit("127.0.0.1") == True

        f = open(filename, "r+")
        for last in f: pass
        f.close()

        last_date = last.split(" ")[0]
        last_count = last.split(" ")[1]

        assert last_date == time.strftime("%d/%m/%Y")
        assert last_count.strip() == str(1)

        f.close()

        os.remove(filename)

        #Test if we already have an entry, it is incremented

        filename = "127.0.0.1.rate"
        f = open(filename, "w+")
        f.writelines("01/02/2002 5\n")
        f.writelines("30/44/1997 10\n")
        f.writelines(time.strftime("%d/%m/%Y")+" 10\n")
        f.close()

        assert postoffice.check_rate_limit("127.0.0.1") == True

        f = open(filename, "r+")
        for last in f: pass
        f.close()
        
        last_date = last.split(" ")[0]
        last_count = last.split(" ")[1]

        assert last_date == time.strftime("%d/%m/%Y")
        assert last_count.strip() == str(11)

        os.remove(filename)

        return

    def test_print(self):
        return

    def parse_string(self):
        return

    def test_write_file(self):
        filename = "192.168.0.0"+"_"+time.strftime("%d-%m-%Y-%H-%M")
        postoffice.write_file("hello", "192.168.0.0", time.strftime("%d-%m-%Y-%H-%M"))

        try:
            f = open(filename, "r")
        except FileNotFoundError:
            self.fail("Could not open file: "+ filename)

        for last in f: pass
        assert last == "hello"

        f.close()

        os.remove(filename)

        return


    def test_connection(self):
        return


if __name__ == "__main__":
    unittest.main()
