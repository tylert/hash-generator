#!/usr/bin/env python

import getpass
from hashlib import sha1
import random

from passlib.hash import apr_md5_crypt, sha512_crypt


# Base64 alphabet
ALPHABET = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def mysql_hash(secret):
    '''Generate MySQL password hash.'''

    hashed = sha1(sha1(secret.encode('utf-8')).digest()).hexdigest().upper()
    return '*{}'.format(hashed)


def htaccess_hash(secret, salt=None):
    '''Generate htaccess/htpasswd password hash.'''

    # Sending it None for a salt will cause it to generate one.
    hashed = apr_md5_crypt.encrypt(secret=secret, salt=salt)
    return '{}'.format(hashed)


def linux_hash(secret, salt=None):
    '''Generate Linux password hash.'''

    if salt is None:
        salt = ''.join(random.choice(ALPHABET) for i in range(16))

    hashed = sha512_crypt.encrypt(secret=secret, salt=salt,
                                  rounds=5000)
    return '{}'.format(hashed)


def main():
    '''Main function.'''

    secret = getpass.getpass('Please enter your desired password: ')

    print('mysql {}'.format(mysql_hash(secret)))
    print('htaccess {}'.format(htaccess_hash(secret)))
    print('linux {}'.format(linux_hash(secret)))


if __name__ == '__main__':
    main()


# Generate password hashes without knowing the users' passwords.

# Tested with Python 3.6.3, 2.7.14, 2.7.10 on macOS 10.12
# Tested with Python 3.5.3, 3.4.2, 3.4.0, 2.7.9, 2.7.6, 2.6.6 on Debian 9.x,
# Debian 8.x, Ubuntu 14.04, Mac OS X 10.10, CentOS 6.6, CentOS 6.5

# http://unix.stackexchange.com/questions/44883/encrypt-a-password-the-same-way-mysql-does
# http://stackoverflow.com/questions/13052047/python-crypt-in-osx
# http://stackoverflow.com/questions/5293959/creating-a-salt-in-python

# mysql_config_editor set --login-path=foo --host=host --user=user --password
# mysql --login-path=foo

# Assuming the plaintext passphrase 'hello' for john.smith...

# USE mysql;
# CREATE USER 'john.smith'@'%' IDENTIFIED BY PASSWORD \
#   '*6B4F89A54E2D27ECD7E8DA05B4AB8FD9D1D8B119';
# GRANT SELECT,INSERT,UPDATE,DELETE ON *.* TO 'john.smith'@'%';
# FLUSH PRIVILEGES;

# ... or, if updating an existing user's password hash directly...

# USE mysql;
# SET PASSWORD FOR 'john.smith'@'%' =
# '*6B4F89A54E2D27ECD7E8DA05B4AB8FD9D1D8B119';

# >>> mysql_hash(secret='hello')
# *6B4F89A54E2D27ECD7E8DA05B4AB8FD9D1D8B119

# >>> htaccess_hash(secret='hello', salt='QtSwlvv9')
# '$apr1$QtSwlvv9$kiaFPes02tFnJML/Fumum.'

# >>> linux_hash(secret='hello', salt='T8XqbUhf')
# $6$T8XqbUhf$yrcwfZxBJABzTIE4QemGI62CO3P37EAZ0lhnoLVbz4hY.MpyoDyKHiPTmvCBU.GU.sepo7zCBKH3z2NoQQlq1.
