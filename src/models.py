from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User_model(Base):
    __tablename__ = 'mktzap_users'

    # Primary Key
    id = Column(Integer, name = 'user_id', primary_key = True)
    
    name = Column(String, name = 'user_name')
    display_name = Column(String, name = 'user_display_name')
    email = Column(String, name = 'user_email')
    created_at = Column(String, name = 'user_created_at')
    inactive_since = Column(String, name = 'user_inactive_since')
    role = Column(String, name = 'user_role')
    
class History_model(Base):
    __tablename__ = 'mktzap_history'

    # Primary Key    
    id = Column(Integer, name = 'id', primary_key = True)

    messages_count = Column(Integer, name = 'messages_count')
    status_id = Column(Integer, name = 'status_id')
    company_id = Column(Integer, name = 'company_id')
    sector_id = Column(Integer, name = 'sector_id')
    channelable_id = Column(Integer, name = 'channelable_id')
    is_json = Column(Integer, name = 'is_json')
    last_user_id = Column(Integer, name = 'last_user_id')
    first_start_chat_at = Column(Integer, name = 'first_start_chat_at')
    first_operator_answer_at = Column(Integer, name = 'first_operator_answer_at')
    latest_contact_chat_message_at = Column(Integer, name = 'latest_contact_chat_message_at')
    latest_operator_answer_at = Column(Integer, name = 'latest_operator_answer_at')
    waiting_time_medium = Column(Integer, name = 'waiting_time_medium')
    waiting_time_count = Column(Integer, name = 'waiting_time_count')
    last_message_by_operator = Column(Integer, name = 'last_message_by_operator')
    closed_by_user_id = Column(Integer, name = 'closed_by_user_id')
    operator_assigned_id = Column(Integer, name = 'operator_assigned_id')
    sla_count = Column(Integer, name = 'sla_count')
    is_auto = Column(Integer, name = 'is_auto')
    nome = Column(String, name = 'nome')
    last_message_at = Column(String, name = 'last_message_at')
    created_at = Column(String, name = 'created_at')
    updated_at = Column(String, name = 'updated_at')
    contact_id = Column(String, name = 'contact_id')
    channelable_type = Column(String, name = 'channelable_type')
    closed_at = Column(String, name = 'closed_at')
    first_message_at = Column(String, name = 'first_message_at')
    protocol = Column(String, name = 'protocol')
    
class CPF_model(Base):
    __tablename__ = 'mktzap_history_cpf'

    # Primary Key    
    id = Column(Integer, name = 'protocol', primary_key = True)
    
    history_id = Column('mktzap_atendimentos_id', Integer, ForeignKey(History_model.id))
    
    contact_id = Column(String, name = 'contact_id')
    company_id = Column(String, name = 'company_id')
    created_at = Column(String, name = 'created_at')
    updated_at = Column(String, name = 'updated_at')
    
    cpf = Column(Integer, name = 'cpf')
    
class Hsm_model(Base):
    __tablename__ = 'mktzap_hsm'

    # Primary Key
    id = Column(Integer, name = 'hsm_id', primary_key = True)
    
    use_in_poll = Column(Integer, name = 'hsm_use_in_poll')
    
    template = Column (String, name = 'hsm_template')
    header_template = Column (String, name = 'hsm_header_template')
    company_id = Column (String, name = 'hsm_company_id')
    name = Column (String, name = 'hsm_name')
    namespace = Column (String, name = 'hsm_namespace')
    element_name = Column (String, name = 'hsm_element_name')
    policy = Column (String, name = 'hsm_policy')
    language = Column (String, name = 'hsm_language')
    created_at = Column (String, name = 'hsm_created_at')
    updated_at = Column (String, name = 'hsm_updated_at')
    deleted_at = Column (String, name = 'hsm_deleted_at')
    header_type = Column (String, name = 'hsm_header_type')
    
class Departament_model(Base):
    __tablename__ = 'mktzap_departaments'

    # Primary Key
    id = Column(Integer, name = 'sector_id', primary_key = True)

    company_id = Column(Integer, name = 'sector_company_id')
    is_default = Column(Integer, name = 'sector_is_default')

    name = Column(String, name = 'sector_name')
    created_at = Column(String, name = 'sector_created_at')
    updated_at = Column(String, name = 'sector_updated_at')
    deleted_at = Column(String, name = 'sector_deleted_at')
    

class Status_model(Base):
    __tablename__ = 'mktzap_status'

    # Primary Key
    id = Column(Integer, name = 'status_id', primary_key = True)
    
    company_id = Column(Integer, name = 'status_company_id')
    should_close = Column(Integer, name = 'status_should_close')
    poll_id = Column(Integer, name = 'status_poll_id')
    should_require = Column(Integer, name = 'status_should_require')
    classification = Column(Integer, name = 'status_classification')
    flags = Column(Integer, name = 'status_flags')
    use_in_bot = Column(Integer, name = 'status_use_in_bot')
    
    name = Column(String, name ='status_name')
    color = Column(String, name = 'status_color')
    created_at = Column(String, name = 'status_created_at')
    updated_at = Column(String, name = 'status_updated_at')
    deleted_at = Column(String, name = 'status_deleted_at')
    hsm_id = Column(String, name = 'status_hsm_id')