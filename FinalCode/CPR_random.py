import random
import os, glob
from msilib.schema import _Validation_records
import cv2 as cv
import numpy as np
from dataclasses import dataclass
import CPR_tools as cpr

sampledColoniesFolder = "sampleColonies"

#Randomizing colonies from 1-6 files and selecting 96: creates a list and 6 text files
def randomize(folder_path):
    count = 0
    colonyXY = []
    petriXY = []
    WellLocations = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12',
                    'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12',
                    'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12',
                    'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12',
                    'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12',
                    'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
                    'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12',
                    'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12']

    #need this to grab petri dishes in order of 1-6 *****
    for filename in glob.glob(os.path.join(folder_path, '*.txt')):
        with open(filename, 'r') as old_file: 
            count = count + 1
            with open(f"P{count}colonies.txt", "w") as new_file:
                for line in old_file:
                    wordCount = 0
                    words = line.split()
                    for word in words:
                        colonyXY.append(word)
                    petriXY.append(list(colonyXY))
                    new_file.write(" ".join(colonyXY))  # Join colonyXY items with space
                    new_file.write("\n")
                    colonyXY.clear()
    #--- END READING IN TEXT FILES --------------------------------------------------------------------   
    
    #--- VARIABLES, LISTS AND DICTIONARY INITIALIZATION -----------------------------------------------
    #this will store all of the colonies~ might need to be a dictionary to save pos 1 and 2 of text file
    P1coloniesList = ['P1']     #initialize with first index being a name to compare to later on (remeber for lengths to sub 1)
    P2coloniesList = ['P2']
    P3coloniesList = ['P3']
    P4coloniesList = ['P4']
    P5coloniesList = ['P5']
    P6coloniesList = ['P6']
    #Number of colonies in each Petri dish
    P1lengthColonies = 0
    P2lengthColonies = 0
    P3lengthColonies = 0
    P4lengthColonies = 0
    P5lengthColonies = 0
    P6lengthColonies = 0
    #total amount of colonies in run
    totalLength = 0
    #dictionary to store length of colony set and the name
    colonyLengthSet      = {}  
    #dictionary to store length of colonies to be sampled with the name of Petri dish
    sampleLengthSet      = {}  
    #--- END OF INSTATIONATIONS -----------------------------------------------------------------------

    #--- ADD CONTENTS OF FILE INTO A LIST FOR X NUMBER OF PETRI DISHES --------------------------------
    #example of each line in file: 0 Xpos Ypos 0 0 0
    tempList = []
    if(count >= 1):
        with open('P1colonies.txt') as f:
            for line in f:
                words = line.split()  # Split the line into words
                tempList.extend(words)  # Extend tempList with the words from the line
                P1coloniesList.append(tempList.copy())  # Append a copy of tempList to P1coloniesList
                tempList.clear() 
            P1lengthColonies = len(P1coloniesList)-1
            #random.shuffle(P1coloniesList[1:P1lengthColonies])
            colonyLengthSet.update({P1lengthColonies : 'P1'})   #add to dictionary

    if(count >= 2):
        with open('P2colonies.txt') as f:
            for line in f:
                words = line.split()  # Split the line into words
                tempList.extend(words)  # Extend tempList with the words from the line
                P2coloniesList.append(tempList.copy())  # Append a copy of tempList to P1coloniesList
                tempList.clear() 
        P2lengthColonies = len(P2coloniesList)-1
        #random.shuffle(P2coloniesList[1:P2lengthColonies])
        colonyLengthSet.update({P2lengthColonies : 'P2'})

    if(count >= 3):
        with open('P3colonies.txt') as f:
            for line in f:
                words = line.split()  # Split the line into words
                tempList.extend(words)  # Extend tempList with the words from the line
                P3coloniesList.append(tempList.copy())  # Append a copy of tempList to P1coloniesList
                tempList.clear() 
        P3lengthColonies = len(P3coloniesList)-1
        #random.shuffle(P3coloniesList[1:P3lengthColonies])
        colonyLengthSet.update({P3lengthColonies : 'P3'})

    if(count >= 4):
        with open('P4colonies.txt') as f:
            for line in f:
                words = line.split()  # Split the line into words
                tempList.extend(words)  # Extend tempList with the words from the line
                P4coloniesList.append(tempList.copy())  # Append a copy of tempList to P1coloniesList
                tempList.clear() 
        P4lengthColonies = len(P4coloniesList)-1
        #random.shuffle(P4coloniesList[1:P4lengthColonies])
        colonyLengthSet.update({P4lengthColonies : 'P4'})

    if(count >= 5):
        with open('P5colonies.txt') as f:
            for line in f:
                words = line.split()  # Split the line into words
                tempList.extend(words)  # Extend tempList with the words from the line
                P5coloniesList.append(tempList.copy())  # Append a copy of tempList to P1coloniesList
                tempList.clear() 
        P5lengthColonies = len(P5coloniesList)-1
        #random.shuffle(P5coloniesList[1:P5lengthColonies])
        colonyLengthSet.update({P5lengthColonies : 'P5'})

    if(count >= 6):
        with open('P6colonies.txt') as f:
            for line in f:
                words = line.split()  # Split the line into words
                tempList.extend(words)  # Extend tempList with the words from the line
                P6coloniesList.append(tempList.copy())  # Append a copy of tempList to P1coloniesList
                tempList.clear() 
        P6lengthColonies = len(P6coloniesList)-1
        #random.shuffle(P6coloniesList[1:P6lengthColonies])
        colonyLengthSet.update({P6lengthColonies : 'P6'})
    #--- DONE CREATING THE INITIAL LISTS --------------------------------------------------------------

    #find how many colonies in this run
    totalLength = P1lengthColonies + P2lengthColonies + P3lengthColonies + P4lengthColonies + P5lengthColonies + P6lengthColonies
    print("Total number of colonies in run: " + str(totalLength))

    #sort from smallest to largest
    myKeys = list(colonyLengthSet.keys())
    myKeys.sort()
    colonyLengthSet = {i: colonyLengthSet[i] for i in myKeys}

    #get the colony with the largest set
    numPetriDishes = len(colonyLengthSet)           #get how many petri dishes there are
    largestNumber = list(colonyLengthSet)[-1]       #get the last key
    largestName = colonyLengthSet[largestNumber]
    print(f"Petri dish with largest sample {largestName} as: " + str(largestNumber))

    #math part to receive fraction*length
    fraction = 96/totalLength

    #for x in range(numPetriDishes):
    P1SampleLength = round(fraction*P1lengthColonies)
    sampleLengthSet.update({P1SampleLength : 'P1'})
    P2SampleLength = round(fraction*P2lengthColonies)
    sampleLengthSet.update({P2SampleLength : 'P2'})
    P3SampleLength = round(fraction*P3lengthColonies)
    sampleLengthSet.update({P3SampleLength : 'P3'})
    P4SampleLength = round(fraction*P4lengthColonies)
    sampleLengthSet.update({P4SampleLength : 'P4'})
    P5SampleLength = round(fraction*P5lengthColonies)
    sampleLengthSet.update({P5SampleLength : 'P5'})
    P6SampleLength = round(fraction*P6lengthColonies)
    sampleLengthSet.update({P6SampleLength : 'P6'})

    #sort through the sampling number for each Petri dish
    mySampleKeys = list(sampleLengthSet.keys())
    mySampleKeys.sort()
    sampleLengthSet = {i: sampleLengthSet[i] for i in mySampleKeys}
    largestSampleSet = list(sampleLengthSet)[-1]       #get the last key
    largestSampleName = sampleLengthSet[largestSampleSet]
    print(f"Largest Petri dish will sample {largestSampleName} as: " + str(largestSampleSet))


    sampledColoniesLength = P1SampleLength + P2SampleLength + P3SampleLength + P4SampleLength + P5SampleLength + P6SampleLength
    if(sampledColoniesLength > 96):
        delete = sampledColoniesLength - 96
        sampledColoniesLength = sampledColoniesLength - delete
        largestSampleSet = largestSampleSet - delete
        print(f"largest sample must lose {delete} colonies")

    if(sampledColoniesLength < 96):
        add = 96 - sampledColoniesLength
        sampledColoniesLength = sampledColoniesLength + add
        if(largestNumber > largestSampleSet):
            largestSampleSet = largestSampleSet + add
        print(f"largest sample must add {add} colonies")    

    print("Sampled colonies in set: " + str(sampledColoniesLength))

    #need the largest one to work
    petri1 = 0
    petri2 = 0
    petri3 = 0
    petri4 = 0
    petri5 = 0
    petri6 = 0

    #--- SIZE DOWN THE LIST TO 96 ---------------------------------------------------------------------
    #find which one is the largest and create it's new list
    if(P1coloniesList[0] == largestSampleName):
        P1coloniesList=P1coloniesList[1:largestSampleSet+1]
        petri1 = 1
    if(P2coloniesList[0] == largestSampleName):
        P2coloniesList=P2coloniesList[1:largestSampleSet+1]
        petri2 = 1
    if(P3coloniesList[0] == largestSampleName):
        P3coloniesList=P3coloniesList[1:largestSampleSet+1]
        petri3 = 1
    if(P4coloniesList[0] == largestSampleName):
        P4coloniesList=P4coloniesList[1:largestSampleSet+1]
        petri4 = 1
    if(P5coloniesList[0] == largestSampleName):
        P5coloniesList=P5coloniesList[1:largestSampleSet+1]
        petri5 = 1
    if(P6coloniesList[0] == largestSampleName):
        P6coloniesList=P6coloniesList[1:largestSampleSet+1]
        petri6 = 1

    #Take the first P1 samples of every colony list if it wast not the largest
    if(petri1 == 0):
        P1coloniesList= P1coloniesList[1:P1SampleLength+1]
    if(petri2 == 0):
        P2coloniesList= P2coloniesList[1:P2SampleLength+1]
    if(petri3 == 0):
        P3coloniesList= P3coloniesList[1:P3SampleLength+1]
    if(petri4 == 0):
        P4coloniesList= P4coloniesList[1:P4SampleLength+1]
    if(petri5 == 0):
        P5coloniesList= P5coloniesList[1:P5SampleLength+1]
    if(petri6 == 0):
        P6coloniesList= P6coloniesList[1:P6SampleLength+1]
        
    #--- Randomizing the list that were created -------------------------------------------------------
    random.shuffle(P1coloniesList)
    random.shuffle(P2coloniesList)
    random.shuffle(P3coloniesList)
    random.shuffle(P4coloniesList)
    random.shuffle(P5coloniesList)
    random.shuffle(P6coloniesList)

    #--- DELETE THE FILE CREATED USED THROUGHOUT ---#
    for x in range(1, count+1):
        os.remove(f'P{x}colonies.txt')

    #writing a directory to hold 6 text files of PxcoloniesList
    #Will need to update with final foler location
    os.makedirs(sampledColoniesFolder)

    wellLocationCount = -1
    sampleColonies1Line = [sublist[0:6] for sublist in P1coloniesList]
    file_path = os.path.join(sampledColoniesFolder, "image1.txt")
    with open(file_path, "w") as file:
        for line in sampleColonies1Line:
            wellLocationCount = wellLocationCount + 1
            file.write(' '.join(line))
            file.write(' ' + WellLocations[wellLocationCount] + '\n')


    sampleColonies2Line = [sublist[0:6] for sublist in P2coloniesList]
    file_path = os.path.join(sampledColoniesFolder, "image2.txt")
    with open(file_path, "w") as file:
        for line in sampleColonies2Line:
            wellLocationCount = wellLocationCount + 1
            file.write(' '.join(line))
            file.write(' ' + WellLocations[wellLocationCount] + '\n')

    sampleColonies3Line = [sublist[0:6] for sublist in P3coloniesList]
    file_path = os.path.join(sampledColoniesFolder, "image3.txt")
    with open(file_path, "w") as file:
        for line in sampleColonies3Line:
            wellLocationCount = wellLocationCount + 1
            file.write(' '.join(line))
            file.write(' ' + WellLocations[wellLocationCount] + '\n')

    sampleColonies4Line = [sublist[0:6] for sublist in P4coloniesList]
    file_path = os.path.join(sampledColoniesFolder, "image4.txt")
    with open(file_path, "w") as file:
        for line in sampleColonies4Line:
            wellLocationCount = wellLocationCount + 1
            file.write(' '.join(line))
            file.write(' ' + WellLocations[wellLocationCount] + '\n')

    sampleColonies5Line = [sublist[0:6] for sublist in P5coloniesList]
    file_path = os.path.join(sampledColoniesFolder, "image5.txt")
    with open(file_path, "w") as file:
        for line in sampleColonies5Line:
            wellLocationCount = wellLocationCount + 1
            file.write(' '.join(line))
            file.write(' ' + WellLocations[wellLocationCount] + '\n')

    sampleColonies6Line = [sublist[0:6] for sublist in P6coloniesList]
    file_path = os.path.join(sampledColoniesFolder, "image6.txt")
    with open(file_path, "w") as file:
        for line in sampleColonies6Line:
            wellLocationCount = wellLocationCount + 1
            file.write(' '.join(line))
            file.write(' ' + WellLocations[wellLocationCount] + '\n')

    #Write to Motor controls just x and y in one long list
            #need to add these 96 to 1 lists, Petri dishes will be ordered from least colonies to most
    totalList = []

    #only takes the 2 and 3rd value in sublist of list
    totalList1 = [sublist[1:3] for sublist in P1coloniesList]
    totalList2 = [sublist[1:3] for sublist in P2coloniesList]
    totalList3 = [sublist[1:3] for sublist in P3coloniesList]
    totalList4 = [sublist[1:3] for sublist in P4coloniesList]
    totalList5 = [sublist[1:3] for sublist in P5coloniesList]
    totalList6 = [sublist[1:3] for sublist in P6coloniesList]

    #do math to the ttoallist
    #   percentage(0.2) * 3264 *  x length across screen (15.5) / pixels(3264)
    xScale = 16
    yScale = 12

    for sublist in totalList1:
        x = float(sublist[0])
        x = x * xScale
        x = x + 66.11
        sublist[0] = x
        y = float(sublist[1])
        y = y * yScale
        y = y + 62.57
        sublist[1] = y


    for sublist in totalList2:
        x = float(sublist[0])
        x = x * xScale
        x = x + 66.11
        sublist[0] = x
        y = float(sublist[1])
        y = y * yScale
        y = y - 58.08        #TODO change to microns for final
        sublist[1] = y


    for sublist in totalList3:
        x = float(sublist[0])
        x = x * xScale
        x = x + 180.41
        sublist[0] = x
        y = float(sublist[1])
        y = y * yScale
        y = y + 62.57
        sublist[1] = y

    for sublist in totalList4:
        x = float(sublist[0])
        x = x * xScale
        x = x + 180.41
        sublist[0] = x
        y = float(sublist[1])
        y = y * yScale
        y = y - 58.08
        sublist[1] = y

    for sublist in totalList5:
        x = float(sublist[0])
        x = x * xScale
        x = x + 294.71
        sublist[0] = x
        y = float(sublist[1])
        y = y + 62.57
        y = y * yScale
        sublist[1] = y

    for sublist in totalList6:
        x = float(sublist[0])
        x = x * xScale
        x = x + 409.01
        sublist[0] = x
        y = float(sublist[1])
        y = y + 62.57
        y = y * yScale
        sublist[1] = y
    

    totalList.extend(totalList1)
    totalList.extend(totalList2)
    totalList.extend(totalList3)
    totalList.extend(totalList4)
    totalList.extend(totalList5)
    totalList.extend(totalList6)

    #print(totalList)
    return(totalList)
