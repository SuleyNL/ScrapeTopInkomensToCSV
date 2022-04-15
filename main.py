import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def downloadWNTList():
    # It takes exactly 1 minute to download all the organisation names
    organisationList = []

    # start web browser
    browser = webdriver.Chrome(ChromeDriverManager().install())

    # get source code
    browser.get("https://www.topinkomens.nl/voor-wnt-instellingen/wnt-register")
    html = browser.page_source

    # wait for page to load
    time.sleep(1)

    # get all organisations
    table = browser.find_elements_by_css_selector('tr')
    i = 0
    while i < table.__len__():
        # skip first value (title)
        if i > 0:
            name = table[i].find_elements_by_css_selector('td')[0].text.replace("\n", "")
            place = table[i].find_elements_by_css_selector('td')[1].text.replace("\n", "")
            grondslag = table[i].find_elements_by_css_selector('td')[2].text.replace("\n", "")
            minister = table[i].find_elements_by_css_selector('td')[3].text.replace("\n", "")

            organisation = clean(name) +\
                           "; " + place +\
                           "; " + grondslag +\
                           "; " + minister + \
                           "\n"

            organisationList.append(organisation)
        i = i + 1

    # Loop is over, write list to file
    print(organisationList)
    g = open("Extra/WNT-List.csv", "w+")
    for organisation in organisationList:
        g.write(organisation)
    g.close()

    # close web browser
    browser.close()


def clean(organisationName):
    # some organisations (#163) had their names double, so here that gets cleaned up.
    # the only risk with this approach is if the organisation organisationName is symmetrical like 'grootoorg'.
    # in that case we should googlesearch both the half and the full organisationName
    # estimated risk chance is < 0.1%
    middleNumber = round(len(organisationName) / 2)

    # determine both halves of the organisation organisationName
    left = organisationName[0:middleNumber]
    right = organisationName[middleNumber:-1] + organisationName[-1]

    # see if both halves are the same, if yes: take the left half
    if left == right:
        organisationName = left

    return organisationName


if __name__ == "__main__":
    downloadWNTList()
