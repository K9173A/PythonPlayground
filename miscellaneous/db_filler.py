"""
Генерация sql-скрипта с insert-командами.
"""
import json
import random
import os
import types

from faker import Faker


fake = Faker()
Faker.seed(0)


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
        return random.choice(['true', 'false'])


def main(schema, table, configuration, limit):
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
            elif isinstance(result, str) and result not in ['NULL', 'true', 'false']:
                result = '\'' + result + '\''
            elif isinstance(result, dict):
                result = "'" + str(result).replace('\'', '"') + "'"

            row.append(result)

        string = '\t({})'.format(', '.join(row))
        string += ',' if index < limit - 1 else ';'

        rows.append(string)

    rows.append('COMMIT WORK;')

    path = os.path.join(os.path.dirname(__file__), '{schema}-{table}.sql'.format(schema=schema, table=table))

    os.remove(path)

    with open(path, mode='w') as f:
        f.write('\n'.join(rows))


if __name__ == '__main__':
    main(schema='webim_service_pro_dev',
         table='chatdepartment',
         configuration={
             'departmentid': FakeDataGenerator.generate_increment(from_=12),
             'departmentkey': lambda: fake.company(),
             'departmentorder': FakeDataGenerator.generate_increment(from_=12),
             'departmentgeo': 'NULL',
             'isprivate': 'false',
             'ishidden': 'false',
             'config': FakeDataGenerator.generate_config(),
             'deleted': 'false'
         },
         limit=100)
