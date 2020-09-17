#coding=utf-8
import os
import lineTool


def SendLineNotify(content):
    token = "bQ0axZBPZ7HXeBaGlYG3fFtGYqF4Gyxgc624xwGycyO"
    msg = content
    print(content)
    lineTool.lineNotify(token, msg)

