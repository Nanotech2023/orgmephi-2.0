class DefaultConfiguration:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TASKS_API_PATH = '../contest_data/tasks_api.yaml'
