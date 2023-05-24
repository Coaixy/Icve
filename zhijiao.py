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
            result[course_name]['moduleId'] = ""
        self.course_list = result
        return result

    def getTopicList(self, course_name, moduleId):
        url = "https://zjy2.icve.com.cn/api/study/process/getTopicByModuleId"
        if not self.course_list:
            self.getCourseList()
        data = {
            "courseOpenId": self.course_list[course_name]['courseOpenId'],
            "moduleId": moduleId
        }
        response = self.requestResult(url, data)
        return response['topicList']

    def getClassList(self, course_name):
        url = "https://zjy2.icve.com.cn/api/common/courseLoad/getStuStudyClassList"
        if not self.course_list:
            self.getCourseList()
        data = {
            "courseOpenId": self.course_list[course_name]['courseOpenId'],
            "openClassId": self.course_list[course_name]['openClassId']
        }
        response = self.requestResult(url, data)
        return response

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
        return result

    def getCellList(self, course_name, topic_id):
        if not self.course_list:
            self.getCourseList()
        url = "https://zjy2.icve.com.cn/api/study/process/getCellByTopicId"
        data = {
            "courseOpenId": self.course_list[course_name]["courseOpenId"],
            "openClassId": self.course_list[course_name]["openClassId"],
            "topicId": topic_id
        }
        response = self.requestResult(url, data)
        return response['cellList']

    def change(self, course_name, module_id, cell_id,cell_name):
        if not self.course_list:
            self.getCourseList()
        url = "https://zjy2.icve.com.cn/api/common/Directory/changeStuStudyProcessCellData"
        data = {
            "courseOpenId": self.course_list[course_name]["courseOpenId"],
            "openClassId": self.course_list[course_name]["openClassId"],
            "moduleId": module_id,
            "cellId": cell_id,
            "cellName": cell_name
        }
        response = self.requestResult(url, data)
        return response

    def getCellInfo(self, course_name, module_id, cell_id):
        if not self.course_list:
            self.getCourseList()
        url = "https://zjy2.icve.com.cn/api/common/Directory/viewDirectory"
        data = {
            "courseOpenId": self.course_list[course_name]["courseOpenId"],
            "openClassId": self.course_list[course_name]["openClassId"],
            "cellId": cell_id,
            "moduleId": module_id
        }
        response = self.requestResult(url, data)
        # cellId 和 cellLogId 都在
        return response

    def sendProcess(self, course_name, cell_id, cell_log_id, token, time, num):
        if not self.course_list:
            self.getCourseList()
        url = "https://zjy2.icve.com.cn/api/common/Directory/stuProcessCellLog"
        data = {
            "courseOpenId": self.course_list[course_name]["courseOpenId"],
            "openClassId": self.course_list[course_name]["openClassId"],
            "cellId": cell_id,
            "cellLogId": cell_log_id,
            "studyNewlyTime": time,
            "studyNewlyPicNum": num,
            "token": token
        }
        response = self.requestResult(url, data)
        return [data,response]

    def requestResult(self, url, data):
        response = requests.post(url, headers=self.header, data=data)
        return response.json()

    def test(self):
        url = "https://zjy2.icve.com.cn/api/common/Directory/viewDirectory"
        data = {
            "courseOpenId": "4ov5ackr05fo5cxjfv82dg",
            "openClassId": "nm4aawv65dpvrgorr3kgq",
            "cellId": "eqv8ackra5toesdqjetpa",
            "moduleId": "eqv8ackrf5jlefgzmxes7w"
        }
        print(self.requestResult(url, data))
