__all__ = [
    "makeSeleniumSoup",
    "makeSoup",
    "futureDate",
    "myStrptime"
]

import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent   
import requests
# from selenium import webdriver
from playwright.sync_api import sync_playwright
from time import sleep
import socket

userAgentString = str(UserAgent(os="Mac OS X").chrome)
TODAY = datetime.date.today()

def makeSoup(url, parser='html.parser', verify=True):
    headers = {'User-Agent': userAgentString}
    SITE = requests.get(url, headers=headers, verify=verify)
    return BeautifulSoup(SITE.content, parser)

# def makeSeleniumSoup(url, sleepTime=0, scripts=[]):
#     opt = webdriver.ChromeOptions()
#     opt.add_argument("--headless")
#     opt.add_argument('--blink-settings=imagesEnabled=false')
#     opt.add_argument("--no-sandbox")
#     opt.add_argument("--disable-gpu")
#     opt.add_argument('--disable-dev-shm-usage')
#     opt.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
#     opt.add_argument("user-agent=" + userAgentString)
#     driver = webdriver.Chrome(options=opt)
#     tz_params = {'timezoneId': 'Europe/Amsterdam'}
#     driver.execute_cdp_cmd('Emulation.setTimezoneOverride', tz_params)

#     driver.get(url)
#     sleep(sleepTime)
#     for script in scripts:
#         driver.execute_script(script)
#         sleep(sleepTime)
#     html = driver.page_source
#     driver.quit()
#     return BeautifulSoup(html, 'html.parser')

def makeSeleniumSoup(url, sleepTime=0, scripts=[], waitFor = None):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path = None if "mac" in socket.gethostname().lower() else "/usr/bin/chromium",
            args = [
                "--headless",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage"
            ],
            timeout = 180000,
        )
        context = browser.new_context(user_agent=userAgentString, timezone_id='Europe/Amsterdam')
        page = context.new_page()


        # page.on("request", lambda request: print( 
        # 	">>", request.method, request.url,
        #     request.resource_type)) 
        # page.on("response", lambda response: print( 
    	#     "<<", response.status, response.url)) 

        # excluded_resource_types = ["stylesheet", "image", "font"] 
        # def block_aggressively(route): 
        #     if (route.request.resource_type in excluded_resource_types): 
        #         route.abort() 
        #     else: 
        #         route.continue_() 
        # page.route("**/*", block_aggressively) 


        page.goto(url, timeout=180000)
        if waitFor:
            page.wait_for_selector(waitFor, timeout=18000)
        sleep(sleepTime)
        for script in scripts:
            page.evaluate(script)
            sleep(sleepTime)
        html = page.content()
        context.close()
        browser.close()
    return BeautifulSoup(html, 'html.parser')

def futureDate(date: datetime.date, daysInPast = 0, failOnFarFuture = True):
    TODAY = datetime.date.today()
    if date.month == 2 and date.day == 29:
        increment = 4
    else:
        increment = 1
    while (date - TODAY).days < -daysInPast:
        date = date.replace(year = date.year + increment)
    if failOnFarFuture and (date - TODAY).days > 30 * 9:
        raise Exception("FutureDate: too far away? " + date.isoformat())
    return date

dag_kort = [
    ['ma', 'Mon'],
    ['di', 'Tue'],
    ['wo', 'Wed'],
    ['do', 'Thu'],
    ['vr', 'Fri'],
    ['za', 'Sat'],
    ['zo', 'Sun'],
]

dag_lang = [
    ['maandag', 'Monday'],
    ['dinsdag', 'Tuesday'],
    ['woensdag', 'Wednesday'],
    ['donderdag', 'Thursday'],
    ['vrijdag', 'Friday'],
    ['zaterdag', 'Saturday'],
    ['zondag', 'Sunday'],
]

maand_kort = [
    ['jan', 'Jan'],
    ['feb', 'Feb'],
    ['mrt', 'Mar'],
    ['apr', 'Apr'],
    ['mei', 'May'],
    ['jun', 'Jun'],
    ['jul', 'Jul'],
    ['aug', 'Aug'],
    ['sep', 'Sep'],
    ['okt', 'Oct'],
    ['nov', 'Nov'],
    ['dec', 'Dec'],
]

maand_lang = [
    ['januari', 'January'],
    ['februari', 'February'],
    ['maart', 'March'],
    ['april', 'April'],
    ['mei', 'May'],
    ['juni', 'June'],
    ['juli', 'July'],
    ['augustus', 'August'],
    ['september', 'September'],
    ['oktober', 'October'],
    ['november', 'November'],
    ['december', 'December'],
]

def myStrptime(date, format):
    try:
        return datetime.datetime.strptime(date, format)
    except:
        pass
    date = date.lower()
    if '%A' in format:
        for dag, day in dag_lang:
            date = date.replace(dag, day.upper())
    if '%B' in format:
        for dag, day in maand_lang:
            date = date.replace(dag, day.upper())
    if '%a' in format:
        for dag, day in dag_kort:
            date = date.replace(dag, day.upper())
    if '%b' in format:
        for dag, day in maand_kort:
            date = date.replace(dag, day.upper())
    return datetime.datetime.strptime(date, format)