from passlib.context import CryptContext
from password_strength import PasswordPolicy


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
        if not self._passlib.verify(password, password_hash):
            raise WrongCredentials()


def get_password_policy():
    """
    Get current password policy

    Synonym to get_current_app().password_policy
    :return: Current password policy
    """
    from . import _orgmephi_current_app
    return _orgmephi_current_app.get().password_policy
