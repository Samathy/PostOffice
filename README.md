PostOffice
======================

A silly Python program which listens for connections
over TCP and prints whever bytes are received over
that connection.
Performs some rudimentory
rate-limiting.
Saves all printed bytes to files.

HOWTO
======================

Part of why this is an amusing project is that I'm not going to tell you how to
send bytes. Work it out! 
PostOffice, by default, accepts connections on port 7878.
Have a look at the postoffice_send.py file if you
have to, or have a look at the Ncat tool. You'll work it out.

Messages are printed in the format:

    ------------
    192.168.254.254
    d-m-Y-h-mAPM
    -----------
    Message Text auto-
    line wrapped by
    the printer.
    -----------


GPG HOWTO
----------------------
Since messages are not sent over an encrypted connection, PostOffice accepts
GPG encrypted messages in ASCII armoured format. Messages are decrypted and
then stored in plain text, so don't send your bank details, home address, or
list of heinous crimes to me please.

Rate Limiting
----------------------
Each IP address is limited to 20 connections per-day.

Message Size
---------------------
The buffer size is 1024 bytes. Messages above this size are truncated.


FAQ
====================

Are my messages saved to file?
    Yes.

Can I send images?
    Not at the moment. But I can probably work something into the parse_string() function
    to make this kinda thing available.

What happens if I send some garbage?
    If Python can't convert the bytes into a unicode string, it'll probably kill the process.

What printer are you using?
    Star TSP700II

