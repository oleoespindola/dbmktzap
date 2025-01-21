from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

class Schema:
    def __init__(self, secrets):
        engine = create_engine(secrets.SECRETS)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.__session = SessionLocal()
            
    def merge(self, data) -> None:
        try:
            self.__session.merge(data)
            self.__session.commit()
            
        except exc.SQLAlchemyError as e:
            print(f'Error in merge function (Class Schema) -> {e}')
            