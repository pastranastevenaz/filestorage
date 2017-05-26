class Config(object):
    DEBUG=True
    TESTING=False
    DATABASE_NAME='papers'

class DevelopmentConfig(Config):
    SECRET_KEY='MySecretKey'

config = {
    'development': DevelopmentConfig,
    'testing': DevelopmentConfig,
    'production': DevelopmentConfig
}
