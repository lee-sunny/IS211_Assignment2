#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Week 2 Assignment - Python Standard Library

Part 0 - Repo created in GitHub
https://github.com/lee-sunny/IS211_Assignment2
"""

import argparse
import urllib.request
import urllib.error
import datetime
import logging

"""
Part I - Think about the Design - download the csv via URL and read the file line by line
Part II - Download the Data
takes a string called url, download contents and return it to caller
save the results to a variable called csvData
The given URL is a parameter to the script via argparse
If exception is thrown by this function will be caught in main()
"""
def downloadData(url):
    with urllib.request.urlopen(url) as webpage:
        mydata = webpage.readlines()
    return mydata

"""
Part III - Process Data
takes the contents of the file as the first parameter,
processes the file line by line,
returns a dictionary that maps a person's ID to a tuple of the form (name,birthday)
DICTIONARY NAME = personData
birthday = Datetime object, not a string
process the birthday which has the format dd/mm/yyyy and conver it to Datetime object
(Note: the time portion of the Datetime object will be 0, so you can use Date object optional)
Write an output file recording which lines in the file cannot be processed
correctly due to an improperly formatted date
Birthday might not be in correct format - typo of invalid date
log this error using the loggin module - done later
this function should get a logger using the name 'assignment2'
>>>>logger should be configured to write to a single file called "errors.log"
    can be done on a separate function or done in main program
the log msg whould be sent to the ERROR level
and of the format: "Error processing line #<linenum> for ID#<id>"
Pass csvData into processData() function and result saved as personData (which is a dictionary)
"""

def processData(mydata):
    #an empty dictionary that will later be used to lookup personData
    mydict = {}
    #processing each line of data
    counter = 0

    for line in mydata:
        #converting each line to the dictionary format with defined key and values
        converted = line.decode('ascii').strip().split(',')
        key = converted[0]
        val1 = converted[1]
        val2 = converted[2]
        counter +=1

        #setting the format of the birthday
        try:
            newval = datetime.datetime.strptime(val2, '%d/%m/%Y').date()
        except ValueError:
            logger.error('Error processing line #{} for ID#{}'.format(counter, key))
        else:
            mydict[int(key)] = (val1, newval)
    return mydict

"""
Part IV - Display/User Input
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
def displayPerson(id, personData):
    if id not in personData.keys():
        print('      The id you entered does not belong to a person on file.')
    else:
        print('      Person #{} is {} with a birthday of {}'.format(id, personData[id][0], personData[id][1]))
        


def main():
    #Use the argparse module to allow the user to send a url parameter to the script
    parser = argparse.ArgumentParser(description='my url')
    #Add the parameters
    parser.add_argument('url', help="Enter your url to download data")
    #Parse the arguments
    args = parser.parse_args()

    #url input errors
    try:
        csvData = downloadData(args.url)
    except urllib.error.HTTPError as e:
        print('   There is an HTTP error.', e.code)
    except urllib.error.URLError as e:
        print('   There is a URL error.', e.reason)
    except ValueError:
        print('   The URL provided is in invalid format.')
    else:
        try:
            personData = processData(csvData)
        except:
            print('   The application is unable to finish because the data from the url can\'t be processed.\n'
                  '   Please check that the url contains a csv file with the proper setup.')
            exit()
        else:
            #configure exit with entering zero or negative number
            running = True
            while running:
                print('   Zero or negative entry will exit the program.')
                while True:
                    try:
                        personid = int(input('   Please enter an id number to request information:'))
                    except ValueError:
                            print('      Invalid id number.')
                    else:
                        break
                if personid > 0:
                    displayPerson(personid, personData)
                else:
                    running = False


if __name__ == '__main__':
    #logger with set level to ERROR
    logger = logging.getLogger('assignment2')
    logger.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(name)s:%(message)s')
    file_handler = logging.FileHandler('errors.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    main()
