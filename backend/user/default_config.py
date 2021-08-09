from datetime import timedelta


class DefaultConfiguration:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ORGMEPHI_API_PATH = 'api'
    ORGMEPHI_UNIVERSITY_FILE = 'user/universities.txt'
    ORGMEPHI_COUNTRY_FILE = 'user/countries.txt'
    ORGMEPHI_PASSWORD_HASH = 'pbkdf2_sha256'
    ORGMEPHI_PASSWORD_LENGTH = 8
    ORGMEPHI_PASSWORD_UPPERCASE = 1
    ORGMEPHI_PASSWORD_NUMBERS = 1
    ORGMEPHI_PASSWORD_SPECIAL = 1
    ORGMEPHI_PASSWORD_NONLETTERS = 0
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)
    ORGMEPHI_REMEMBER_ME_TIME = timedelta(days=30)
    JWT_ALGORITHM = 'RS256'
    ORGMEPHI_PUBLIC_KEY = 'id_rsa.pub'
    ORGMEPHI_PRIVATE_KEY = 'id_rsa'
    # Values: 'Strict', 'Lax', 'None' ('None' is a string, not a NoneType)
    # Warning: in most browsers 'None' only works over https
    ORGMEPHI_JWT_SAMESITE = 'Strict'
    ORGMEPHI_CORS_ENABLED = True