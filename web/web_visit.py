# Imports BeautifulSoup framework to allow us to do more high-level HTML searches
from bs4 import BeautifulSoup
# Gives us the ability to access the internet and make URL requests
import urllib.request
import urllib.error


# Setup BeautifulSoup
def soup_setup():
    soup = BeautifulSoup("", "html.parser")
    return soup


# Visit the the URL
def soup_visit(url):
    print("Accessing = " + url)
    # Open the website
    try:
        site_download = urllib.request.urlopen(url)
    # If HTTP error occurs...
    except urllib.error.HTTPError as e:
        print("---------------------------------| FAILED |-------------------------------------------")
        print("ERROR |", e)
        return "FAIL"
    # If URL error occurs...
    except urllib.error.URLError as e:
        print("---------------------------------| FAILED |-------------------------------------------")
        print("ERROR |", e)
        print("--------------------------------------------------------------------------------------")
        return "FAIL"
    # Otherwise download the website
    else:
        try:
            site_read = site_download.read().decode('utf-8')
        except:
            print("---------------------------------| FAILED |-------------------------------------------")
            print("ERROR | The Website Could Not Be Encoded")
            return "FAIL"
        else:
            print("---------------------------------| SUCCESS |------------------------------------------")
            soup = BeautifulSoup(site_read, "html.parser")
            return soup