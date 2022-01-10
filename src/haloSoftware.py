import os.path
from os import path
import pandas as pd
import time
#import datetime
#import csv
import sys


typeNames = []
   

readedPage = ""
outputFile = ""



def findTypeOfCondition(values):
    if RepresentsInt(values[0]):
        if RepresentsInt(values[1]):
            return 0
        else:
            return 2
    else:
        if RepresentsInt(values[1]):
            return 1
        else:
            return 3

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def swapTwoRecord2(typeName,fileNum1, pageNum1, recordNum1, fileNum2, pageNum2, recordNum2):
    if fileNum1 != fileNum2:
        fileName = typeName + str(fileNum1) + ".txt"
        f = open(fileName)
        f.seek(312 + 4*2048 + 7+6*280)
        record1 = f.read(280)
        f.close()
        
        fileName = typeName + str(fileNum2) + ".txt"
        f = open(fileName)
        f.seek(312 + 0*2048 + 7+ 0*280)
        record2 = f.read(280)
        f.close()
        
        if( record2[20:40].rstrip() == ""):
            return 0
        
        fileName = typeName + str(fileNum1) + ".txt"
        f = open(fileName,"r+")
        f.seek(312 + 4*2048 + 7+6*280)
        f.write(record2)
        f.close()
        
        fileName = typeName + str(fileNum2) + ".txt"
        f = open(fileName,"r+")
        f.seek(312 + 0*2048 + 7 +0*280)
        f.write(record1)
        f.close()
        
    else:    
        fileName = typeName + str(fileNum1) + ".txt"
        f = open(fileName)
        f.seek(312 + (pageNum1-1)*2048 + 7 + (recordNum1-1)*280)
        record1 = f.read(280)
        f.close()
        
        fileName = typeName + str(fileNum2) + ".txt"
        f = open(fileName)
        f.seek(312 + (pageNum2-1)*2048 + 7 + (recordNum2-1)*280)
        record2 = f.read(280)
        f.close()
        
        print(record2[20:40].rstrip())
        if( record2[20:40].rstrip() == ""):
            return 0
        
        fileName = typeName + str(fileNum1) + ".txt"
        f = open(fileName,"r+")
        f.seek(312 + (pageNum1-1)*2048 + 7 + (recordNum1-1)*280)
        f.write(record2)
        f.close()
        
        fileName = typeName + str(fileNum2) + ".txt"
        f = open(fileName,"r+")
        f.seek(312 + (pageNum2-1)*2048 + 7 + (recordNum2-1)*280)
        f.write(record1)
        f.close()
        
    return 1


def swapTwoRecord(typeName,fileNum1, pageNum1, recordNum1, fileNum2, pageNum2, recordNum2):
    if fileNum1 != fileNum2:
        fileName = typeName + str(fileNum1) + ".txt"
        f = open(fileName)
        f.seek(312 + 4*2048 + 7+6*280)
        record1 = f.read(280)
        f.close()
        
        fileName = typeName + str(fileNum2) + ".txt"
        f = open(fileName)
        f.seek(312 + 0*2048 + 7+ 0*280)
        record2 = f.read(280)
        f.close()
        
        if( int(record1[20:40].rstrip()) > int(record2[20:40].rstrip())):
            return 0
        
        fileName = typeName + str(fileNum1) + ".txt"
        f = open(fileName,"r+")
        f.seek(312 + 4*2048 + 7+6*280)
        f.write(record2)
        f.close()
        
        fileName = typeName + str(fileNum2) + ".txt"
        f = open(fileName,"r+")
        f.seek(312 + 0*2048 + 7 +0*280)
        f.write(record1)
        f.close()
        
    else:    
        fileName = typeName + str(fileNum1) + ".txt"
        f = open(fileName)
        f.seek(312 + (pageNum1-1)*2048 + 7 + (recordNum1-1)*280)
        record1 = f.read(280)
        f.close()
        
        fileName = typeName + str(fileNum2) + ".txt"
        f = open(fileName)
        f.seek(312 + (pageNum2-1)*2048 + 7 + (recordNum2-1)*280)
        record2 = f.read(280)
        f.close()
        
        if( int(record1[20:40].rstrip()) > int(record2[20:40].rstrip())):
            return 0
        
        fileName = typeName + str(fileNum1) + ".txt"
        f = open(fileName,"r+")
        f.seek(312 + (pageNum1-1)*2048 + 7 + (recordNum1-1)*280)
        f.write(record2)
        f.close()
        
        fileName = typeName + str(fileNum2) + ".txt"
        f = open(fileName,"r+")
        f.seek(312 + (pageNum2-1)*2048 + 7 + (recordNum2-1)*280)
        f.write(record1)
        f.close()
        
    return 1


