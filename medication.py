#coding:utf-8
import web
import json
import sqlite3
import time
import traceback
import sys
import urllib2
reload(sys)
sys.setdefaultencoding("utf8")

class Medication:
    
    CODE_ERROR= -1
    CODE_OK = 0
    
    #db path
    db_path = "/home/work/www/wechat_mini_program/data/medication.db"
    
    def __init__(self):
        #初始化数据库
        self.connect = sqlite3.connect(self.db_path, 10)
        self.connect.row_factory = self.resultDictFactory
        self.connect.text_factory = str
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.cursor.close()
        
    def GET(self,name):
        return self.POST(name)

    def POST(self,name):
        data = web.input() 
        if name == "post":
            return self.insert(data)
        elif name == "delete":
            return self.delete(data)
        elif name == "put":
            return self.update(data)
        elif name == "get":
            return self.get(data)
        elif name == "getlist":
            return self.getList(data)
        elif name == "get_session_data":
            return self.getSessionByCode(data)
        else:
            return self.default()

    def insert(self, data):
        is_sucess = 0
        if not data.has_key("wx_id"):
            return self.resultStruct("", -1, "wx_id param error")
        if not data.has_key("symptom"):
            return self.resultStruct("", -1, "symptom param error")
        if not data.has_key("drug"):
            return self.resultStruct("", -1, "drug param error")

        try:
            wx_id = data["wx_id"]
            symptom = data["symptom"]
            drug = data["drug"]
            hospital = data["hospital"]
            status = 1
            create_time = int(time.time())
            if not hospital:
                hospital = ""
            sql = "insert into medication values (null, '%s', '%s', '%s', %s, '%s', %s)" % (wx_id, hospital, symptom, status, drug, create_time)
            sql = sql.encode("utf8")
            self.cursor.execute(sql)
            self.connect.commit()
            is_sucess = 1
        except Exception as e:
            self.connect.rollback() 
            traceback.print_exc(file=open("./medication.log", "a"))
        if is_sucess == 1:
            return self.resultStruct()
        else:
            return self.resultStruct("", -1, "fail")

    def delete(self,data):
        if not data.has_key("wx_id"):
            return self.resultStruct("", -1, "wx_id param error")
        if not data.has_key("medication_id"):
            return self.resultStruct("", -1, "id param error")
        is_sucess = 0
        try:
            wx_id = data["wx_id"]
            medication_id = data["medication_id"]
            sql = "update medication set status = 0 where id = %s and wx_id = '%s'" % (medication_id, wx_id)
            sql = sql.encode("utf8")
            self.cursor.execute(sql)
            self.connect.commit()
            is_sucess = 1
        except Exception as e:
            self.connect.rollback() 
            traceback.print_exc(file=open("./medication.log", "a"))
        if is_sucess == 1:
            return self.resultStruct()
        else:
            return self.resultStruct("", -1, "fail")

    def update(self, data):
        if not data.has_key("wx_id"):
            return self.resultStruct("", -1, "wx_id param error")
        if not data.has_key("medication_id"):
            return self.resultStruct("", -1, "id param error")
        if not data.has_key("symptom"):
            return self.resultStruct("", -1, "symptom param error")
        if not data.has_key("drug"):
            return self.resultStruct("", -1, "drug param error")
        if not data.has_key("hospital"):
            return self.resultStruct("", -1, "hospital param error")
        is_sucess = 0
        try:
            wx_id = data["wx_id"]
            medication_id = data["medication_id"]
            symptom = data["symptom"]
            drug = data["drug"]
            hospital = data["hospital"]
            sql = "update medication set symptom = '%s', drug = '%s', hospital = '%s' where id = %s and wx_id = '%s'" % (symptom, drug, hospital, medication_id, wx_id)
            sql = sql.encode("utf8")
            self.cursor.execute(sql)
            self.connect.commit()
            is_sucess = 1
        except Exception as e:
            self.connect.rollback() 
            traceback.print_exc(file=open("./medication.log", "a"))
        if is_sucess == 1:
            return self.resultStruct()
        else:
            return self.resultStruct("", -1, "fail")

    def get(self, data):
        if not data.has_key("wx_id"):
            return self.resultStruct("", -1, "wx_id param error")
        if not data.has_key("medication_id"):
            return self.resultStruct("", -1, "id param error")
        is_sucess = 0
        try:
            wx_id = data["wx_id"]
            medication_id = data["medication_id"]
            sql = "select * from medication where status = 1 and id = %s and wx_id = '%s'" % (medication_id, wx_id)
            sql = sql.encode("utf8")
            self.cursor.execute(sql)
            med_data = self.cursor.fetchone()
            is_sucess = 1
        except Exception as e:
            traceback.print_exc(file=open("./medication.log", "a"))
        if is_sucess == 1:
            return self.resultStruct(med_data)
        else:
            return self.resultStruct("", -1, "fail")

    def getList(self, data):
        if not data.has_key("wx_id"):
            return self.resultStruct("", -1, "wx_id param error")
        is_sucess = 0
        try:
            wx_id = data["wx_id"]
            offset = 0
            size = 5
            if data.has_key("offset"):
                offset = data["offset"]
            if data.has_key("size"):
                size = data["size"]
            sql = "select * from medication where status = 1 and wx_id = '%s' order by create_time limit %s offset %s " % (wx_id, size, offset)
            sql = sql.encode("utf8")
            self.cursor.execute(sql)
            med_data = self.cursor.fetchall()
            is_sucess = 1
        except Exception as e:
            traceback.print_exc(file=open("./medication.log", "a"))
        if is_sucess == 1:
            return self.resultStruct(med_data)
        else:
            return self.resultStruct("", -1, "fail")
        
    def default(self):
        return "hello world"

    def resultStruct(self, data="", code=0, msg="sucess"):
        result = {"data":data, "code":code, "msg":msg} 
        return json.dumps(result, ensure_ascii=False) 

    def resultDictFactory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def getSessionByCode(self, data):
        if not data.has_key("js_code"):
            return self.resultStruct("", -1, "js_code param error")

        JSCODE = data["js_code"]
        response = urllib2.urlopen("https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" % (APPID, SECRET, JSCODE))
        code = response.code
        data = response.read()
        jsondata = json.loads(data) 
        if code == 200:
            return self.resultStruct(jsondata)
        else:
            return self.resultStruct(jsondata, -1, "fail")



