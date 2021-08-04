# See aggregate/default_config.py (for monolith), analytics/default_config.py, contest/default_config.py,
#   user/default_config.py (for microservice) for available options

SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite"
ORGMEPHI_JWT_SAMESITE = 'Strict'
# Set to limit origins for cors
# CORS_ORIGINS = ['origin1', ...]
