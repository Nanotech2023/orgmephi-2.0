class DefaultConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ORGMEPHI_API_PATH = 'example/api'
    JWT_ALGORITHM = 'RS256'
    ORGMEPHI_PUBLIC_KEY = 'id_rsa.pub'
    ORGMEPHI_CORS_ENABLED = True