def createStringOfNewRecord(fieldValues):
    recordString = ""
    recordString += createNspaceString(20, "E226 S187")
    for i in range(len(fieldValues)):
        recordString += createNspaceString(20, fieldValues[i])
    for i in range(13-len(fieldValues)):
        recordString += createNspaceString(20, "")
    return recordString 

def insertStringToGivenPosition(givenStr,index,oldString):
    return oldString[:index] + givenStr  + oldString[index:]

def createNspaceString(neededLength,givenString):
    str1 = givenString
    for i in range(neededLength-len(givenString)):
        str1+=" "
    return str1
        
def createFieldNamesString(numOfFields,fieldNames):
    str1 = "planet              pk                  "
    for i in range(numOfFields):
        str1 += createNspaceString(20, fieldNames[i])
    for i in range(12-numOfFields):
        str1 += createNspaceString(20, "")
    return str1

def pageToList(page):
    listOfRecords = []
    for i in range(7):
        record = []
        for j in range(14):
            record.append(page[i*280 + j*20:i*280 + 20 + j*20].rstrip())
        listOfRecords.append(record)
    return listOfRecords

def listToPage(recordList,header):
    page = header
    for i in range(7):
        for j in range(14):
            page += createNspaceString(20, recordList[i][j])
    return createNspaceString(2048, page)


def deleteLastRecordOfType(typeName):
    lastFileForType = findLastTypeFile(typeName, 1)
    fileName = typeName + str(lastFileForType) + ".txt"
    f = open(fileName)
    f.seek(0)
    header = f.read(312)
    f.close()
    isNthpageEmpty = header[-5: ]
    areThereSpaceInNthPage = header[-10 : -5]
    pageToDeleteRecord = 10
    for i in range(5):
        if isNthpageEmpty[i] == "0":
            pageToDeleteRecord = i
                
    f = open(fileName)
    f.seek(312+pageToDeleteRecord*2048)
    readedPage = f.read(2048)
    f.close()
    
    pageHeader = readedPage[:7]

    for i in range(7):
        if pageHeader[i] == "1":
            recordToDelete = i
            
    newIsNthPageEmpty = isNthpageEmpty
    newAreThereSpaceInNthPage = areThereSpaceInNthPage
    
    if recordToDelete == 0 :
        if pageToDeleteRecord == 0 and lastFileForType != 1:
            os.remove(fileName)
            return 1
        else:
            newIsNthPageEmpty = isNthpageEmpty[:pageToDeleteRecord] + "1"+ isNthpageEmpty[pageToDeleteRecord+1 : ]
    if recordToDelete == 6 :
        newAreThereSpaceInNthPage = isNthpageEmpty[:pageToDeleteRecord] + "1"+ isNthpageEmpty[pageToDeleteRecord+1 : ]
    
    updatedPageHeader =""
    for i in range(recordToDelete):
        updatedPageHeader += "1"
    for i in range(7-recordToDelete):
        updatedPageHeader += "0"
        
    updatedFileHeader = header[:-10] + newAreThereSpaceInNthPage + newIsNthPageEmpty
    f = open(fileName, "r+")
    f.seek(0)
    f.write(updatedFileHeader)
    f.close()
    
    f = open(fileName, "r+")
    f.seek(312 + pageToDeleteRecord*2048 )
    f.write(updatedPageHeader)
    f.close()
    
    f = open(fileName, "r+")
    f.seek(312 + pageToDeleteRecord*2048 + 7 + recordToDelete*280)
    f.write(createNspaceString(280, ""))
    f.close()
    
    
    
    
        
        
            
            
    
    

