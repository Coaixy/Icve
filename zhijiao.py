import json

import requests


class Zjy:
    header = {}
    cookie = ""
    course_list = list()

    def __init__(self, header, cookie):
        self.header = header
        self.cookie = cookie

    def getUserInfo(self):
        data = self.requestResult("https://zjy2.icve.com.cn/api/student/Studio/index", "")
        result = {
            'schoolId': data['schoolId'],
            'disPlayName': data['disPlayName'],
            'courseNum': data['statData']['myCourseCount'],
            'homeworkNum': data['statData']['myHomeworkCount'],
            'examNum': data['statData']['myExamCount'],
        }
        return result

    def getCourseList(self):
        data = self.requestResult("https://zjy2.icve.com.cn/api/student/learning/getLearnningCourseList", "")[
            'courseList']
        length = len(data)
        result = {}
        for i in range(length):
            course_name = data[i]['courseName']
            result[course_name] = dict()
            result[course_name]['id'] = data[i]['Id']
            result[course_name]['id'] = data[i]['Id']
            result[course_name]['courseOpenId'] = data[i]['courseOpenId']
            result[course_name]['openClassId'] = data[i]['openClassId']
            result[course_name]['process'] = data[i]['process']
        self.course_list = result
        return result

    def getProcess(self, course_name):
        if not self.course_list:
            self.getCourseList()
        all_process = self.course_list[course_name]['process']
        data = {
            "courseOpenId": self.course_list[course_name]['courseOpenId'],
            "openClassId": self.course_list[course_name]['openClassId']
        }
        response = self.requestResult("https://zjy2.icve.com.cn/api/study/process/getProcessList", data)
        temp_data = response['progress']['moduleList']
        result = list()
        for i in temp_data:
            result.append(i)
        result.append(all_process)
        return result


    def requestResult(self, url, data):
        response = requests.post(url, headers=self.header, data=data)
        return response.json()
