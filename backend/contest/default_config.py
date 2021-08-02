class DefaultConfiguration:
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ORGMEPHI_CONTEST_API_PATH = 'api'
    JWT_ALGORITHM = 'RS256'
    ORGMEPHI_PUBLIC_KEY = 'id_rsa.pub'