def parseFieldNamesFromHeader(data):
    fieldsList = []
    for i in range(14):
        fieldNameWithSpace= data[22+i*20 : 22+(i+1)*20]
        fieldsList.append(fieldNameWithSpace.rstrip())
    return fieldsList


#finds the last file that stores types.
def findLastTypeFile(typeName,counter):
    while 1:
        typeFileName1 = typeName +str(counter)+".txt"
        typeFileName2 = typeName+ str(counter+1)+".txt"
        if path.exists(typeFileName2) == False :
            if path.exists(typeFileName1):
                return counter
            else :
                return 0
        counter+=1


def createTypeFile(typeName,numOfFields,fieldNames, fileNum):
    if fileNum == 1:
        if typeName in typeNames:
            return 0
    fileName = str(typeName) + str(fileNum) + ".txt"
    f = open(fileName, "w")
    if fileNum == 1:
        typeNames.append(typeName)
        #print(typeNames)
    fileHeader = createNspaceString(20,typeName)
    fileHeader += createNspaceString(2, str(numOfFields))
    fileHeader += createFieldNamesString(numOfFields, fieldNames)
    fileHeader += "1111111111"
    f.write(fileHeader)
    for i in range(5):
        emptyPage = createNspaceString(2048, "0000000")
        f.write(emptyPage)
    f.close()
    return 1


def inheritType(targetTypeName, sourceTypeName, additionalFields):
    sourceFile = str(sourceTypeName) + "1.txt"
    targetFile = str(targetTypeName) + "1.txt"
    if path.exists(sourceFile) == False :
        return 0
    elif path.exists(targetFile) == True :
        return 0
    else:
        f = open(sourceFile)
        f.seek(0)
        header = f.read(312)
        f.close()
        sourceFields = parseFieldNamesFromHeader(header)
        sourceFields = [i for i in sourceFields if i != ""]
        targetFields = sourceFields + additionalFields
        createTypeFile(targetTypeName, len(targetFields)-2, targetFields[2:],1)
        return 1
        
def listType():
    typeNames2 = sorted(typeNames)
    str1 = ""
    for i in range(len(typeNames2)):
        str1 += typeNames2[i]+"\n"
    f = open(outputFile, "a")
    f.write(str1)
    f.close()
    if len(typeNames2) == 0:
        return 0
    return 1

def deleteType(typeName):
    lastFileToDelete = findLastTypeFile(typeName, 1)
    if lastFileToDelete == 0:
        return 0
    typeNames.remove(typeName)
    for i in range(lastFileToDelete):
        os.remove(typeName + str(i+1) + ".txt")
    return 1


