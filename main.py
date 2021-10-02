#packages
import re
import os
import csv

#configs
fInputs = '\\text\\'
fOutputs = '\\csv\\'

def openFile(file):
    data = ''
    with open(file,'r') as f:
        data = f.read()
    return data

def getLines(data):
    matchData = []
    p = re.compile('[A]\d{2}\/\d{4}')
    for m in p.finditer(data):
        tempDict = {"location":m.start(), "string":m.group(), "startDate":"", "endDate":"","title":""}
        matchData.append(tempDict)
    return matchData

def getDates(data):
    dateData = []
    p = re.compile('\d{1,2} \w* \d{4}')
    for m in p.finditer(data):
        dateData.append(m.group())
    return dateData

def writeData(newPath, fileName, writeData):
    splitName = fileName.split('.')[0]
    saveFile = newPath + splitName + '.csv'
    checkExist = os.path.exists(saveFile)
    if not checkExist:
        os.remove(saveFile)

    with open(saveFile, 'w', newline='') as f:
        header = ['location','string', 'title', 'startDate', 'endDate']
        writer = csv.DictWriter(f,fieldnames=header)
        writer.writeheader()

        for dict in writeData:
            writer.writerow(dict)

def run(inputPath,outputPath):
    inputPath = os.getcwd() + inputPath
    outputPath = os.getcwd() + outputPath

    files = os.scandir(inputPath)

    for file in files:
        data = openFile(file)
        matchData = getLines(data)
        counter = 0
        totalItems = len(matchData)

        for section in matchData:
            print(counter)
            startSpot = section["location"] + len(section["string"]) + 1
            if counter+1 == totalItems:
                endSpot = len(data)
            else:
                endSpot = matchData[(counter+1)]["location"]
            restString = data[startSpot-1:endSpot]
            print(restString)
            section["title"] = restString
            dateData = getDates(section["title"])
            if len(dateData) == 2:
                section["startDate"] = dateData[0]
                section["endDate"] = dateData[1]
                section["title"] = section["title"].replace(section["startDate"], '')
                section["title"] = section["title"].replace(section["endDate"], '')
                section["title"] = section["title"].strip()
            counter = counter + 1
        print(matchData)
        writeData(outputPath, file.name, matchData)



run(fInputs,fOutputs)
print('Finished')