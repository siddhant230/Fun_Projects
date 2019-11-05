from selenium import webdriver
import smtplib
from selenium.webdriver.chrome.options import Options
options = webdriver.ChromeOptions()
options.add_argument('headless')

driver=webdriver.Chrome(executable_path='C:\\Users\\tusha\\Downloads\\chromedriver.exe',options=options)
driver.get('https://www.amazon.in/Lenovo-Legion-Windows-Graphics-81V4000LIN/dp/B07XP981T8/ref=sr_1_11_sspa?keywords=laptop&qid=1571949451&smid=A14CZOWI0VEHLG&sr=8-11-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyTVJURE5NRUxCMkkwJmVuY3J5cHRlZElkPUEwNTgxMjcyMVpLMFFFQjFQMzhGWiZlbmNyeXB0ZWRBZElkPUEwMDUwMTU3UVpKTjJFNThNUEFQJndpZGdldE5hbWU9c3BfbXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==')
price=10**9
count=0
expected=60000
while True:
    value=driver.find_element_by_id('priceblock_dealprice')
    price=value.text[2:]
    price=price.split(',')
    price=int(price[0])*(10**(len(price[1])-3))+float(price[1])
    if count%100==0:
        print('CURRENT PRICE : ',price)
        if price<expected:
            s=smtplib.SMTP('smtp.gmail.com',587)
            s.starttls()
            message='Please check the message, there is a drop :'
            s.login('rsiddhant73@gmail.com','#pokemon911')
            s.sendmail('rsiddhant73@gmail.com',
                       'sidlovesml@gmail.com',msg=message)
            s.quit()
            print('SENT')
    count+=1
    print(count)
