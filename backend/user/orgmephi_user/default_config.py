class DefaultConfiguration:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ORGMEPHI_USERNAME_MAXLEN = 320
    ORGMEPHI_PHONE_MAXLEN = 12
    ORGMEPHI_UNIVERSITY_MAXLEN = 50
    ORGMEPHI_UNIVERSITY_FILE = 'universities.txt'
    ORGMEPHI_COUNTRY_MAXLEN = 50
    ORGMEPHI_COUNTRY_FILE = 'countries.txt'
    ORGMEPHI_REGION_MAXLEN = 50
    ORGMEPHI_CITY_MAXLEN = 50