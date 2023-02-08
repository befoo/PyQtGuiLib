# -*- coding:utf-8 -*-
# @time:2023/2/813:18
# @author:LX
# @file:styleAnalysis.py
# @software:PyCharm

'''

    QSS 样式解析器
'''

import re

def dictTostr(qss_dict)->str:
    combination = ""
    for selector, attribute in qss_dict.items():
        combination += selector + "{\n"
        for attrk, attrv in attribute.items():
            combination += "%s:%s;\n" % (attrk, attrv)
        combination += "}\n"
    return combination

class Qss:
    def __init__(self,qss:str,parent=None):
        self.__parent =parent
        self._qss_str = qss
        self._qss_dict = dict()
        self._qss_header = ""
        self._qss_body = ""

        self.Init()

    def Init(self):
        header = re.findall(".*{", self._qss_str, re.DOTALL)
        if header:
            self._qss_header = header[0].replace("\n", "").replace("{", "")
        else:
            raise TypeError("Syntax error, missing {")

        # ---
        body = re.findall(r"{(.*)}", self._qss_str, re.DOTALL)
        if body:
            self._qss_body = body[0].strip()

        self._qss_dict = {self.header(): self.bodyToDict()}

    def header(self)->str:
        return self._qss_header

    def headerSubdivision(self)->list:
        return self.header().split(",")

    def body(self)->str:
        return self._qss_body

    def bodySubdivision(self)->list:
        bodysub_list = []
        # bodysub_list = re.findall(r"[a-z].*?;",bodysub,re.DOTALL)

        for v in self.body().split(";"):
            if v:
                bodysub_list.append(v.strip())
        return bodysub_list

    def bodyToDict(self)->dict:
        s_dict = dict()
        for v in self.bodySubdivision():
            key,value = v.split(":",1)
            s_dict[key]=value.strip()
        return s_dict

    def toDict(self)->dict:
        return self._qss_dict

    def updateAttr(self,key,value):
        self._qss_dict[self.header()][key]=value
        # print(self._qss_dict)
        self._qss_str = dictTostr(self._qss_dict)
        self.Init()
        if self.__parent:
            self.__parent.setStyleSheet(self._qss_str)



    def __str__(self):
        return self._qss_str


class QssStyleAnalysis:
    def __init__(self,parent=None):
        self.__parent = parent
        self._qss = [] # type:Qss
        self._map_qss = dict()

    # 分解多组QSS
    def groupDecomposition(self,styles):
        styles=re.findall(r".*?}", styles, re.DOTALL)
        return [v.strip() for v in styles]

    def count(self) -> int:
        return len(self._qss)

    def setQSS(self,qss:str):
        # Preprocessing qss
        self._qss = [Qss(qss,self.__parent) for qss in self.groupDecomposition(qss)]
        # Mapping coordinate
        for i in range(self.count()):
            self._map_qss[self.qssIndex(i).header()]=i

        if self.__parent:
            self.__parent.setStyleSheet(qss)

    def setQSSDict(self,qss_dict:dict):
        self.setQSS(dictTostr(qss_dict))

    def printShow(self):
        for qss in self._qss:
            print(qss)

    def qssKey(self,key)->Qss:
        return self.qssIndex(self._map_qss[key])

    def qssIndex(self,i)->Qss:
        return self._qss[i]

    def qss(self,ang)->Qss:
        if isinstance(ang,int):
            return self.qssIndex(i)
        elif isinstance(ang,str):
            return self.qssKey(ang)
        else:
            raise TypeError("Parameter error!")

    def toDict(self)->dict:
        qss_dict = dict()
        for i in range(self.count()):
            qss_dict.update(self.qssIndex(i).toDict())
        return qss_dict

    # 更新样式
    def updateStyleSheet(self,ang,parent=None):
        if parent is None and self.__parent is None:
            raise TypeError("Unable to update!")
        elif parent:
            parent.setStyleSheet(str(self.qss(ang)))
        elif self.__parent:
            parent = self.__parent
            parent.setStyleSheet(str(self.qss(ang)))
        parent.update()

    def __str__(self):
        return dictTostr(self.toDict())

style = '''
#MainWindow{
	background-color: rgb(255, 255, 255);
	background-color: qradialgradient(spread:pad, cx:0.466, cy:0.482364, radius:0.433, fx:0.119699, fy:0.223154, stop:0 rgba(11, 8, 8, 255), stop:1 rgba(255, 255, 255, 255));
	color: rgb(255, 255, 127);
}
QDASD,DWWW{
background-color: rgb(255, 255, 255);
color: rgb(255, 255, 127);
}
'''

style_dict = {'#MainWindow': {'background-color': 'qradialgradient(spread:pad, cx:0.466, cy:0.482364, radius:0.433, fx:0.119699, fy:0.223154, stop:0 rgba(11, 8, 8, 255), stop:1 rgba(255, 255, 255, 255))', 'color': 'rgb(255, 255, 127)'}, 'QDASD,DWWW': {'background-color': 'rgb(255, 255, 255)', 'color': 'rgb(255, 255, 127)'}}

#
# qsa = QssStyleAnalysis()
# qsa.setQSSDict(style_dict)
# print(qsa)
# qsa.setQSS(style)
# print(qsa.toDict())
# print(qsa.qss("#MainWindow").bodyToDict())
# print(qsa.qssIndex(0).headerSubdivision())
# print(qsa.qssIndex(0).bodyToDict())
# print(qsa.qssIndex(1).bodyToDict())
# qsa.qss("#MainWindow").updateAttr("background-color","#000")

# def tt(a):
#     a.updateAttr("background-color","red")
#     print(a)
#
# tt(qsa.qss("#MainWindow"))