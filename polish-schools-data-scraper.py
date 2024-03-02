# contact information scraper for polish schools around the world
# @shine.exe 2024

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


def choose_country(country):
    # finding filtering by country option on page
    filter_button = driver.find_element(By.CLASS_NAME, "well")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", filter_button)

    # selecting chosen country in filter form
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "form-control")))
    select_element = driver.find_element(By.ID, "filter-1578")
    select = Select(select_element)
    select.select_by_value(country)

    # accepting filter settings
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-primary btn-sm"]')))
    driver.find_element(By.XPATH, '//button[@class="btn btn-primary btn-sm"]').click()


# counting how many pages of results there are in search output
def count_pages():
    pages_n = 0
    page_container = driver.find_element(By.XPATH, "//div[@class='well'][2]")
    driver.execute_script("arguments[0].scrollIntoView();", page_container)
    pages_n = len(driver.find_elements(By.XPATH, "//div[@class='well'][2]/a"))
    print('Pages found: ' + str(pages_n))
    return pages_n


# reading data for selected school and printing it to corresponding file
def get_school_info():
    time.sleep(5)
    # waiting for table to load and finding it
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='col-md-12'][2]/div[1]")))
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH, "//div[@class='col-md-12'][2]/div[1]"))
    info_table = driver.find_element(By.XPATH, "//div[@class='col-md-12'][2]/div[1]/table/tbody")
    driver.execute_script("arguments[0].scrollIntoView();", info_table)

    # selecting data from table
    rows = info_table.find_elements(By.CSS_SELECTOR, 'tr')
    country = rows[4].find_elements(By.CSS_SELECTOR, 'td')[1].text
    filename = './results/' + country + '.txt'
    city = rows[3].find_elements(By.CSS_SELECTOR, 'td')[1].text
    email = rows[12].find_elements(By.CSS_SELECTOR, 'td')[1].text

    # printing data for chosen school to a separate country file
    school_log = city + ';' + email
    country_file = open(filename, 'a', encoding="utf-8")
    print(school_log, file=country_file)
    country_file.close()

    # printing data for chosen school to a file containing data from all countries
    school_log = country + ';' + school_log
    result_file = open('./results/result.txt', 'a', encoding="utf-8")
    print(school_log, file=result_file)
    result_file.close()

    driver.back()
    time.sleep(0.5)


# iterating through contents of the selected page
def scrape_from_page(page_number):
    # changing to chosen result page
    if page_number > 1:
        page_url = "https://www.orpeg.pl/db/web/database/115?queryString=&page=" + str(page_number)
        driver.get(page_url)
        time.sleep(5)

    # waiting for table to load and finding it
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table[@id='databaseTable']")))
    info_table = driver.find_element(By.XPATH, "//table[@id='databaseTable']/tbody")
    driver.execute_script("arguments[0].scrollIntoView();", info_table)

    number_of_rows = len(info_table.find_elements(By.CSS_SELECTOR, "tr"))
    if number_of_rows > 0:
        # iterating through all schools in the table
        for school_x in range(number_of_rows):
            info_table = driver.find_element(By.XPATH, "//table[@id='databaseTable']/tbody")
            schools = info_table.find_elements(By.CSS_SELECTOR, "tr")
            print(school_x+1)
            more_info = schools[school_x].find_elements(By.CSS_SELECTOR, "td")[11]
            driver.execute_script("arguments[0].scrollIntoView();", more_info)
            more_info.find_element(By.CSS_SELECTOR, "i").click()
            time.sleep(0.5)
            get_school_info()


if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.maximize_window()

    base_url = 'http://orpeg.pl/db/web/database/baza-danych-szkol'  # database website address
    driver.get(base_url)
    time.sleep(5)

    # use following to extract data from only one country
    # country_name = "Niemcy"   # example country name in polish
    # choose_country(country_name)

    # iterating through all the result pages
    pages_number = count_pages()
    if pages_number > 1:
        for x in range(pages_number):
            print("PAGE " + str(x + 1))
            scrape_from_page(x + 1)

    print("SUCCESS")
    time.sleep(10)
    driver.quit()
