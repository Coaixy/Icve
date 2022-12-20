import requests
import zhijiao

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 "
                  "Safari/537.36 Edg/108.0.1462.54 ",
    "cookie": ""
}

cookie = ""
with open("cookie.txt", "r") as f:
    cookie = f.read()
header['cookie'] = cookie

driver = zhijiao.Zjy(header, cookie)
print(driver.getProcess("应急救护技术"))
