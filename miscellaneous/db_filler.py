"""
Генерация sql-скрипта с insert-командами.
"""
import json
import multiprocessing
import random
import os
import types

from faker import Faker


fake = Faker()
Faker.seed(0)


def serialize_dict(d):
    return "'" + str(d).replace('\'', '"') + "'"


class FakeDataGenerator:
    @staticmethod
    def generate_increment(from_=0, to=float('inf')):
        i = from_
        while i < to:
            yield i
            i += 1

    @staticmethod
    def generate_increment_name(name, from_=0, to=float('inf')):
        i = from_
        while i < to:
            yield '{}_{}'.format(name, i)
            i += 1

    @staticmethod
    def generate_config():
        return json.dumps({
            'agent_target_first_answer_time': fake.pyint(min_value=1, max_value=120, step=1),
            'auto_prioritization_by_service_level': fake.pybool(),
            'target_service_level': fake.pyint(min_value=0, max_value=100, step=1)
        })

    @staticmethod
    def generate_bool():
        """
        Генерирует строковую интерпретацию boolean, т.к. именно в такой форме нужно записать
        её в insert-скрипт, чтобы PostgreSQL воспринял значение.
        """
        return random.choice(['true', 'false'])

    @staticmethod
    def generate_choice_with_probabilities(**choices):
        """
        В Python3 появилась возможность задавать вероятность выбора (2-м параметром).
        В контексте генерации данных для БД это необходимо, что число удалённых операторов
        было максимум 20% от общего числа.
        """
        return random.choices(choices.keys(), choices.values())


def generate_data_for_table(schema, table, configuration, limit):
    columns = ', '.join(configuration.keys())

    rows = [
        'BEGIN WORK;',
        'LOCK TABLE {schema}.{table} IN ROW EXCLUSIVE MODE;'.format(schema=schema, table=table),
        'INSERT INTO {schema}.{table}'.format(schema=schema, table=table),
        '\t({columns})'.format(columns=columns),
        'VALUES'
    ]

    for index in range(limit):
        row = []

        for generator in configuration.values():
            if isinstance(generator, types.GeneratorType):
                result = next(generator)
            elif callable(generator):
                result = generator()
            else:
                result = generator

            if isinstance(result, int):
                result = str(result)
            elif isinstance(result, str) and result not in ['NULL', 'null', 'true', 'false']:
                result = '\'' + result + '\''
            elif isinstance(result, dict):
                result = serialize_dict(result)

            row.append(result)

        string = '\t({})'.format(', '.join(row))
        string += ',' if index < limit - 1 else ';'

        rows.append(string)

    rows.append('COMMIT WORK;')

    path = os.path.join(os.path.dirname(__file__), '{schema}-{table}.sql'.format(schema=schema, table=table))

    os.remove(path)

    with open(path, mode='w') as f:
        f.write('\n'.join(rows))


def generate_data_for_tables(*table_configs):
    with multiprocessing.Pool(processes=len(table_configs)) as pool:
        pool.starmap(generate_data_for_table, table_configs)


if __name__ == '__main__':
    generate_data_for_tables(
        [
            'webim_service_pro_dev',
            'chatdepartment',
            {
                'departmentid': FakeDataGenerator.generate_increment(from_=12),
                'departmentkey': lambda: fake.company(),
                'departmentorder': FakeDataGenerator.generate_increment(from_=12),
                'departmentgeo': 'NULL',
                'isprivate': 'false',
                'ishidden': 'false',
                'config': FakeDataGenerator.generate_config(),
                'deleted': 'false'
            },
            100
        ],
        [
            'webim_site',
            'chatoperator',
            {
                'operatorid': FakeDataGenerator.generate_increment(from_=1),
                'fullname': lambda: fake.full_name(),
                'email': lambda: fake.email(),
                'created': '2020-03-03 17:51:53.523787+03',
                'password': 'f4eeddf4451523a0e460e4925b24ea3c',
                'recoverytoken': 'NULL',
                'recoverytime': 'NULL',
                'deleted': FakeDataGenerator.generate_choice_with_probabilities(),
                'operatororder': lambda: fake.pyint(min_value=1, max_value=2000),
                'avatar': 'NULL',
                'login': 'NULL',
                'sip': 'NULL',
                'sip_password': 'NULL',
                'answer': 'NULL',
                'subscribed': 0,
                'config': serialize_dict({
                    'answers': {'ru': []},
                    'max_chats_per_operator': 'null',
                    'backend_locale': 'ru',
                    'new_visitor_notification': 'null',
                    'additional_info': '',
                    'title': 'null'
                }),
                'passwordmodified': '2020-03-03 17:51:53.523787+03',
                'officeid': 'NULL'
            },
            100
        ],
        [
            'webim_service_pro_dev',
            'chatoperatordepartment',
            {
                'operatordepartmentid': FakeDataGenerator.generate_increment(from_=1),
                'operatorid': None,  # todo: выбор из тех id, которые в таблице chatoperatod
                'departmentid': None,  # todo: выбор из тех id, которые в таблице chatdepartment
                'priority': lambda: fake.pyint(min_value=1, max_value=100),
                'supervisor': 'false'
            },
            100
        ],
        [
            'webim_service_pro_dev',
            'chatthreadhistory',
            {
                'chatthreadhistoryid': FakeDataGenerator.generate_increment(from_=1),
                'threadid': None,
                'number': None,
                'dtm': None,
                'state': None,
                'operatorid': None,
                'departmentid': None,
                'event': None,
                'locate': 'ru',
                'officeid': 'NULL'
            },
            100
        ]
    )
