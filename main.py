#importing required modules.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import random
import time
def main():
    counter=0
    #Taking input of the username who's tweet is to be retweeted.
    print("Enter the username who's tweet you want to retweet:",end="")
    USERNAME_TO_SEARCH=input().strip()
    print("Re-enter the username:",end="")
    USERNAME_RE=input().strip()
    if USERNAME_TO_SEARCH.lower()==USERNAME_RE.lower():
    #reading csv file and forming a data frame.
        file=open('Email.csv','r+')
        df = pd.read_csv(file)
        row_count=len(df["Username"])
        row_extract=random.randint(0,row_count-1)
        #main while loop.
        while counter<row_count:
            USER_CHECK=""
            if df["Checkbox"][row_extract].lower()=='no': # condition checking if the username is already used for the process of retweet
                #taking username and password to login in twitter
                USERNAME=df["Username"][row_extract]
                PASSWORD=df["Password"][row_extract]
                #opens chrome and surf to twitter login page 
                chrome_driver_path="./chromedriver.exe"
                driver=webdriver.Chrome(chrome_driver_path)
                driver.maximize_window()
                login_url='https://twitter.com/'
                driver.get(login_url)
                driver.implicitly_wait(2)
                try:
                    #locating login button
                    login=driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a')
                    time.sleep(2.8)
                    login.send_keys(Keys.RETURN)
                    #locating username field and take input
                    input_email=driver.find_element(By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
                    time.sleep(1.2)
                    for i in USERNAME:
                        input_email.send_keys(i)
                        time.sleep(0.1)
                    input_email.send_keys(Keys.RETURN)
                    #locating password field and take input
                    input_password=driver.find_element(By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
                    time.sleep(0.8)
                    for i in PASSWORD:
                        input_password.send_keys(i)
                        time.sleep(0.1)
                    input_password.send_keys(Keys.RETURN)
                    #navigate explore button to search for username 
                    search=driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[2]')
                    time.sleep(0.9)
                    search.send_keys(Keys.RETURN)
                    search_bar=driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')
                    time.sleep(1.5)
                    #taking username input in searchbar
                    for i in USERNAME_TO_SEARCH:
                        search_bar.send_keys(i)
                        time.sleep(0.1)
                    search_bar.send_keys(Keys.RETURN)
                    j=1
                    time.sleep(2)
                    people=driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[3]/a')
                    people.send_keys(Keys.RETURN)
                    time.sleep(2)
                    while USER_CHECK.lower()!=USERNAME_TO_SEARCH.lower():
                        try:
                            user=driver.find_element(By.XPATH,f'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/section/div/div/div[{j}]/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div')
                            USER_CHECK=user.text[1:]
                            j=j+1
                        except:
                            j=j+1
                    user.click()
                    time.sleep(1)
                    # navigating retweet option and confirm to retweet option 
                    retweet=driver.find_element(By.CSS_SELECTOR,'.css-18t94o4[data-testid ="retweet"]')
                    time.sleep(1.2)
                    retweet.send_keys(Keys.RETURN)
                    time.sleep(1)
                    #retweet confirmation
                    driver.find_element(By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/div').click()
                    time.sleep(1.9)
                    #log out process
                    logout=driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[2]/div/div')
                    time.sleep(1.1) 
                    logout.send_keys(Keys.RETURN)
                    time.sleep(0.8)
                    logout_=driver.find_element(By.XPATH,'//*[@id="layers"]/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div/a[2]')
                    time.sleep(1)
                    logout_.click()
                    time.sleep(1.8)
                    logout_confirmation=driver.find_element(By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]')
                    time.sleep(1)
                    logout_confirmation.send_keys(Keys.RETURN)
                    #updating csv that the user has retweeted
                    df.loc[row_extract, 'Checkbox']='Yes'
                    df.to_csv("Email.csv", index=False)
                    counter=counter+1
                    driver.close()
                    if counter<row_count:
                        time.sleep(120)
                except:
                        driver.close()
            else:
                row_extract=random.randint(0,row_count-1)
        #again setting the checkbox of all username to 'no' so that the program can be used again
        for i in range (row_count):
            df.loc[i, 'Checkbox']='No'
            df.to_csv("Email.csv", index=False)
    else:
        print('''Sorry username does not match''')
        input("Press ENTER to restart")
        main()
main()
