from selenium import webdriver

driver=webdriver.Chrome()
driver.get('https://web.whatsapp.com/')
num_of_person=int(input('How many people you want to send message : '))
name_to_send=[]
for i in range(num_of_person):
    name_to_send.append(input('Enter the name of person or group you want to send the message : '))
count=int(input('how many times do you want to send the message : '))
message=input('Enter the message : ')

for name in name_to_send:
    user=driver.find_element_by_xpath('//span[@title="{}"]'.format(name))
    user.click()

    msg_box=driver.find_element_by_class_name('_13mgZ')

    for i in range(count):
        print(i)
        msg_box.send_keys(message)
        button=driver.find_element_by_class_name('_3M-N-')
        button.click()