def createRecord(typeName, fieldValues):
    lastFileForType = findLastTypeFile(typeName, 1)
    if lastFileForType == 0:
        return 0
    fileName = typeName + str(lastFileForType) + ".txt"
    f = open(fileName)
    f.seek(0)
    header = f.read(312)
    f.close()
    isNthpageEmpty = header[-5: ]
    areThereSpaceInNthPage = header[-10 : -5]
    firstSuitablePage = -1
    for i in range(5):
        if areThereSpaceInNthPage[i] == "1":
            firstSuitablePage = i
            break
    
    if firstSuitablePage == -1:
        createTypeFile(typeName, len(fieldValues)-1, parseFieldNamesFromHeader(header)[2:], lastFileForType+1)
    
    readedPageIndex = 312 + 2048*firstSuitablePage
    f = open(fileName)
    f.seek(readedPageIndex)
    readedPage = f.read(2048)
    f.close()
    #print(readedPage)
    pageHeader = readedPage[:7]
    primaryKey = fieldValues[0]
    indexToInsert = 0
    isRecordFull = 0
    #print(pageHeader)
    for i in range(7):
        #print("asddasda")
        if pageHeader[i]== "0":
            indexToInsert = i
            break
        if pageHeader[i]== "1":
            currentRecord= readedPage[7 + i*280 :287 + i*280]
            if int(currentRecord[20:40].rstrip()) == int(primaryKey):
                return 0
            elif int(currentRecord[20:40].rstrip() ) > int(primaryKey):
                continue
            else:
                indexToInsert = i
                break
    
    for i in range(len(pageHeader)):
        if pageHeader[i] == "1":
            isRecordFull +=1
    updatedPageHeader = (isRecordFull+1)*"1" + (6-isRecordFull)*"0"
    updatedPage = updatedPageHeader + readedPage[7:]
    #print(updatedPage)
    updatedRecordStr = createStringOfNewRecord(fieldValues)
    updatedPage = insertStringToGivenPosition(updatedRecordStr, 7 + indexToInsert*280, updatedPage)
    updatedPage = updatedPage[:-280]
    f = open(fileName, "r+")
    f.seek(312 + 2048*firstSuitablePage)
    f.write(updatedPage)
    f.close()
    
    # file header'ı al
    f = open(fileName)
    f.seek(0)
    header = f.read(312)
    areThereSpaceInNthPage = header[-10 : -5]
    isNthpageEmpty = header[-5: ]
    f.close()
    
    newIsNthPageEmpty = isNthpageEmpty
    newAreThereSpaceInNthPage = areThereSpaceInNthPage
    
    if isRecordFull == 0:
        newIsNthPageEmpty = ""
        for i in range(5):
            if i == firstSuitablePage:
                newIsNthPageEmpty += "0"
            else:
                newIsNthPageEmpty += isNthpageEmpty[i]
    if isRecordFull == 6:
        newAreThereSpaceInNthPage = ""
        if firstSuitablePage == 5:
            createTypeFile(typeName, len(fieldValues)-1, parseFieldNamesFromHeader(header), lastFileForType+1)
        for i in range(5):
            if i == firstSuitablePage:
                newAreThereSpaceInNthPage += "0"
            else:
                newAreThereSpaceInNthPage += areThereSpaceInNthPage[i]
    
    updatedFileHeader = header[:-10] + newAreThereSpaceInNthPage + newIsNthPageEmpty
    f = open(fileName, "r+")
    f.seek(0)
    f.write(updatedFileHeader)
    f.close()
    
    if indexToInsert == 0:
        fileNum1= lastFileForType
        fileNum2 = lastFileForType
        pageNum1 = firstSuitablePage
        pageNum2 = firstSuitablePage+1
        recordNum1 = 7
        recordNum2 = 1
        if pageNum2 == 1:
            return 1
        
        while 1:
            result = swapTwoRecord(typeName,fileNum1, pageNum1, recordNum1, fileNum2, pageNum2, recordNum2)
            if result == 0:
                return 1
            else:
                recordNum1 += -1
                recordNum2 += -1
                if recordNum1 == 0:
                    recordNum1 = 7
                    pageNum1 += -1
                    if pageNum1 == 0:
                        if fileNum1 == 1:
                            return 1
                        else:
                            fileNum1 += -1
                            pageNum1 = 5
                if recordNum2 == 0:
                    recordNum2 = 7
                    
                    pageNum2 += -1
                    if pageNum2 == 0:
                        if fileNum2 == 1:
                            return 1
                        else:
                            fileNum1 += -1
                            pageNum1 = 5
            
    return 1          

    

def searchRecord(typeName, primaryKey):
    lastFileForType = findLastTypeFile(typeName, 1)
    if lastFileForType == 0:
        return 0
    counter= 0
    for l in range(lastFileForType):
        fileName = typeName + str(l+1) + ".txt"
        f = open(fileName)
        f.seek(0)
        fileHeader = f.read(312)
        f.close()
        isPageNEmpty = fileHeader[-5:]
        for i in range(5):
            if isPageNEmpty[i] == "0":
                f = open(fileName)
                f.seek(312+ 2048*i)
                page = f.read(2048)
                f.close()
                recordListOfPage = pageToList(page[7:])
                for j in range(7):
                    if recordListOfPage[j][0] == "":
                        if counter==0:
                            return 0
                        else:
                            return 1
                    print((recordListOfPage[j][1]) + "  " + primaryKey)
                    if recordListOfPage[j][1] == primaryKey:
                        counter+=1
                        str1 = "E226-S187"
                        for z in range(len(recordListOfPage[j])-1):
                            if recordListOfPage[j][z+1] != "":
                                str1 += " " + recordListOfPage[j][z+1]
                        str1 += "\n"
                        f = open(outputFile, "a")
                        f.write(str1)
                        f.close()
                        return 1
    if counter==0:
        return 0
    else:
        return 1

 
    
