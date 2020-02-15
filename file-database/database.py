import helper

data = None
config = None
overflow = None
databaseName = ""
fieldNames = []
fieldValues = []


def createDB():
    print("Which csv file would you like to create the database out of?")
    csvFilename = input()
    fieldNames = ['rank', 'name', 'city', 'state', 'zip',
                  'employee', 'totalRecordSize']
    fieldValues = [4, 35, 20, 2, 5, 10, 77]
    numRecords = 0
    csvFile = open(csvFilename + ".csv", "r")
    data = open(csvFilename + ".data", "w")
    for line in csvFile:
        record = line.replace("\n", "").split(",")
        for i in range(len(fieldNames)):
            if fieldNames[i] != "totalRecordSize":
                if len(record[i]) > fieldValues[i]:
                    write = record[i][: fieldValues[i]]
                else:
                    write = record[i]
                    while range(fieldValues[i] - len(write)):
                        write = write + "-"
                data.write(write)
        data.write("\n")
        numRecords += 1
    data.close()
    csvFile.close()
    config = open(csvFilename + ".config", "w")
    for i in range(len(fieldNames)):
        config.write(fieldNames[i] + "," + str(fieldValues[i]) + "\n")
    config.write("numRecords," + str(numRecords))
    config.close()
    overflow = open(csvFilename + ".overflow", "w")
    overflow.close()


def openDB():
    global data, config, overflow, databaseName
    if data:
        print(
            databaseName
            + " is currently open. Please close before opening a new DB."
        )
    else:
        print("Which database would you like to open?")
        databaseName = input()
        data = open(databaseName + ".data", "r+")
        config = open(databaseName + ".config", "r+")
        overflow = open(databaseName + ".overflow", "r+")


def closeDB():
    global data, config, overflow, databaseName
    if data:
        print("Closing the database " + databaseName)
        databaseName = ""
        data.close()
        data = None
        config.close()
        config = None
        overflow.close()
        overflow = None
    else:
        print("There are no databases currently open.")


def displayRecord():
    global data, overflow, fieldNames, fieldValues
    if data:
        setFields()
        print(
            "Enter the name of the record you would like to search for. Limited to 35 characters."
        )
        name = input().lower()
        record = helper.searchRecord(data, overflow, name, fieldNames, fieldValues)
        if record:
            record.printRecord()
        else:
            print("No record was found with name (" + name + ")")
    else:
        print(
            "There are no databases currently open. Please open a database to display a record."
        )


def updateRecord():
    global data, overflow, fieldNames, fieldValues
    if data:
        setFields()
        print(
            "Enter the name of the record you would like to update. Limited to 35 characters."
        )
        name = input().lower()
        record = helper.searchRecord(data, overflow, name, fieldNames, fieldValues)
        if record:
            helper.updateRecord(data, record, fieldNames, fieldValues)
        else:
            print("No record was found with name (" + name + ")")
    else:
        print(
            "There are no databases currently open. Please open a database to update a record."
        )


def createReport():
    global data

    report = open("report.txt", "w")

    if data:
        for i in range(10):
            line = data.readline()
            rank = line[:4].replace("-", "")
            name = line[4:39].replace("-", "")
            city = line[39:59].replace("-", "")
            state = line[59:61].replace("-", "")
            zipCode = line[61:66].replace("-", "")
            numEmployees = line[66:].replace("-", "")
            report.write(
                "Record {}\n   Rank: {}\n   Name: {}\n   City: {}\n   State: {}\n   Zip Code: {}\n   Number of Employees: {}\n".format(
                    i + 1, rank, name, city, state, zipCode, numEmployees
                )
            )

        print("Report created.")
    else:
        print(
            "There are no databases currently open. Please open a database to create a report."
        )

    report.close()


def addRecord():
    global data, overflow, config, fieldNames, fieldValues
    if overflow:
        setFields()
        helper.addRecord(data, overflow, config, fieldNames, fieldValues)
    else:
        print(
            "There are no databases currently open. Please open a database to add a record."
        )


def deleteRecord():
    global data, overflow, config, fieldNames, fieldValues
    if data:
        setFields()
        print(
            "Enter the name of the record you would like to delete. Limited to 35 characters."
        )
        name = input().lower()
        record = helper.searchRecord(data, overflow, name, fieldNames, fieldValues)
        if record:
            helper.deleteRecord(data, overflow, config, record, fieldNames, fieldValues)
        else:
            print("No record was found with name (" + name + ")")
    else:
        print(
            "There are no databases currently open. Please open a database to delete a record."
        )


def setFields():
    global fieldNames, fieldValues, config
    if not fieldNames:
        config.seek(0)
        for line in config.readlines():
            name, value = line.split(",")
            fieldNames.append(name)
            fieldValues.append(int(value))
