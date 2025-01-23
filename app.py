import requests
import pandas as pd
import os

from sqlalchemy import create_engine, text, exc
from sqlalchemy.orm import sessionmaker

from datetime import datetime

from telegram import Telegram

# API MKTZAP
URL = f'https://api.mktzap.com.br/company/638'
CLIENT_KEY = os.getenv('clientKey')

# DB
HOST = os.getenv('host')
PORT = os.getenv('port')
USER = os.getenv('user')
PASSWORD = os.getenv('password')

# Date format
STR_DATE_FORMAT = f'%Y-%m-%dT%H:%M:%S.%fZ'

def get_str_engine() -> str:
    return f'mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}'

def get_header() -> str:
    response = requests.get(URL + f'/token?clientKey={CLIENT_KEY}')
    accessToken = response.json()['accessToken']
    header = {
        'Authorization': f'Bearer {accessToken}'
    }
    return header

def get_history(created_from: str, created_to: str):
    header = get_header()
    response = requests.get(URL + f'/history?createdFrom={created_from}&createdTo={created_to}', headers=header)
    df = pd.DataFrame(response.json())
    if df.empty:
        return df
    df['last_message_at'] = pd.to_datetime(df['last_message_at'], format=STR_DATE_FORMAT)
    df['created_at'] = pd.to_datetime(df['last_message_at'], format=STR_DATE_FORMAT)
    df['updated_at'] = pd.to_datetime(df['last_message_at'], format=STR_DATE_FORMAT)
    df['closed_at'] = pd.to_datetime(df['last_message_at'], format=STR_DATE_FORMAT)
    df['first_message_at'] = pd.to_datetime(df['last_message_at'], format=STR_DATE_FORMAT)
    df['first_start_chat_at'] = pd.to_datetime(df['last_message_at'], format=STR_DATE_FORMAT)
    df['first_operator_answer_at'] = pd.to_datetime(df['last_message_at'], format=STR_DATE_FORMAT)
    df['latest_contact_chat_message_at'] = pd.to_datetime(df['last_message_at'], format=STR_DATE_FORMAT)
    df['latest_operator_answer_at'] = pd.to_datetime(df['last_message_at'], format=STR_DATE_FORMAT)
    return df

def upsert_history(created_from: str, created_to: str) -> pd.DataFrame:
    df = get_history(created_from, created_to)
    if not df.empty:
        try:
            engine = create_engine(get_str_engine())
            Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
            session = Session()
            
            query = f"""
                INSERT INTO dbmkt.history ({', '.join(df.columns)})
                SELECT * FROM dball.temp_history
                ON DUPLICATE KEY UPDATE
                    {', '.join([f'{col} = VALUES({col})' for col in df.columns])}
            """
            
            with session.connection() as conn:
                df.to_sql(name='temp_history', schema='dball', con=conn, if_exists='replace', index=False)
                conn.commit()
                conn.execute(text(query))
                conn.execute(text('DROP TABLE IF EXISTS dball.temp_history'))
                conn.commit()
        except exc.IntegrityError:
            Telegram('*dbmkt* | Foreign Key error in history')
        except Exception:
            Telegram('*dbmkt* | General error')
        
def get_messages(created_from: str, created_to: str):
    header = get_header()
    response = requests.get(URL + f'/message?createdFrom={created_from}&createdTo={created_to}', headers=header)
    df = pd.DataFrame(response.json())
    if df.empty:
        return df
    df['created_at'] = pd.to_datetime(df['created_at'], format=STR_DATE_FORMAT)
    df['updated_at'] = pd.to_datetime(df['updated_at'], format=STR_DATE_FORMAT)
    df['received_at'] = pd.to_datetime(df['received_at'], format=STR_DATE_FORMAT)
    return df

def upsert_messages(created_from: str, created_to: str):
    df = get_messages(created_from, created_to)
    if not df.empty:
        try:
            engine = create_engine(get_str_engine())
            Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
            session = Session()
            
            query = f"""
                INSERT INTO dbmkt.messages ({', '.join(df.columns)})
                SELECT * FROM dball.temp_messages
                ON DUPLICATE KEY UPDATE
                    {', '.join([f'{col} = VALUES({col})' for col in df.columns])}
            """
            
            with session.connection() as conn:
                df.to_sql(name='temp_messages', schema='dball', con=conn, if_exists='replace', index=False)
                conn.commit()
                conn.execute(text(query))
                conn.execute(text('DROP TABLE IF EXISTS dball.temp_messages'))
                conn.commit()
        except exc.IntegrityError:
            Telegram('*dbmkt* | Foreign Key error in messages')
        except Exception:
            Telegram('*dbmkt* | General error')

def main():
    
    end_date = datetime.now()
    number_of_days = 30
    while number_of_days > 0:
        create_from = (end_date - pd.Timedelta(days=number_of_days)).strftime('%Y-%m-%d')
        created_to = (end_date - pd.Timedelta(days=number_of_days-1)).strftime('%Y-%m-%d')
        print(f'⌛ Aguarde, Atualizando dia {create_from}', end='\r')
        
        upsert_history(create_from, created_to)
        upsert_messages(create_from, created_to)
        
        number_of_days -= 1
        
    print('✅ Atualização concluída!', end='\r')

if __name__ == '__main__':
    main()