def updateRecord(typeName, primaryKey, fieldValues):
    lastFileForType = findLastTypeFile(typeName, 1)
    if lastFileForType == 0:
        return 0
    counter=0
    for l in range(lastFileForType):
        fileName = typeName + str(l+1) + ".txt"
        f = open(fileName)
        f.seek(0)
        fileHeader = f.read(312)
        f.close()
        isPageNEmpty = fileHeader[-5:]
        for i in range(5):
            if isPageNEmpty[i] == "0":
                f = open(fileName)
                f.seek(312+ 2048*i)
                page = f.read(2048)
                f.close()
                pageHeader = page[0:7]
                recordListOfPage = pageToList(page[7:])
                for j in range(7):
                    if recordListOfPage[j][0] == "":
                        if counter==0:
                            return 0
                        else:
                            return 1
                    if int(recordListOfPage[j][1]) == int(primaryKey):
                        counter+=1
                        for k in range(len(fieldValues)):
                            recordListOfPage[j][k+2] = fieldValues[k]
                        updatedPage = listToPage(recordListOfPage, pageHeader)
                        f = open(fileName,"r+")
                        f.seek(312+ 2048*i)
                        f.write(updatedPage)
                        f.close()
                        return 1
   
    if counter==0:
        return 0
    else:
        return 1


def listRecord(typeName):
    lastFileForType = findLastTypeFile(typeName, 1)
    counter=0
    if lastFileForType == 0:
        return 0
    for l in range(lastFileForType):
        fileName = typeName + str(l+1) + ".txt"
        f = open(fileName)
        f.seek(0)
        fileHeader = f.read(312)
        f.close()
        isPageNEmpty = fileHeader[-5:]
        numOfFields = fileHeader[20:22].rstrip()
        for i in range(5):
            if isPageNEmpty[i] == "0":
                print("inside method")
                f = open(fileName)
                f.seek(312+ 2048*i)
                page = f.read(2048)
                f.close()
                pageHeader = page[0:7]
                recordListOfPage = pageToList(page[7:])
                for j in range(7):
                    print(typeName +" " +str(l)+ " " + str(i) + " "+ str(j))
                    if recordListOfPage[j][1] != "":
                        counter+=1
                    else:
                        if counter==0:
                            return 0
                        else:
                            return 1
                    record ="E226-S187"
                    for k in range(int(numOfFields)+1):
                        record += " " + recordListOfPage[j][k+1]
                    record += "\n"
                    f = open(outputFile, "a")
                    f.write(record)
                    f.close()
                    
    if counter==0:
        return 0
    else:
        return 1
        
#typeOfCondition (num-num, field-num, num-field, field-field)      
#typeOfCondition2 (<, > , = )                   
def filterRecord(leftIndex, rightIndex , typeOfCondition, typeName, typeOfCondition2 ):
    lastFileForType = findLastTypeFile(typeName, 1)
    if lastFileForType == 0:
        return 0
    counter=0
    for l in range(lastFileForType):
        fileName = typeName + str(l+1) + ".txt"
        f = open(fileName)
        f.seek(0)
        fileHeader = f.read(312)
        f.close()
        isPageNEmpty = fileHeader[-5:]
        numOfFields = fileHeader[20:22].rstrip()
        fieldNames = parseFieldNamesFromHeader(fileHeader)
        index1= 0
        index2 =0
        if typeOfCondition == 1:
            index1 = fieldNames.index(leftIndex)
        if typeOfCondition == 2:
            index2 = fieldNames.index(rightIndex)
        if typeOfCondition == 3:
            index1 = fieldNames.index(leftIndex)
            index2 = fieldNames.index(rightIndex)
        for i in range(5):
            if isPageNEmpty[i] == "0":
                f = open(fileName)
                f.seek(312+ 2048*i)
                page = f.read(2048)
                f.close()
                pageHeader = page[0:7]
                recordListOfPage = pageToList(page[7:])
                for j in range(7):
                    if recordListOfPage[j][0] == "":
                        if counter==0:
                            return 0
                        else:
                            return 1
                    if typeOfCondition == 0:
                        condition = str(leftIndex) + typeOfCondition2 + str(rightIndex)
                    if typeOfCondition == 1:
                        condition = str(recordListOfPage[j][index1]) + typeOfCondition2 + str(rightIndex)
                    if typeOfCondition == 2:
                        condition =  str(leftIndex) + typeOfCondition2 + str(recordListOfPage[j][index2])
                    if typeOfCondition == 3:
                        condition =  str(recordListOfPage[j][index1]) + typeOfCondition2 + str(recordListOfPage[j][index2])
                        print(condition)
                    boolean = eval(condition)
                    
                    if boolean:
                        counter+=1
                        record ="E226-S187"
                        for k in range(int(numOfFields)+1):
                            record += " " + recordListOfPage[j][k+1]
                        
                        record += "\n"
                        f = open(outputFile,"a")
                        f.write(record)
                        f.close()
    if counter==0:
        return 0
    else:
        return 1

