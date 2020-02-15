class Record:
    def __init__(self, record, fieldNames, fieldValues, position, overflow):
        count = 0
        for i in range(len(fieldNames)):
            if fieldNames[i] != 'totalRecordSize' and fieldNames[i] != 'numRecords':
                value = record[count:fieldValues[i] + count].replace('-', '')
                count += fieldValues[i]
                self.names.append(fieldNames[i])
                self.values.append(value)
        self.position = position
        self.overflow = overflow

    overflow = False
    position = 0
    names = []
    values = []

    def printRecord(self):
        for i in range(len(self.values)):
            print('{}: {}'.format(self.names[i], self.values[i]))

    def updateRecord(self):
        for i in range(len(self.values)):
            if self.names[i] != 'name':
                print('The current {} is {}. Enter the new value or just press enter for no change.'.format(self.names[i], self.values[i]))
                update = input()
                if update != '':
                    self.values[i] = update
