from datetime import timedelta


class DefaultConfiguration:
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ORGMEPHI_API_PATH = 'api'
    JWT_ALGORITHM = 'RS256'
    ORGMEPHI_PUBLIC_KEY = 'id_rsa.pub'
    ORGMEPHI_PRIVATE_KEY = 'id_rsa'
    ORGMEPHI_UNIVERSITY_FILE = 'user/universities.txt'
    ORGMEPHI_COUNTRY_FILE = 'user/countries.txt'
    ORGMEPHI_REGION_FILE = 'user/regions.txt'
    ORGMEPHI_CITY_FILE = 'user/cities.txt'
    ORGMEPHI_PASSWORD_HASH = 'pbkdf2_sha256'
    ORGMEPHI_PASSWORD_LENGTH = 8
    ORGMEPHI_PASSWORD_UPPERCASE = 1
    ORGMEPHI_PASSWORD_NUMBERS = 1
    ORGMEPHI_PASSWORD_SPECIAL = 1
    ORGMEPHI_PASSWORD_NONLETTERS = 0
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)
    ORGMEPHI_REMEMBER_ME_TIME = timedelta(days=30)
    ORGMEPHI_CORS_ENABLED = True
    ORGMEPHI_NATIVE_COUNTRY = 'Россия'
    ORGMEPHI_NATIVE_DOCUMENT = 'Паспорт гражданина РФ'
    ORGMEPHI_INTERNATIONAL_DOCUMENT = 'Заграничный паспорт гражданина РФ'
    ORGMEPHI_FOREIGN_DOCUMENT = 'Паспорт гражданина иностранного государства'
    ORGMEPHI_AREA = 'both'