def deleteRecord(typeName, primaryKey ):
    lastFileForType = findLastTypeFile(typeName, 1)
    if lastFileForType == 0:
        return 0
    
    for l in range(lastFileForType):
        fileName = typeName + str(l+1) + ".txt"
        f = open(fileName)
        f.seek(0)
        fileHeader = f.read(312)
        f.close()
        isPageNEmpty = fileHeader[-5:]
        counter=0
        for i in range(5):
            if isPageNEmpty[i] == "0":
                f = open(fileName)
                f.seek(312+ 2048*i)
                page = f.read(2048)
                f.close()
                recordListOfPage = pageToList(page[7:])
                for j in range(7):
                    if recordListOfPage[j][0] == "":
                        if counter ==0:
                            return 0
                        else:
                            return 1
                    if recordListOfPage[j][1] == primaryKey:
                        counter+= 1
                        recordNum1 = j+1
                        pageNum1 = i+1
                        fileNum1 = l+1
                        recordNum2 = j+2
                        pageNum2 = i+1
                        fileNum2 = l+1
                        if recordNum1 == 7:
                            recordNum2 = 1
                            pageNum2 = pageNum1+1
                        if recordNum1 == 7 and pageNum1 ==5 :
                            recordNum2 = 1
                            pageNum2 = 1
                            fileNum2 = fileNum1 + 1
                            
                        while 1:
                            
                            result = swapTwoRecord2(typeName, fileNum1, pageNum1, recordNum1, fileNum2, pageNum2, recordNum2)
                            if result == 0:
                                deleteLastRecordOfType(typeName)
                                return 1
                            else:
                                recordNum1 += 1
                                recordNum2 += 1
                                if recordNum1 == 8:
                                    if pageNum1 == 5:
                                        fileNum1 +=1
                                        pageNum1 = 1
                                        recordNum1 = 1
                                    else:
                                        pageNum1 +=1
                                        recordNum1 = 1
                                if recordNum2 == 8:
                                    if pageNum2 == 5:
                                        fileNum2 +=1
                                        pageNum2 = 1
                                        recordNum2 = 1
                                    else:
                                        pageNum2 +=1
                                        recordNum2 = 1
                            
                        return 1
    if counter ==0:
        return 0
    else:
        return 1

'''
createTypeFile("typeName1", 4, ["a","b","c","d","","","","","","","",""],1)
createTypeFile("typeName2", 3, ["x","y","z","","","","","","","","",""],1)
createRecord("typeName2", ["1","1","sen","o"])
createRecord("typeName2", ["2","5","siz","onlar"])
createRecord("typeName2", ["4","4","w","e"])
createRecord("typeName2", ["3","7","t","y"])
createRecord("typeName2", ["7","2","o","p"])
createRecord("typeName2", ["12","3","s","d"])
createRecord("typeName2", ["9","9","g","h"])
createRecord("typeName2", ["8","2","k","l"])
createRecord("typeName2", ["6","1","sen","o"])
createRecord("typeName2", ["10","1","siz","onlar"])
createRecord("typeName2", ["11","1","w","e"])
createRecord("typeName2", ["14","1","t","y"])
createRecord("typeName2", ["15","1","o","p"])
createRecord("typeName2", ["5","1","s","d"])
createRecord("typeName2", ["13","1","g","h"])
createRecord("typeName2", ["16","1","k","l"])
print(searchRecord("typeName2", "28"))
print(pageToList("E226 S187           1                   ben                 sen                 o                                                                                                                                                                                                       E226 S187           2                   biz                 siz                 onlar                                                                                                                                                                                                   E226 S187           3                   r                   t                   y                                                                                                                                                                                                       E226 S187           4                   q                   w                   e                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                "))
print(updateRecord("typeName2", "2",["2" ,"roz", "ber"]))
listRecord("typeName2")
filterRecord("1", "x", 2, "typeName2", "==")
deleteRecord("typeName2", "1")

createTypeFile("animal", 4, ["name","age","height","weight","","","","","","","",""],1)
inheritType("human", "animal", ["alias","occupation"])
createRecord("human", ["3", "MarkWebbler" ,"27" ,"178", "81", "Shadow engineer"])
listRecord("human")
createRecord("human", ["1", "JaneBradley" ,"24", "171", "61" ,"Leaf doctor"])

''' 

