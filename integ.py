# file System Monitoring Tool
# Mean to be run as daemon ; Monitors File directory , Calculate and list total files, Their information
# Notifies changes made into particular file, if accessed, modified, or deleted
# Alerts New File Creation
# Alerts Transfer of new File
# Calculate and stores Checksums of each file for Integrity
# Periodically checks the checksum hash value to see if integrity has been compromised.
# all these data maybe stored in csv file.

import os
import os.path
from os import path
import glob
import csv
import hashlib
import pandas as pd

def deleteFile():
    os.remove("subsequenthash.csv")

def initialCheck():
    fileexists = False
    try:
        fileexists = path.exists("firstruncheck.txt")
        if fileexists == True:
            print("Script already did initial check, Performing subsequent checks now")
            return fileexists
        else:
            print("Script running for the very first time. Performing Initial Check")
            return fileexists
    except:
        print("Some error occurred ")


def provideInfo():
    runfirst = initialCheck()
    c = 0

    # false means no record of files exist, so we run first check
    if runfirst == False:
        print("Calculating total number of files")
        print("The system contains following number of files")
        for dir, subdir, files in os.walk('D:\\wallpapercraft'):
            c += len(files)
            for x in files:
                print(x)
        nof=print("Total number of file found in the system:", c)
        with open('fsmlog.csv','a') as file:
            writer = csv.writer(file)
            #writer.writerow(['Total Files'])
            writer.writerow([c])
            f = open("firstruncheck.txt","w")
        print("calculating hashes of all files for the first time")
        fileHash()
    else:
        firsthash_exist = path.exists('firsthash.csv')
        print("Calculating total number of files")
        print("The system contains following number of files")
        for dir, subdir, files in os.walk('D:\\wallpapercraft'):
            c += len(files)
            for x in files:
                print(x)
        nof=print("Total number of file found in the system:", c)
        with open('sublog.csv','a') as file:
            writer = csv.writer(file)
            #writer.writerow(['Total Files'])
            writer.writerow([c])

        if firsthash_exist == True:
            #Calculate subsequent hashes of the files in the file system
            fileHash()


def fileHash():
    blocksize = 65536
    hasher = hashlib.md5()
    firsthash_exist = path.exists('firsthash.csv')
    if firsthash_exist == False:
        for dir , subdir, files in os.walk('D:\\wallpapercraft'):
            for x in files:
                with open(os.path.join(dir,x),'rb') as afile:
                    buf = afile.read(blocksize)
                    while len(buf) > 0:
                        hasher.update(buf)
                        buf = afile.read(blocksize)
                print(x,hasher.hexdigest())
                hashvalue = hasher.hexdigest()
                with open('firsthash.csv', 'a') as csvfile:
                    #add newline = '' if not present and program gives you trouble
                    writer = csv.writer(csvfile)
                    writer.writerow([x, hashvalue])
                csvfile.close()
    else:
        for dir , subdir, files in os.walk('D:\\wallpapercraft'):
            for x in files:
                with open(os.path.join(dir,x),'rb') as afile:
                    buf = afile.read(blocksize)
                    while len(buf) > 0:
                        hasher.update(buf)
                        buf = afile.read(blocksize)
                print(x,hasher.hexdigest())
                hashvalue = hasher.hexdigest()
                with open('subsequenthash.csv', 'a') as csvfile6:
                    #add newline ='' if any trouble
                    writer = csv.writer(csvfile6)
                    writer.writerow([x, hashvalue])
                csvfile6.close()
        print("Now checking for bad hash")
        #FIMCheck()
        IntegrityModule2()




def IntegrityModule2():
    import csv
    t1 = open('firsthash.csv', 'r').readlines()
    t2 = open('subsequenthash.csv', 'r').readlines()
    flag = True
    # t1.close()
    # t2.close()

    x = 0
    for i in t1:
        if i != t2[x]:
            flag=False
            print("bad hash found",t1[x], t2[x])
            with open('badhash.csv', 'a') as csvfile3:
                writer = csv.writer(csvfile3)
                writer.writerow([t1[x], t2[x]])
        x += 1
   #t1.close()
   #t2.close()
    os.remove("subsequenthash.csv")
    if flag == False:
        msg='Bad hash has been found. Data have been compromised, please check log for more information'
        return(msg)
    else :
        msg= 'No bad has found. File Looks all clean'
        return (msg)


def FileIntegrityModule():
    f1 = open('firsthash.csv','r')
    reader1 = csv.reader(f1, delimiter=',')
    row1 = next(reader1)
    f2 = open('subsequenthash.csv','r')
    reader2 = csv.reader(f2,  delimiter=',')
    row2 = next(reader2)
    for row1 in reader1:
        for row2 in reader2:
            if row1[1]!=row2[1]:
                print('Bad Hash value found',row1[0],row2[1])
                with open('badhash.csv','a') as csvfile3:
                    writer = csv.writer(csvfile3)
                    writer.writerow([row1[0],row2[1]])

    #f2.close()
    #deleteFile()


    print("No bad hash found")
    print("Hash check Complete")

def FIMCheck():
    firsthash_exist = path.exists('firsthash.csv')
    sub_hash_exist = path.exists('subsequenthash.csv')
    if firsthash_exist == True and sub_hash_exist == True:
        IntegrityModule2()



provideInfo()


#firsthash_exist = path.exists('firsthash.csv')
 #           if firsthash_exist == False:

#else:
#with open('subsequenthash.csv', 'a') as csvfile2:
 ##  writer.writerow

#File Integrity module isnt working right. Need bug fixes
