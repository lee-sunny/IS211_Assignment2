#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Week 2 Assignment - Python Standard Library
https://github.com/lee-sunny/IS211_Assignment2
"""

import argparse
import urllib.request
import urllib.error
import datetime
import logging

"""Download the Data"""
"""takes a string called url, download contents and return it to caller
save the results to a variable called csvData
The given URL is a parameter to the script via argparse
If exception is thrown by this funstion, catch it, print out appropriate error msg and exit
"""
def downloadData(url):
    with urllib.request.urlopen(url) as webpage:
        csvData = webpage.readlines()
    return csvData

"""Process Data
    takes the contents of the file as the first parameter,
    processes the file line by line,
    returns a dictionary that maps a person's ID to a tuple of the form (name,birthday)
    DICTIONARY NAME = personData
    birthday = Datetime object, not a string
    process the birthday which has the format dd/mm/yyyy and conver it to Datetime object
    (Note: the time portion of the Datetime object will be 0, so you can use Date object optional)
"""
"""Write an output file recording which lines in the file cannot be processed
correctly due to an improperly formatted date
Birthday might not be in correct format - typo of invalid date
log this error using the loggin module
this function should get a logger using the name 'assignment2'
this logger will be configured later in the program
>>>>logger should be configured to write to a single file called "errors.log"
    can be done on a separate function or done in main program
the log msg whould be sent to the ERROR level
and of the format: "Error processing line #<linenum> for ID#<id>"
Pass csvData into processData() function and result saved as personData (which is a dictionary)
"""

def processData(csvData):
    #create an empty dictionary to add Data
    mydict = {}
    #set counter for each line
    counter = 0

    for line in csvData:
        #convert each line
        converted = line.decode('ascii').strip().split(',')

        #define key and values
        key = converted[0]
        name = converted[1]
        val2 = converted[2]

        counter +=1

        #convert birthday into datetime
        try:
            birthday = datetime.strptime(val2, '%d/%m/%Y').date()
        except ValueError:
            logger.error('Error processing line #{} for ID#{}'.format(counter, key))
        else:
            mydict[int(key)] = (name, birthday)
    return mydict

"""Display/User Input
allow a user to enter in an ID number and print out that person's info
def displayPerson
    takes in an integer called id as its first parameter
    a dictionary as its second parameter, called personData
    PURPOSE: print the name and birthday of a given user identified by the input id
    if there is not entry with the given id, print "No user found with that id"
    Otherwise format should be "Person #<id> is <name> with a birthday of <date>"
    date whould be formatted YYYY-MM-DD

a - if user enters a negative number or 0, exit program
b - if user enters positive number, user displayPerson() to attempt printing out the user
c - keep asking the user for input until they enter in a negative number of 0 to exit
"""
def displayUserInput(id, personData):
    if id not in personData.keys():
        print('\nNo user found withe that id\n')
    else:
        print('\nPerson #{} is {} with a birthday of {}\n',format(id, personData[id][0], personData[id][1]))
        


if __name__ == '__main__':

    #Use the argparse module to allow the user to send a url parameter to the script
    parser = argparse.ArgumentParser(
        description='my url'
    )
    #Add the parameters
    parser.add_argument('url', help="Enter your url to download data", type=str)
    #Parse the arguments
    args = parser.parse_args()

    #Configure error messages for invalid url
    try:
        data_download = downloadData(args.url)
    except urllib.error.HTTPError as e:
        print('\nThere is an HTTP error.\n', e.code)
    except urllib.error.URLError as e:
        print('\nThere is a URL error.\n', e.reason)
    except ValueError:
        print('\nThe URL provided is in invalid format.\n')
    else:
        try:
            personData = processData(data_download)
        except:
            print('\nThe data cannot be processed.\n')
            exit()
        else:
            running = True
            while running:
                print('Please enter a positive number to return person information')
                while True:
                    try:
                        personid = int(input('Enter below a person\'s id number: '))
                    except ValueError:
                        print('\nInvalid id number.\n')
                    else:
                        break
                if choice > 0:
                    displayUserInput(personid, personData)
                else:
                    running = False








