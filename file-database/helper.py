from record import *

numRecords = 0
recordSize = 0


def getRecord(data, recordNum):
    record = ""
    global numRecords, recordSize
    if recordNum >= 1 and recordNum <= numRecords:
        data.seek(recordNum * recordSize, 0)
        record = data.readline()
    return record


def searchRecord(data, overflow, name, fieldNames, fieldValues):
    record = binarySearch(data, name, fieldNames, fieldValues)
    if record:
        return record
    else:
        record = linearSearch(overflow, name, fieldNames, fieldValues)
        if record:
            return record
    return False


def binarySearch(data, name, fieldNames, fieldValues):
    setGlobals(fieldNames, fieldValues)
    low = 0
    high = numRecords - 1
    record = ""
    while high >= low:
        middle = int((low + high) / 2)
        record = getRecord(data, middle)
        dataName = recordName(record)
        if dataName == name:
            return Record(record, fieldNames, fieldValues, middle * recordSize, False)
        elif dataName < name:
            low = middle + 1
        else:
            high = middle - 1
    return False


def linearSearch(data, name, fieldNames, fieldValues):
    setGlobals(fieldNames, fieldValues)
    pos = 0
    data.seek(0)
    for line in data.readlines():
        record = Record(line, fieldNames, fieldValues, pos, True)
        if record.values[1].lower() == name.lower():
            return record
        pos += recordSize
    return False


def updateRecord(data, record, fieldNames, fieldValues):
    record.updateRecord()
    final = ""
    for i in range(len(record.values)):
        if len(record.values[i]) > fieldValues[i]:
            write = record.values[i][: fieldValues[i]]
        else:
            write = record.values[i]
            while range(fieldValues[i] - len(write)):
                write = write + "-"
        final += write
    data.seek(record.position)
    data.write(final)
    new = Record(
        getRecord(data, record.position / recordSize),
        fieldNames,
        fieldValues,
        record.position,
        record.overflow,
    )
    print("Here is the updated record")
    new.printRecord()


def addRecord(data, overflow, config, fieldNames, fieldValues):
    setGlobals(fieldNames, fieldValues)
    final = ""
    for i in range(len(fieldNames)):
        if fieldNames[i] != "totalRecordSize" and fieldNames[i] != "numRecords":
            print("Please enter a value for " + fieldNames[i])
            field = input().upper()
            if len(field) > fieldValues[i]:
                write = field[: fieldValues[i]]
            else:
                write = field
                while range(fieldValues[i] - len(write)):
                    write = write + "-"
            final += write
    num = overflow.seek(0, 2)
    overflow.write(final + "\n")
    flag = (num + recordSize) / recordSize > 4
    new = Record(getRecord(overflow, num / recordSize), fieldNames, fieldValues, num, not flag)
    print("Here is the new record")
    new.printRecord()
    if flag:
        print("Merging overflow into data file...")
        mergeData(data, overflow, config, fieldNames, fieldValues)


def mergeData(data, overflow, config, fieldNames, fieldValues):
    overflow.seek(0)
    records = []
    for record in overflow.readlines():
        records.append(record)
    add = len(records)
    records.sort(key=recordName)
    num = int(data.seek(0, 2) / recordSize)
    print(num)
    for i in range(num):
        data.seek(i * recordSize)
        line = data.readline()
        data.seek(i * recordSize)
        dataName = recordName(line)
        record = recordName(records[0])
        if dataName < record:
            data.write(line)
        else:
            data.write(records.pop(0))
            insert = 0
            for i in range(len(records)):
                if insert == 0:
                    record = recordName(records[i])
                    if dataName < record:
                        insert = i
            records.insert(insert, line)
    data.writelines(records)
    data.seek(0)
    data.readline()
    overflow.truncate(0)
    pos = config.seek(0, 2) - 14
    config.seek(pos)
    config.write("numRecords" + "," + str(num + add))
    config.seek(0)
    config.read()


def recordName(record):
    return record[4:38].replace("-", "").lower()


def deleteRecord(data, overflow, config, record, fieldNames, fieldValues):
    name = record.values[1] + "(deleted)"
    record.values[1] = name
    if len(name) > fieldValues[1]:
        write = name[: fieldValues[1]]
    else:
        write = name
        for _ in range(fieldValues[1] - len(name)):
            write += "-"
    if record.overflow:
        overflow.seek(record.position)
        writeDeleted(overflow, write, fieldNames, fieldValues)
        overflow.seek(record.position)
        overflow.readline()
    else:
        data.seek(record.position)
        writeDeleted(data, write, fieldNames, fieldValues)
        data.seek(record.position)
        data.readline()
    pos = config.seek(0, 2) - 14
    config.seek(pos)
    num = config.readline().split(",")
    config.seek(pos)
    config.write("numRecords" + "," + str(int(num[1]) - 1))
    config.seek(0)
    config.read()


def writeDeleted(data, write, fieldNames, fieldValues):
    for i in range(len(fieldNames)):
        if fieldNames[i] != "totalRecordSize" and fieldNames[i] != "numRecords" and fieldNames[i] != "name":
            for _ in range(fieldValues[i]):
                data.write(" ")
        elif fieldNames[i] == "name":
            data.write(write)


def setGlobals(fieldNames, fieldValues):
    global numRecords, recordSize
    numRecords = fieldValues[7]
    recordSize = fieldValues[6]
