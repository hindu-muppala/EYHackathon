from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import os

import time

PATH = r"C:\Users\DELL\application\techathon\Dataset"
 
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--headless")  # Optional: Run without UI

# Initialize WebDriver
driver = webdriver.Chrome()
o = 1
driver.get("https://zerodha.com/varsity/modules/")

time.sleep(3)

try: 

    modules = driver.find_elements(By.CSS_SELECTOR, ".module")
    anchors = driver.find_elements(By.CLASS_NAME, "inv")

  
    for anchor in anchors[1:]:

        href2 = None

        try:
          
            href2 = anchor.get_attribute("href") 
        
            # create a folder of last '/' string of href2 as name
        except:

            print(Exception+" : "+href2)
            continue

        if href2:  
            
            # if o <= 16:
            #     o += 1
            #     continue

            driver.get(href2)
            anchorsx = driver.find_elements(By.CLASS_NAME, "inv")
            # print(href2)
            folder = None

            for x in href2.split("/")[::-1]:
             
                if x:

                    folder = x

                    break
        #    print(folder)

            os.mkdir(os.path.join(PATH, folder))

            time.sleep(3) 

            for anchorx in anchorsx:

                href = anchorx.get_attribute("href") 

                if href:  

                    print(f"Navigating to: {href}") 

                    driver.get(href)

                    folder2 = None

                    for x in href.split("/")[::-1]:
                        if x:
                            folder2 = x
                            break

                    with open(os.path.join(PATH, folder, folder2 + ".txt"), "w",  encoding="utf-8") as f:

                  #      print(href)

                        f.write(driver.find_element(By.CSS_SELECTOR, "body").text)

                        f.close()

                    time.sleep(3)
                    driver.back()
                    time.sleep(3)

            driver.back()
            time.sleep(4) 
        

  
         
except Exception as e:
    
    print(e)


finally:

    driver.quit()

# # Close the WebDriver