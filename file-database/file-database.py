from typing import Dict


class Database():

    def __init__(self, name: str, fields: Dict[str, int]):
        num_records = 0
        with open(name + '.csv', 'r') as rf, open(name + '.data', 'w') as wf:
            for line in rf:
                record = line.replace('\n', '').split(',')
                for field_value, record_value in zip(fields.values(), record):
                    if len(record_value) > field_value:
                        wf.write(record_value[:field_value])
                    else:
                        write = record_value
                        while len(write) < field_value:
                            write += '-'
                        wf.write(write)
                wf.write('\n')
                num_records += 1

        with open(name + '.config', 'w') as f:
            record_size = 0
            for field_name, field_value in fields.items():
                f.write(field_name + ',' + str(field_value) + '\n')
                record_size += field_value
            f.write('record_size,' + str(record_size + 1) + '\n')
            f.write('num_records,' + str(num_records) + '\n')

        with open(name + '.overflow', 'w') as _:
            pass

        self.name = name
        self.fields = fields
        self.record_size = record_size
        self.num_records = num_records


if __name__ == '__main__':
    test_data_fields = {
        'rank': 4,
        'name': 35,
        'city': 20,
        'state': 2,
        'zip': 5,
        'employee': 10
    }
    database = Database('test_data', test_data_fields)
