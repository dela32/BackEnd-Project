class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Kimbalama#32@localhost/autoshop_db'
    DEBUG = True
    
class TestingConfig:
    pass

class ProductionConfig:
    pass