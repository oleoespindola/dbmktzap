from datetime import timedelta
from requests import RequestException

from .models import History_model, CPF_model, Status_model, Departament_model, User_model

from datetime import datetime

import requests
import json

class Controller():
    def __init__(self, api_secrets, initial_date, schema):
        self.__api_secrets = api_secrets
        self.__initial_date = initial_date
        self.__schema = schema
    
    def get_header(self) -> json:
        try:
            # Get private KEY
            key = requests.get(self.__api_secrets.URLAPI + 'token?clientKey=' + self.__api_secrets.CLIENT_KEY)
            if key.status_code == 200:
                key = key.json() # Convert privat key to JSON
                return {'Authorization': 'Bearer ' + key['accessToken']} # Set private key in header
        except RequestException as e:
            print(f'Error in get_history function -> {e}')
        
    def get_history(self, initial_date_iso, final_date_iso) -> json:
        try:
            query = self.__api_secrets.URLAPI + 'historycontact?createdFrom=' + initial_date_iso + '&createdTo=' + final_date_iso
            history_data = requests.get(query, headers=self.get_header()) 
            history_data = history_data.json()
            return history_data
        except RequestException as e:
            print(f'Error in get_history function  -> {e}')
            
              
    def get_status(self) -> json:
        try:
            query = self.__api_secrets.URLAPI + 'status'
            status = requests.get(query, headers = self.get_header()) 
            status = status.json()
            return status
        except RequestException as e:
            print(f'Error in get_status function -> {e}')
            
    def get_users(self) -> json:
        try:
            query = self.__api_secrets.URLAPI + 'user'
            users = requests.get(query, headers=self.get_header()) 
            users = users.json()
            return users
        except RequestException as e:
            print(f'Error in get_users function -> {e}')
            
    def get_departaments(self) -> json:
        try:
            query = self.__api_secrets.URLAPI + 'sector'
            departaments = requests.get(query, headers=self.get_header()) 
            departaments = departaments.json()
            return departaments
        except RequestException as e:
            print(f'Error in get_departaments function -> {e}')       
   
    def upsert_departaments(self) -> None:
        try:
            departaments = self.get_departaments()
            for departament_json in departaments:
                departament_model = Departament_model()               
                departament_model.id = departament_json['id']           
                departament_model.company_id = departament_json['company_id']                
                departament_model.is_default = departament_json['is_default']            
                departament_model.name = departament_json['name']    #setor para sector     
                departament_model.created_at = datetime.strptime(departament_json['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')                 
                departament_model.updated_at = datetime.strptime(departament_json['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ')                
                departament_model.deleted_at = datetime.strptime(departament_json['deleted_at'], '%Y-%m-%dT%H:%M:%S.%fZ') if departament_json['deleted_at'] != None else None
                                
                self.__schema.merge(departament_model)
                
            departaments = None
            
        except Exception as e:
            print(f'Error in upsert_departaments function -> {str(e)}')
                   
    def upsert_status(self) ->  None:
        try:            
            status = self.get_status()
            for status_json in status:
                status_model = Status_model()
                status_model.id = status_json['id']
                status_model.company_id = status_json['company_id']
                status_model.should_close = status_json['should_close']
                status_model.poll_id = status_json['poll_id']
                status_model.should_require = status_json['should_require']
                status_model.classification = status_json['classification']
                status_model.flags = status_json['flags']
                status_model.use_in_bot = status_json['use_in_bot']
                status_model.name = status_json['name']
                status_model.color = status_json['color']
                status_model.created_at = datetime.strptime(status_json['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
                status_model.updated_at = datetime.strptime(status_json['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
                status_model.deleted_at = datetime.strptime(status_json['deleted_at'], '%Y-%m-%dT%H:%M:%S.%fZ') if status_json['deleted_at'] != None else None
                status_model.hsm_id = status_json['hsm_id']
                self.__schema.merge(status_model)
            status = None
        except Exception as e:
            print(f'Error in upsert_status function -> {str(e)}')

    def upsert_users(self):      
        try:      
            users = self.get_users()
            for user_json in users:
                user_model = User_model()
                user_model.id = user_json['id']
                user_model.name = user_json['name']
                user_model.display_name = user_json['display_name']
                user_model.email = user_json['email']
                user_model.created_at = datetime.strptime(user_json['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
                user_model.inactive_since = datetime.strptime(user_json['inactive_since'], '%Y-%m-%dT%H:%M:%S.%fZ') if user_json['inactive_since'] != None else None
                user_model.role = user_json['role']
                self.__schema.merge(user_model)
            users = None
        except Exception as e:
            print(f'Error in upsert_users function -> {str(e)}')
            
    def upsert_history(self):
        try:
            inicial_date = datetime.strptime(self.__initial_date, f'%Y-%m-%d').date()
            while inicial_date <= datetime.today().date():
                inicial_date_iso = inicial_date.isoformat()
                final_date_iso = (inicial_date + timedelta(days=1)).isoformat()
            
                historys = self.get_history(initial_date_iso=inicial_date_iso, final_date_iso=final_date_iso)
                for hisory_json in historys:
                    history_model = History_model()
                    history_model.id = hisory_json['id']                                     
                    history_model.messages_count = hisory_json['messages_count']
                    history_model.status_id = hisory_json['status_id']
                    history_model.company_id = hisory_json['company_id']
                    history_model.sector_id = hisory_json['sector_id']
                    history_model.channelable_id = hisory_json['channelable_id']
                    history_model.is_json = hisory_json['is_json']
                    history_model.last_user_id = hisory_json['last_user_id']
                    history_model.first_start_chat_at = datetime.fromtimestamp(hisory_json['first_start_chat_at']) if hisory_json['first_start_chat_at'] != None else None
                    history_model.first_operator_answer_at = datetime.fromtimestamp(hisory_json['first_operator_answer_at']) if hisory_json['first_operator_answer_at'] != None else None
                    history_model.latest_contact_chat_message_at = datetime.fromtimestamp(hisory_json['latest_contact_chat_message_at']) if hisory_json['latest_contact_chat_message_at'] != None else None 
                    history_model.latest_operator_answer_at = datetime.fromtimestamp(hisory_json['latest_operator_answer_at']) if hisory_json['latest_operator_answer_at'] != None else None
                    history_model.waiting_time_medium = hisory_json['waiting_time_medium']
                    history_model.waiting_time_count = hisory_json['waiting_time_count']
                    history_model.last_message_by_operator = hisory_json['last_message_by_operator']
                    history_model.closed_by_user_id = hisory_json['closed_by_user_id']
                    history_model.operator_assigned_id = hisory_json['operator_assigned_id']
                    history_model.sla_count = hisory_json['sla_count']
                    history_model.is_auto = hisory_json['is_auto']
                    history_model.nome = hisory_json['name']
                    history_model.last_message_at = datetime.strptime(hisory_json['last_message_at'], '%Y-%m-%dT%H:%M:%S.%fZ') if hisory_json['last_message_at'] != None else None
                    history_model.created_at = datetime.strptime(hisory_json['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ') if hisory_json['created_at'] != None else None
                    history_model.updated_at = datetime.strptime(hisory_json['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ') if hisory_json['updated_at'] != None else None
                    history_model.contact_id = hisory_json['contact_id']
                    history_model.channelable_type = hisory_json['channelable_type']
                    history_model.closed_at = datetime.strptime(hisory_json['closed_at'], '%Y-%m-%dT%H:%M:%S.%fZ') if hisory_json['closed_at'] != None else None
                    history_model.first_message_at = datetime.strptime(hisory_json['first_message_at'], '%Y-%m-%dT%H:%M:%S.%fZ') if hisory_json['first_message_at'] != None else None
                    history_model.protocol = hisory_json['protocol']
                    
                    self.__schema.merge(history_model)
                    print(f'⏳ Carregando atendimentos do dia {str(inicial_date)}: {history_model.id}...', end='\r')
                    
                    for contact in hisory_json['contacts']:
                        if contact['label'] == 'CPF':
        
        
                            cpf_model = CPF_model()
                            cpf_model.history_id = history_model.id
                            cpf_model.contact_id = contact['contacts']['contact_id']
                            cpf_model.company_id = contact['contacts']['company_id']
                            cpf_model.created_at = contact['contacts']['created_at']
                            cpf_model.updated_at = contact['contacts']['updated_at']
                            cpf_model.cpf = contact['contacts']['cpf']
                            self.__schema.merge(cpf_model)
                    
                inicial_date += timedelta(days=2)
                
        except Exception as e: 
            print(f'Error in upsert_history function: {str(e)}')