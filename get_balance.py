from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
import os
import datetime
import sys

# make browser run in background
# options = Options()
# options.headless = True
# driver = webdriver.Chrome(options=options)

def main():
    driver = webdriver.Chrome()

    while True:
        # generate new key pair
        os.system("make &> /dev/null")

        # read new key pair
        with open("addr") as f:
            address = f.read().strip()
        with open("priv") as f:
            private = f.read().strip()

        # get keypair balance
        driver.get("http://etherscan.io/address/"+address)
        eth_balance_xpath = '//*[@id="ContentPlaceHolder1_divSummary"]/div[1]/div[1]/div/div[2]/div[1]/div[2]'
        balance = 0.
        try:
            e = driver.find_element_by_xpath(eth_balance_xpath)
        except:
            log("log", "failed to get balance of address=%s" % address)
        else:
            balance = float(e.get_attribute("innerText").split(" ")[0])

        msg = "%s %s %.2feth" % (address, private, balance)
        log("log", msg)
        if balance > 0:
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            log("$$$", msg)
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    driver.close()

def log(path, msg):
    msg_with_time = "%s %s" % (datetime.datetime.now(), msg)
    print(msg_with_time)
    with open(path, "a") as f:
        f.write(msg_with_time+"\n")

main()
