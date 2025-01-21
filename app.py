from datetime import date, timedelta
from src.controller import Controller
from src.schema import Schema
from src.config import CP2, SOL


def main(): 

    print('Preparendo-se para coletar dados...')

    number_of_days = 3
    inicial_date = (date.today() - timedelta(days = number_of_days)).isoformat()

    schema = Schema(CP2)


    controller = Controller(api_secrets=SOL, initial_date=inicial_date, schema=schema)

    controller.upsert_departaments()
    controller.upsert_status()
    controller.upsert_users()
    controller.upsert_history()

    print(f'✅ Dados coletados com sucesso!')


if __name__ == '__main__':
    main()