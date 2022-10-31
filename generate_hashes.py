#!/usr/bin/env python

from getpass import getpass
from hashlib import sha1
from random import choice

from passlib.hash import apr_md5_crypt, sha512_crypt


# Base64 alphabet
ALPHABET = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def mysql_hash(secret):
    '''Generate MySQL password hash'''

    return f'*{sha1(sha1(secret.encode("utf-8")).digest()).hexdigest().upper()}'


def htaccess_hash(secret, salt=None):
    '''Generate htaccess/htpasswd password hash'''

    # Sending it None for a salt will cause it to generate one.
    return f'{apr_md5_crypt.hash(secret=secret, salt=salt)}'


def linux_hash(secret, salt=None, rounds=5000):
    '''Generate Linux PAM password hash'''

    if salt is None:
        salt = ''.join(choice(ALPHABET) for i in range(16))

    return f'{sha512_crypt.hash(secret=secret, salt=salt, rounds=rounds)}'


def main():
    '''Main function'''

    secret = getpass('Please enter your desired password: ')

    print(f'htaccess {htaccess_hash(secret)}')
    print(f'linux {linux_hash(secret)}')
    print(f'mysql {mysql_hash(secret)}')


if __name__ == '__main__':
    main()


# Generate password hashes without knowing the users' passwords.

# https://en.wikipedia.org/wiki/Bcrypt
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
