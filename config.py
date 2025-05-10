class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Kimbalama#32@localhost/autoshop_db'
    DEBUG = True
    CACHE_TYPE = "SimpleCache"
    
class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'


class ProductionConfig:
    pass