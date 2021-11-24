from passlib.context import CryptContext
from password_strength import PasswordPolicy


_legacy_hash_name = 'org-legacy'


# noinspection InsecureHash
def _legacy_hash(password, salt):
    from hashlib import md5
    pwd_hash = md5(password.encode('utf-8')).hexdigest()
    salt_hash = md5(salt.encode('utf-8')).hexdigest()
    result_hash = md5((pwd_hash + salt_hash).encode('utf-8')).hexdigest()
    return result_hash


def _legacy_verify(password, hashed_password):
    salt = hashed_password.split('$')[2]
    orig_hash = hashed_password.split('$')[3]
    real_hash = _legacy_hash(password, salt)
    return orig_hash == real_hash


class OrgMephiPassword:
    """
    Password manager
    """
    def __init__(self, hash_schemes: list[str], length: int, uppercase: int, numbers: int, special: int,
                 nonletters: int):
        """
        Create password manager object
        :param hash_schemes: list of supported hash schemas (see passlib)
        :param length: minimal password length
        :param uppercase: minimal amount of uppercase characters in a password
        :param numbers: minimal amount of number symbols in a password
        :param special: minimal amount of special symbols in a password
        :param nonletters: minimal amount of non-letter symbols in a password
        """
        self._passlib = CryptContext(schemes=hash_schemes)
        self._pass_policy = PasswordPolicy.from_names(
            length=length,
            uppercase=uppercase,
            numbers=numbers,
            special=special,
            nonletters=nonletters
        )

    def hash_password(self, password, check: bool = True):
        """
        Calculate hash sum of the password (see passlib)
        :param password: password to hash
        :param check: whether password should also be checked according to password strength policy
        :return: hash of the password
        """
        from .errors import WeakPassword
        if check:
            pass_check = self._pass_policy.test(password)
            if pass_check:
                raise WeakPassword(pass_check)
        return self._passlib.hash(password)

    def validate_password(self, password, password_hash):
        """
        Check whether a password matches a provided hash
        :param password: password
        :param password_hash: hash of a password
        """
        from .errors import WrongCredentials
        if password_hash.split('$')[1] == _legacy_hash_name:
            if _legacy_verify(password, password_hash):
                return
        else:
            if self._passlib.verify(password, password_hash):
                return
        raise WrongCredentials()


def get_password_policy():
    """
    Get current password policy

    Synonym to get_current_app().password_policy
    :return: Current password policy
    """
    from . import get_current_app
    return get_current_app().password_policy
