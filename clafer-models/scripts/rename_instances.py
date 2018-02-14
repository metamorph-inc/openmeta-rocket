from sys import argv
from os import listdir
def rename(dir, counter):
    if counter !== 0:
        dir = dir+counter
    for thing in listdir(dir):
        file.replace(file.split('.')[0], file.split('.')[0]counter)
rename(argv[1], argv[2])
