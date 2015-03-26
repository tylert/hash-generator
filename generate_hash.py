#!/usr/bin/env python

# Generate password hashes without knowing the users' passwords.

# Tested with Python 3.4.0, 2.7.6, 2.6.6 on Ubuntu 14.04, Centos 6.5 and
# Mac OS X 10.10

# http://unix.stackexchange.com/questions/44883/encrypt-a-password-the-same-way-mysql-does
# http://stackoverflow.com/questions/13052047/python-crypt-in-osx
# http://stackoverflow.com/questions/5293959/creating-a-salt-in-python

# Assuming the plaintext passphrase 'hello' for john.smith...

# USE mysql;
# CREATE USER 'john.smith'@'%' IDENTIFIED BY PASSWORD '*6B4F89A54E2D27ECD7E8DA05B4AB8FD9D1D8B119';
# GRANT SELECT,INSERT,UPDATE,DELETE ON *.* TO 'john.smith'@'%';
# FLUSH PRIVILEGES;

# ... or, if updating an existing user's password hash directly...

# SET PASSWORD FOR 'john.smith'@'%' = '*6B4F89A54E2D27ECD7E8DA05B4AB8FD9D1D8B119';

# >>> linux_hash('hello', salt='T8XqbUhf')
# $6$T8XqbUhf$yrcwfZxBJABzTIE4QemGI62CO3P37EAZ0lhnoLVbz4hY.MpyoDyKHiPTmvCBU.GU.sepo7zCBKH3z2NoQQlq1.

# >>> apr_md5_crypt.encrypt('hello', salt='QtSwlvv9')
# '$apr1$QtSwlvv9$kiaFPes02tFnJML/Fumum.'


import getpass
from hashlib import sha1
import random
# pip install passlib
from passlib.hash import (apr_md5_crypt, sha512_crypt)


ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ./'


def mysql_hash(plaintext):
    hashed = sha1(sha1(plaintext).digest()).hexdigest().upper()
    return '*{0}'.format(hashed)


def htaccess_hash(plaintext, salt=None):
    hashed = apr_md5_crypt.encrypt(plaintext, salt=salt)
    return '{0}'.format(hashed)


def linux_hash(plaintext, salt=None):
    if salt is None:
        salt = ''.join(random.choice(ALPHABET) for i in range(8))

    hashed = sha512_crypt.encrypt(plaintext, salt=salt,
        rounds=5000, implicit_rounds=True)
    return '{0}'.format(hashed)


if __name__ == '__main__':

    plaintext = getpass.getpass('Please enter your desired password: ')

    print(mysql_hash(plaintext))
    print(htaccess_hash(plaintext))
    print(linux_hash(plaintext))
