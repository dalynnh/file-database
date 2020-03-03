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

        with open(name + '.overflow', 'w') as _:
            pass

        self.name = name
        self.fields = fields
        self.num_records = num_records
        self.record_size = 1
        for value in fields.values():
            self.record_size += value

    def get_record_by_id(self, i: int) -> Dict[str, int] or str:
        return (
            self._binary_search(i)
            or self._linear_search(i)
            or 'Record could not be found'
        )

    def _binary_search(self, i) -> Dict[str, int]:
        with open(self.name + '.data', 'r') as f:
            low = 0
            high = self.num_records - 1
            record = ""
            while high >= low:
                middle = int((low + high) / 2)
                f.seek(middle * self.record_size)
                record = f.readline()
                key = next(iter(self.fields))
                data_id = int(
                    record[:self.fields[key]]
                    .replace("-", "").lower()
                )
                if data_id == i:
                    return self._str_to_dict(record)
                elif data_id < i:
                    low = middle + 1
                else:
                    high = middle - 1
            return None

    def _linear_search(self, i) -> Dict[str, int]:
        with open(self.name + '.overflow', 'r') as f:
            for line in f.readlines():
                data_id = int(
                    line[:next(iter(self.fields.values))]
                    .replace("-", "").lower()
                )
                if data_id == i:
                    return self._str_to_dict(line)
            return None

    def _str_to_dict(self, record) -> Dict[str, int]:
        result = {}
        pos = 0
        for key, value in self.fields.items():
            result[key] = record[pos: value + pos].replace('-', '')
            pos += value
        return result


if __name__ == '__main__':
    test_data_fields = {
        'id': 2,
        'name': 6
    }
    database = Database('test_data', test_data_fields)
    print(database.get_record_by_id(12))
