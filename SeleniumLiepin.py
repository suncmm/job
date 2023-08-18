import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

# Initialize variable 
page_number = 0
info_list = []
info_df = pd.DataFrame()

# Set up Edge driver
opt = webdriver.EdgeOptions()   # Create setup object
opt.add_argument('--disable-gpu')
driver = webdriver.Edge(options=opt)

# Wait for element locating
driver.implicitly_wait(10)

# Open the URL
try:
    url = "https://www.liepin.com"
    # url = 'https://www.liepin.com/zhaopin/?city=410&dq=410&pubTime=&currentPage=4&pageSize=40&key=%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E5%A4%84%E7%90%86%E5%B7%A5%E7%A8%8B%E5%B8%88&suggestTag=&workYearCode=0&compId=&compName=&compTag=&industry=&salary=&jobKind=&compScale=&compKind=&compStage=&eduLevel=&ckId=b3s56cvghczo7e2349k7nr4aon8aiwu9&scene=page&skId=gxwlni0hzx0v6ow5mfg48hf37slztum9&fkId=gxwlni0hzx0v6ow5mfg48hf37slztum9&sfrom=search_job_pc&suggestId='
    driver.get(url)

    # Type and search job position
    # Locate the `input` element and entry key word
    driver.find_element(By.XPATH, "//input[@placeholder='搜索职位/公司/内容关键词']").send_keys("自然语言处理工程师")
    # Locate the search button element and click the button
    driver.find_element(By.XPATH, "//span[text()='搜索']").click()

    # Switch to recruitment page
    driver.switch_to.window(driver.window_handles[-1])

    while True:
        tmp_data_list = []
        tmp_data_df = pd.DataFrame()

        # Wait for page loading to be completed
        # while not driver.execute_script("document.readyState == 'complete'"):
        #     time.sleep(1)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='lp-search-job-box']/div[3]/section[1]/div[1]/div[40]")))
        eles = driver.find_elements(By.XPATH, "//div[@id='lp-search-job-box']/div[3]/section[1]/div[1]/div")

        # Extracte job information
        for ele in eles:
            tmp_data_dict = dict()
            try:
                tmp_data_dict['position'] = ele.find_element(By.XPATH, "./div/div[1]/div/a/div[1]/div/div[1]").text
            except NoSuchElementException:
                tmp_data_dict['position'] = 'N/A'  
            try:
                tmp_data_dict['city'] = ele.find_element(By.XPATH, "./div/div[1]/div/a/div[1]/div/div[2]/span[2]").text  
            except NoSuchElementException:
                tmp_data_dict['city'] = 'N/A'  
            try:
                tmp_data_dict['payment'] = ele.find_element(By.XPATH, "./div/div[1]/div/a/div[1]/span[@class='jsx-2693574896 job-salary']").text
            except NoSuchElementException:
                tmp_data_dict['payment'] = 'N/A'  
            try:
                tmp_data_dict['enterprise'] = ele.find_element(By.XPATH, "./div/div[1]/div/div/div/span").text
            except NoSuchElementException:
                tmp_data_dict['enterprise'] = 'N/A'  
            try:
                tmp_data_dict['requirement-list'] = ele.find_element(By.XPATH, "./div/div[1]/div/a/div[2]").text
            except NoSuchElementException:
                tmp_data_dict['requirement-list'] = 'N/A'  
            try:
                tmp_data_dict['CPprofile-list'] = ele.find_element(By.XPATH, "./div/div[1]/div/div/div/div[2]").text
            except NoSuchElementException:
                tmp_data_dict['CPprofile-list'] = 'N/A'  

            # # Wait for element to be visible and scroll to the visible area
            # driver.execute_script('arguments[0].scrollIntoView();', ele)
            # ele = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(ele))
            
            # Open job information detail page
            ele.click()
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(60)

            # Extract job information detail
            # Job description
            try:
                tmp_data_dict['job-detail'] = driver.find_element(By.XPATH, "//dd[@data-selector='job-intro-content']").text   # responsibilities and requirement-detail
            except NoSuchElementException:
                tmp_data_dict['job-detail'] = 'N/A'  
            # Profile-detail
            try:
                tmp_data_dict['enterprise-detail'] = driver.find_element(By.XPATH, "//div[@class='paragraph-box']//div[1]").text   # enterprise profile-detail
            except NoSuchElementException:
                tmp_data_dict['enterprise-detail'] = 'N/A'  
            tmp_data_list.append(tmp_data_dict)
            info_list.append(tmp_data_dict)

            # Return overview page
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])
            # time.sleep(5)

        # Save current page data
        with open(f'tmp_data_dir/{page_number}.json', 'w') as ftd:
            json.dump(tmp_data_list, ftd, ensure_ascii=False)
        tdf = tmp_data_df.from_records(tmp_data_list)
        tdf.to_csv(f'tmp_data_dir/{page_number}.csv', index=False)

        # Go to next page
        next_button = driver.find_element(By.XPATH, "//li[@title='Next Page']//button[1]")
        if next_button.get_attribute('disabled') == 'true':
            break
        else:
            next_button.click()
            page_number += 1
            time.sleep(60)
        
    # Close the browser
    driver.quit()

# Capture exceptions and exit the browser
except Exception as e:
    print(e)
    driver.quit()


# Save information data
with open('job1.json', 'w') as f:
    json.dump(info_list, f, ensure_ascii=False)

df = info_df.from_records(info_list)
df.to_csv('job1.csv', index=False)