def main():
    columns = {'username':[],
        'occurrence':[],
        'operation' : [],
        'status' : []}
 
    # Create DataFrame
    df = pd.DataFrame(columns)
    
    global typeNames
    if path.exists("typeNames.txt") == 1:
        f = open("typeNames.txt")
        x = f.read()
        typeNames = x.split(" ")[:-1]
        
    
    userDict = {}
    if path.exists("userName.txt") == 0:
        f = open("userName.txt", "w")
        f.close()
    else:
        f = open("userName.txt")
        userNamess = f.read()
        f.close()
        userNames = userNamess.split(" ")
        
    if path.exists("passwords.txt") == 0:
        f = open("passwords.txt", "w")
        f.close()
    else:
        f = open("passwords.txt")
        passwordss = f.read()
        f.close()
        passwords = passwordss.split(" ")
        for i in range(len(userNames)-1):
            userDict[userNames[i]] = passwords[i]
    
            
        
    user = "null"
    
    newLog = {}
    
    global outputFile
    outputFile = sys.argv[2]
    #outputFile = "output.txt"
    f = open(outputFile, "w")
    f.close()
    filepath = sys.argv[1]
    #filepath = "input.txt"
    with open(filepath) as fp:
       lines = fp.readlines()
       for linee in lines:
           line = linee.split()
           try:
               if line[0] == "register":
                   if line[1] == "user":
                       name = line[2]
                       pass1 = line[3]
                       pass2 = line[4]
                       if pass1 != pass2:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : "register user"+ str(name), 'status' : "failure"}
                       elif name in userDict:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : "register user"+str(name), 'status' : "failure"}
                       else:
                           userDict[name] = pass1
                           f = open("userName.txt", "a")
                           f.write(name + " ")
                           f.close()
                           f = open("passwords.txt", "a")
                           f.write(pass1 + " ")
                           f.close()
                           
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : "register user "+str(name), 'status' : "success"}
                       df = df.append(newLog, ignore_index=True)
                   continue
               if line[0] == "login":
                   if user == "null":
                       name = line[1]
                       password = line[2]
                       if name in userDict:
                           if userDict[name] == password:
                               user = name
                               newLog = {'username':str(name),'occurrence':str(time.time()),'operation' : "login", 'status' : "success"}
                       else:
                           newLog = {'username':str(name),'occurrence':str(time.time()),'operation' : "login", 'status' : "failure"}
                   else:
                       newLog = {'username':str(name),'occurrence':str(time.time()),'operation' : "login", 'status' : "failure"}
                   df = df.append(newLog, ignore_index=True)
                   continue
               if line[0] == "logout":
                   if user == "null":
                       newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : "logout", 'status' : "failure"}
                   else:
                       newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : "logout", 'status' : "success"}
                       user = "null"
                   df = df.append(newLog, ignore_index=True)
                   continue
                           
               if user == "null":
                   newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip() , 'status' : "failure"}
                   df = df.append(newLog, ignore_index=True)
                   continue
               
               if line[1] == "type":
                   if line[0] == "create":
                       typeName= line[2]
                       numOfFields = line[3]
                       fieldNames= [str(i) for i in line if line.index(i)>= 4 ]
                       result = createTypeFile(typeName, int(numOfFields), fieldNames, 1)
                       if result == 1:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "success"}
                       else:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "failure"}
                       df = df.append(newLog, ignore_index=True)  
                           
                   if line[0] == "delete":
                       typeName = line[2]
                       result = deleteType(typeName)
                       if result == 1:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "success"}
                       else:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "failure"}
                       df = df.append(newLog, ignore_index=True)
                   if line[0] == "inherit":
                       targetTypeName = line[2]
                       sourceTypeName = line[3]
                       additionalFields= [str(i) for i in line if line.index(i)>= 4 ]
                       result = inheritType(targetTypeName, sourceTypeName, additionalFields)
                       if result == 1:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "success"}
                       else:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "failure"}
                       df = df.append(newLog, ignore_index=True)
                   if line[0] == "list":
                       result = listType()
                       if result == 1:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "success"}
                       else:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "failure"}
                       df = df.append(newLog, ignore_index=True)
               if line[1] == "record":
                   
                   if line[0] == "create":
                       
                       typeName = line[2]
                       fieldValues = [str(i) for i in line if line.index(i)>= 3 ]
                       result = createRecord(typeName, fieldValues)
                       if result == 1:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "success"}
                       else:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "failure"}
                       df = df.append(newLog, ignore_index=True)
                   if line[0] == "delete":
                       
                       typeName = line[2]
                       primaryKey = line[3]
                       result = deleteRecord(typeName, primaryKey)
                       if result == 1:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "success"}
                       else:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "failure"}
                       df = df.append(newLog, ignore_index=True)
                   if line[0] == "update":
                       
                       typeName = line[2]
                       primaryKey = line[3]
                       fieldValues = [str(i) for i in line if line.index(i)>= 4 ]
                       result = updateRecord(typeName, primaryKey, fieldValues)
                       if result == 1:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "success"}
                       else:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "failure"}
                       df = df.append(newLog, ignore_index=True)
                   if line[0] == "search":
                       
                       typeName = line[2]
                       primaryKey = line[3]
                       result = searchRecord(typeName, primaryKey)
                       if result == 1:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "success"}
                       else:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "failure"}
                       df = df.append(newLog, ignore_index=True)
                   if line[0] == "list":
                       print("list record")
                       typeName = line[2]
                       result = listRecord(typeName) 
                       if result == 1:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "success"}
                       else:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "failure"}
                       df = df.append(newLog, ignore_index=True)
                   if line[0] == "filter":
                       
                       typeName = line[2]
                       condition = line[3]
                       d = condition.split("<=")
                       e = condition.split(">=")
                       a = condition.split("<")
                       b = condition.split(">")
                       c = condition.split("==")
                       if(len(d) > 1):
                           result=filterRecord(d[0], d[1], findTypeOfCondition(d), typeName, "<=")
                           print(result)
                           continue
                       if(len(e) > 1):
                           result =filterRecord(e[0], e[1], findTypeOfCondition(e), typeName, ">=")
                           print(result)
                           continue
                       if(len(a) > 1):
                            result = filterRecord(a[0], a[1], findTypeOfCondition(a), typeName, "<")
                       if(len(b) > 1):
                            result = filterRecord(b[0], b[1], findTypeOfCondition(b), typeName, ">")
                       if(len(c) > 1):
                           result = filterRecord(c[0], c[1], findTypeOfCondition(c), typeName, "==")
                       if result == 1:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "success"}
                       else:
                           newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "failure"}
                       df = df.append(newLog, ignore_index=True)
           except:
               
               newLog = {'username':str(user),'occurrence':str(time.time()),'operation' : linee.rstrip(), 'status' : "failure"}
               df = df.append(newLog, ignore_index=True)
               continue
                    
    print(df)
    df.to_csv('haloLog.csv', mode='a', header=False, index=False)  
    
    
    f = open("typeNames.txt", "w")
    strr=""
    print(typeNames)
    for i in range(len(typeNames)):
        strr+= typeNames[i]+" "
    print(strr)
    f.write(strr)
    f.close()
    
    print(typeNames)
      #typeOfCondition (num-num, field-num, num-field, field-field)  
    
if __name__ == '__main__':
    main()