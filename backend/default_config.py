from datetime import timedelta


class DefaultConfiguration:
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ORGMEPHI_API_PATH = 'api'
    JWT_ALGORITHM = 'RS256'
    ORGMEPHI_PUBLIC_KEY = 'id_rsa.pub'
    ORGMEPHI_PRIVATE_KEY = 'id_rsa'
    ORGMEPHI_TARGET_CLASSES_FILE = 'contest/tasks/target_classes.txt'
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
    ORGMEPHI_BIRTH_CERTIFICATE = 'Свидетельство о рождении в РФ'
    ORGMEPHI_AREA = 'both'
    ORGMEPHI_DAILY_THREAD_LIMIT = 5
    ORGMEPHI_DAILY_MESSAGE_LIMIT = 10
    ORGMEPHI_CONFIRM_EMAIL = False
    ORGMEPHI_ENABLE_PASSWORD_RECOVERY = False
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = None
    ORGMEPHI_MAIL_CONFIRM_KEY = b'\r\xa2\x96\xef\t\x8c\xfe\xa8\x83\xb5\x89\x10\xf4i\x9cL'
    ORGMEPHI_MAIL_CONFIRM_SALT = b'\xcd\x985a\xd5^:-\xcd\x01\xbdN\xac\x9e\xec\xd5'
    ORGMEPHI_MAIL_CONFIRM_EXPIRATION = timedelta(days=1)
    ORGMEPHI_MAIL_CONFIRM_SUBJECT = 'Подтверждение почтового адреса на портале олимпиад'
    ORGMEPHI_MAIL_RECOVER_SUBJECT = 'Восстановление доступа к порталу олимпиад'
    ORGMEPHI_PREREGISTER_PASSWORD_LENGTH = 8
    ORGMEPHI_MAX_FILE_SIZE = 1e7
    ORGMEPHI_CAPTCHA_ENABLE = False
    ORGMEPHI_CAPTCHA_LENGTH = 6
    ORGMEPHI_CAPTCHA_EXPIRATION = timedelta(minutes=5)
    RESPONSE_EXTRA_MINUTES = timedelta(seconds=300)
    ORGMEPHI_WKHTMLTOPDF_PATH = '/usr/bin/wkhtmltopdf'
    ORGMEPHI_MEDIA_KEY = 'ORGMEPHI'
    ORGMEPHI_MEDIA_ROOT_PATH = 'media'
    ORGMEPHI_MEDIA_STORES = {
        'PROFILE': 'profile',
        'RESPONSE': 'responses',
        'TASK': 'tasks',
        'NEWS': 'news',
        'CERTIFICATE': 'certificates'
    }
