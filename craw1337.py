#!/usr/bin/python

from datetime import datetime
from termcolor import colored
import requests
import sys
from bs4 import BeautifulSoup

foundLinks = []
foundInternal = []
foundExternal = []


def welcome_message():  # Prints the welcome message
    print(colored("Welcome to Craw1337 V1\n"
                  "Created with love by MoroccanTea\n"
                  "https://github.com/MoroccanTea\n", attrs=['bold']))


def print_help():  # Prints the help message
    print("HELP :\n"
          "     -h | --help | Prints this message.\n"
          "     -d | --domain [Domain to test] | Start crawling a domain.\n"
          "     -o | --ofile [File path or name] | Write the output to a file.\n"
          "USAGE :\n"
          "     Craw1337.py -d https://google.com\n"
          "     Craw1337.py -d https://google.com -o outfile.csv\n")


def print_error():  # Prints the error message
    print(colored("ERROR: Wrong input !\n", "red"))
    print_help()


def showStats(nbrInternalFound, nbrExternalFound, startTime):  # Shows crawl stats in the end
    totalNbr = len(foundLinks)
    time_elapsed = datetime.now() - startTime
    print(colored("Craw1337 scan finished !\n"
                  "Crawled " + str(totalNbr) + " links, \n"
                                               "Of which, Craw1337 found " + str(
        len(nbrInternalFound)) + " internal link(s) and " + str(len(nbrExternalFound)) + " external link(s),\n"
                                                                                         "Time elapsed {}:".format(
        time_elapsed).split('.')[0]
                  , attrs=['bold']))


def read_args():  # Read arguments inputs
    global domain
    global domainHTML
    global output_path
    if len(sys.argv) == 1:
        print_help()
        exit()
    elif len(sys.argv) == 2:
        if sys.argv[1] == '' or sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print_help()
            exit()
    elif len(sys.argv) == 3:
        if sys.argv[1] == '-d' or sys.argv[1] == '--domain':
            domain = sys.argv[2]
            domainHTML = str(BeautifulSoup(requests.get(domain).content, "html.parser"))
    elif len(sys.argv) == 4:
        if sys.argv[1] == '-d' or sys.argv[1] == '--domain' and sys.argv[3] == '-o' or sys.argv[3] == '--ofile':
            domain = sys.argv[2]
            domainHTML = str(BeautifulSoup(requests.get(domain).content, "html.parser"))
            output_path = sys.argv[4]
    else:
        print_error()


def crawl(domainHTML):  # Crawls lol
    href = domainHTML.find("a href")
    if href == -1:
        return None, 0
    openQuote = domainHTML.find('"', href)
    closeQuote = domainHTML.find('"', openQuote + 1)
    domain = domainHTML[openQuote + 1: closeQuote]
    return domain, closeQuote


def main():  # Runs the script
    global domainHTML
    global foundLinks
    welcome_message()
    read_args()
    start = datetime.now()
    crawl(domainHTML)
    while True:
        domain, n = crawl(domainHTML)
        domainHTML = domainHTML[n:]
        if domain:
            internalOrExternal(domain)
            foundLinks.append(domain)
        else:
            break
    showStats(foundInternal, foundExternal, start)
    if len(foundExternal) > 0:
        moreCrawl()
    else:
        exit()


def internalOrExternal(link):  # Checks if found link is internal or external
    if domain in link:
        print(colored("[+] Found external link: " + link, "green", attrs=['bold']))
        foundExternal.append(link)
    elif link != "":
        print(colored("[+] FOUND internal link: " + link, "yellow", attrs=['bold']))
        foundInternal.append(link)


def moreCrawl():  # Asks to run script on found external links
    global domain
    choice = input(
        colored("Craw1337 found " + str(len(foundExternal)) + " link(s) would you like to crawl them too ? [Y/n] ",
                attrs=['bold']))
    if choice == "" or choice == "Y" or choice == "y":
        domain = foundExternal[0]
        foundExternal.clear()
        foundInternal.clear()
        foundLinks.clear()
        main()
    elif choice == "n" or choice == "N":
        print(colored("Thank you for using Craw1337 !", attrs=['bold']))
        exit()
    else:
        print(colored("Wrong input !", "red", attrs=['bold']))
        moreCrawl()


if __name__ == "__main__":
    main()

# TODO: Add output
