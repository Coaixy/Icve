import zhijiao
import os

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 "
                  "Safari/537.36 Edg/108.0.1462.54 ",
    "cookie": ""
}

cookie = ""
if os.path.exists("cookie.txt"):
    with open("cookie.txt", "r") as f:
        cookie = f.read()
    header['cookie'] = cookie
else:
    print("请将Cookie放入Cookie.txt中")
    f = open("cookie.txt", "w")
    f.close()
    exit()

driver = zhijiao.Zjy(header, cookie)
# for i in driver.getProcess("应急救护技术"):
#     print(driver.getTopicList("应急救护技术", i['id']))
# driver.test()
driver.getCellInfo("应急救护技术","eqv8ackrf5jlefgzmxes7w","eqv8ackra5toesdqjetpa")