class Config:
    pass
    # General Config
    # ...

class DevelopmentConfig(Config):
    pass
    # Dev-specific config
    # ...

class TestingConfig(Config):
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/budgeting_app_test'  # Use a separate DB for testing
