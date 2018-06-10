# coding:utf-8

import xlwt

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

'''
这里是操作execl的工具类,以后也可以直接复用
方法调用SpiderUtils.create_excecl(...) 

'''


class ExeclUtils(object):

    @staticmethod
    def create_execl(sheet_name, row_titles):
        '''
        创建execl文件与sheet表，并创建他们的第一行标题
        :param sheet_name: execl中sheet_name文件的名称
        :param row_titles: execl文件的标题行
        :return: execl_file,execl_sheet
        '''

        f = xlwt.Workbook()
        sheet_info = f.add_sheet(sheet_name, cell_overwrite_ok=True)
        for i in range(0, len(row_titles)):
            sheet_info.write(0, i, row_titles[i])

        return f, sheet_info

    @staticmethod
    def write_execl(execl_file, execl_sheet, count, data, execl_name):
        '''
        把数据写入到execl中.这是一个静态方法
        注意：这里所有的数据都不要写死，方便复用.
        :param execl_file:  传入一个execl文件
        :param execl_sheet:  传入一个execl_sheet表
        :param count:  execl文件的行数
        :param data:  要传入的一条数据
        :param execl_name: execl文件名
        :return: None
        '''
        for j in range(len(data)):
            execl_sheet.write(count, j, data[j])

        execl_file.save(execl_name)
