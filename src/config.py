import os

class DIGITAL: 
    
    URLAPI = os.getenv('DIGITAL_URLAPI')
    
    CLIENT_KEY = os.getenv('DIGITAL_CLIENT_KEY')
    
class SOL:
    
    URLAPI = os.getenv('SOL_URLAPI')
    
    CLIENT_KEY = os.getenv('SOL_CLIENT_KEY')
    
    
class CP2: 
    
    SECRETS = os.getenv('DB_SECRETS')