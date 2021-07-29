from passlib.context import CryptContext
from password_strength import PasswordPolicy


class OrgMephiPassword:
    def __init__(self, hash_schemes: list[str], length: int, uppercase: int, numbers: int, special: int,
                 nonletters: int):
        self._passlib = CryptContext(schemes=hash_schemes)
        self._pass_policy = PasswordPolicy.from_names(
            length=length,
            uppercase=uppercase,
            numbers=numbers,
            special=special,
            nonletters=nonletters
        )

    def hash_password(self, password, check: bool = True):
        from .errors import WeakPassword
        if check:
            pass_check = self._pass_policy.test(password)
            if pass_check:
                raise WeakPassword(pass_check)
        return self._passlib.hash(password)

    def validate_password(self, password, password_hash):
        from .errors import WrongCredentials
        if not self._passlib.verify(password, password_hash):
            raise WrongCredentials()


def get_password_policy():
    from . import _orgmephi_current_app
    return _orgmephi_current_app.get().password_policy
