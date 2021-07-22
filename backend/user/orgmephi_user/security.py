from passlib.context import CryptContext
from password_strength import PasswordPolicy

def init_security(app):
    app.config['ORGMEPHI_PASSLIB_CONTEXT'] = CryptContext(schemes=app.config['ORGMEPHI_PASSWORD_HASH'])
    app.config['ORGMEPHI_PASSWORD_POLICY'] = PasswordPolicy.from_names(
        length=app.config['ORGMEPHI_PASSWORD_LENGTH'],
        uppercase=app.config['ORGMEPHI_PASSWORD_UPPERCASE'],
        numbers=app.config['ORGMEPHI_PASSWORD_NUMBERS'],
        special=app.config['ORGMEPHI_PASSWORD_SPECIAL'],
        nonletters=app.config['ORGMEPHI_PASSWORD_NONLETTERS']
    )
