class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST='localhost'
    MYSQL_USER='root'
    MYSQL_PASSWORD=''
    MYSQL_DB='api_diana'
    MYSQL_CLIENT_FLAGS = [2] 
    
config={
    'development': DevelopmentConfig
}
    

    