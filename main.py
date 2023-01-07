# author:Coaixy
import time

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
send = driver.sendProcess
courses = driver.getCourseList()
user_info = driver.getUserInfo()
processes = {}
couse_open_id = ""
print("ℹ️检测到" + str(len(courses)) + "个课程")
for i in courses:
    process = courses[i]['process']
    print(i + "✨" + str(process) + "%")
course_name = input("请输入课程名:")
if course_name in courses:
    processes = driver.getProcess(course_name)
else:
    print("不存在的课程名")
    exit()
process_list = list()
print("❌以下为未完成的项目❌")
for i in processes:
    if i['percent'] < 100:
        process_list.append(i)
        print("🏅" + i['name'] + "✨" + str(i['percent']))
for i in process_list:
    module_id = i['id']
    topic_list = driver.getTopicList(course_name, module_id)
    for j in topic_list:
        cell_list = driver.getCellList(course_name, j['id'])
        for k in cell_list:
            if len(k['childNodeList']) > 0:
                for l in k['childNodeList']:
                    cell_id = l['Id']
                    cell_info = driver.getCellInfo(course_name, module_id, cell_id)
                    if cell_info['code'] != -100:
                        if cell_info['cellPercent'] < 100:
                            cell_log_id = cell_info['cellLogId']
                            audio_video_long = cell_info['audioVideoLong']
                            study_newly_time = cell_info['stuStudyNewlyTime']
                            study_newly_pic = cell_info['stuStudyNewlyPicCount']
                            page_count = cell_info['pageCount']
                            token = cell_info['guIdToken']
                            cell_type = cell_info['categoryName']
                            residue_long = audio_video_long - study_newly_time
                            print(l['cellName'])
                            if cell_type == "视频":
                                send(course_name, cell_id, cell_log_id, token, study_newly_time, 0)  # 发个包让他认识一下
                                time.sleep(5)
                                if audio_video_long < 10 or residue_long < 10:  # 长度小于十
                                    time.sleep(10)
                                    send(course_name, cell_id, cell_log_id, token, audio_video_long, 0)
                                else:
                                    length = int(residue_long / 10) + 1
                                    count = 1
                                    while count != length:
                                        send_time = study_newly_time + 10 * count
                                        if send_time >= audio_video_long:  # 过长
                                            send(course_name, cell_id, cell_log_id, token, audio_video_long, 0)
                                        response = send(course_name, cell_id, cell_log_id, token, send_time, 0)
                                        if response[1]['code'] == 1:
                                            count = count + 1
                                            print("当前进度：" + str(send_time) + "/" + str(audio_video_long))
                                        else:
                                            count = count - 0.5
                                            print(response)
                                        time.sleep(10)
                            else:
                                start = 1
                                if study_newly_pic != 0:
                                    start = study_newly_pic
                                if page_count - start > 0:
                                    for l in range(page_count - start + 1):
                                        response = send(course_name, cell_id, cell_log_id, token, 0, start)
                                        if response[1]['code'] == 1:
                                            print("当前进度：" + str(start) + "/" + str(page_count))
                                            start = start + 1
                                        else:
                                            print(response)
                                        time.sleep(10)
                    else:
                        print(cell_info)
                        print("请更新课程")
                        exit()
                    time.sleep(1)
            else:
                cell_id = k['Id']
                cell_info = driver.getCellInfo(course_name, module_id, cell_id)
                if cell_info['code'] != -100:
                    if cell_info['cellPercent'] < 100:
                        cell_log_id = cell_info['cellLogId']
                        audio_video_long = cell_info['audioVideoLong']
                        study_newly_time = cell_info['stuStudyNewlyTime']
                        study_newly_pic = cell_info['stuStudyNewlyPicCount']
                        page_count = cell_info['pageCount']
                        token = cell_info['guIdToken']
                        cell_type = cell_info['categoryName']
                        residue_long = audio_video_long - study_newly_time
                        print(k['cellName'])
                        if cell_type == "视频":
                            send(course_name, cell_id, cell_log_id, token, study_newly_time, 0)  # 发个包让他认识一下
                            time.sleep(5)
                            if audio_video_long < 10 or residue_long < 10:  # 长度小于十
                                time.sleep(10)
                                send(course_name, cell_id, cell_log_id, token, audio_video_long, 0)
                            else:
                                length = int(residue_long / 10) + 1
                                count = 1
                                while count != length:
                                    send_time = study_newly_time + 10 * count
                                    if send_time >= audio_video_long:  # 过长
                                        send(course_name, cell_id, cell_log_id, token, audio_video_long, 0)
                                    response = send(course_name, cell_id, cell_log_id, token, send_time, 0)
                                    if response[1]['code'] == 1:
                                        count = count + 1
                                        print("当前进度：" + str(send_time) + "/" + str(audio_video_long))
                                    else:
                                        count = count - 0.5
                                        print(response)
                                    time.sleep(10)
                        else:
                            start = 1
                            if study_newly_pic != 0:
                                start = study_newly_pic
                            if page_count - start > 0:
                                for l in range(page_count - start + 1):
                                    response = send(course_name, cell_id, cell_log_id, token, 0, start)
                                    if response[1]['code'] == 1:
                                        print("当前进度：" + str(start) + "/" + str(page_count))
                                        start = start + 1
                                    else:
                                        print(response)
                                    time.sleep(10)
                else:
                    print(cell_info)
                    print("请更新课程")
                    exit()
                time.sleep(1)