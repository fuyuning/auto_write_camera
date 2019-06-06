# *-coding:utf-8-*-
import csv
import re
import os


# 自动生成robot文件类
class AutoWriteRobot(object):
    def __init__(self):
        self.params_path = '../cache/params'
        self.document_path = '../cache/document'
        self.log_path = '../cache/document'

    @staticmethod
    def fail_print(help_str):
        print('\033[0;31m'+help_str+'\033[0m')

    @staticmethod
    def help_print(help_str):
        print('\033[0;32m'+help_str+'\033[0m')

    @staticmethod
    def warning_print(help_str):
        print('\033[0;33m'+help_str+'\033[0m')

    # 解析爬取的数据
    def _parse_file(self):
        folder = os.path.exists(self.params_path)
        if not folder:
            os.makedirs(self.params_path)
        folder = os.path.exists('../cache/json')
        if not folder:
            os.makedirs('../cache/json')
        with open('%s/params_list.csv' % self.params_path, 'w+') as params_csv:
            params_csv.write('')
            params_csv.close()
        with open('%s/server_list.txt' % self.document_path, 'r') as server_file:
            for server_name in server_file:
                server_name = server_name.replace('\n', '')
                if server_name:
                    with open('%s/%s_auto_write_schema.csv' % (self.document_path, server_name), 'r') as schema_csv:
                        reader = csv.DictReader(schema_csv)
                        for row in reader:
                            with open('../cache/json/%s_%s.json' % (row['服务端'], row['实体名']), 'w+') as json_file:
                                params_list = row['实体参数'][1:-1].replace('\'', '').replace(' ', '').split(',')
                                type_list = row['参数类型'][1:-1].replace('\'', '').replace(' ', '').split(',')
                                for i in range(0, len(type_list)):
                                    if type_list[i] in ('float', 'Float', 'integer', 'int', 'time'):
                                        type_list[i] = 'number'
                                    if type_list[i] in ('bool', 'Boolean'):
                                        type_list[i] = 'boolean'
                                    if type_list[i] == 'text':
                                        type_list[i] = 'string'
                                    if type_list[i] == 'json':
                                        type_list[i] = 'object'
                                    if '<' in type_list[i] and '>' in type_list[i]:
                                        type_list[i] = 'array'
                                json_file.write('{\n  "definitions": {\n    "%s": {\n      "type":"object",'
                                                '\n      "properties":{\n' % row['实体名'])
                                for i in range(0, len(params_list)):
                                    if i != len(params_list)-1:
                                        end_point = ','
                                    else:
                                        end_point = ''
                                    if params_list[i] == 'updated_time':
                                        json_file.write('        "%s": {"type":["%s","null"]}%s\n' % (
                                            params_list[i], type_list[i], end_point))
                                    else:
                                        json_file.write('        "%s": {"type":"%s"}%s\n' % (
                                            params_list[i], type_list[i], end_point))
                                json_file.write('      },\n      "required": [\n')
                                for i in range(0, len(params_list)):
                                    if i != len(params_list)-1:
                                        end_point = ','
                                    else:
                                        end_point = ''
                                    json_file.write('        "%s"%s\n' % (params_list[i], end_point))
                                json_file.write('      ]\n    }\n  },\n  "type": "object",\n  "$ref": "#/definitions/'
                                                '%s"\n//  "type": "array",\n//  "minItems":0,\n//  "items": {\n//    "'
                                                '$ref": "#/definitions/%s"\n//  }\n}' % (row['实体名'], row['实体名']))
        with open('%s/auto_write_robot.csv' % self.document_path, 'r') as file:

            folder = os.path.exists('%s/old_auto_write_robot.csv' % self.document_path)
            if folder:
                with open('%s/old_auto_write_robot.csv' % self.document_path, 'r') as old_file:
                    old_file_line = []
                    new_file_line = []
                    new_line = ['服务端,模块名,接口名,请求方式,url,参数名,参数类型,是否必传,响应码情况,返回实体']
                    for line in old_file:
                        old_file_line.append(line)
                    for line in file:
                        new_file_line.append(line)
                    for line in new_file_line:
                        if line not in old_file_line:
                            new_line.append(line)
            else:
                new_line = file
            index2 = 0
            flag = ''
            lib_name = ''
            model_list = []
            all_model_list = []
            folder = os.path.exists('../cache/log')
            if not folder:
                os.makedirs('../cache/log')
            folder = os.path.exists('../cache/log/文档状态码问题.csv')
            if folder:
                os.rename('../cache/log/文档状态码问题.csv', '../cache/log/old_文档状态码问题.csv')
            with open('../cache/log/文档状态码问题.csv', 'w+', newline='') as csv_file:
                # 表头
                fieldnames = ['问题类型', '服务端', '模块名', '接口名', '请求方式', '问题', '预期']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                reader = csv.DictReader(new_line)
                for data in reader:
                    service_name = data['服务端'].replace(' ', '')
                    model_name = data['模块名'].replace(' ', '')
                    api_name = data['接口名'].replace(' ', '')
                    api_method = data['请求方式'].replace(' ', '')
                    api_url = data['url'].replace(' ', '')
                    api_params_name_list = data['参数名'][1:-1].replace('\'', '').replace(' ', '').split(',')
                    api_params_type_list = data['参数类型'][1:-1].replace('\'', '').replace(' ', '').split(',')
                    api_params_nn_list = data['是否必传'][1:-1].replace('\'', '').replace(' ', '').split(',')
                    api_codes_list = data['响应码情况'][1:-1].replace('\'', '').replace(' ', '').split(',')
                    return_entities = data['返回实体'].replace(' ', '')
                    if len(re.findall('404', str(api_codes_list))) > 1:
                        index = []
                        for i in api_codes_list:
                            if i not in index:
                                index.append(i)
                        api_codes_list = index
                        writer.writerow({'问题类型': '建议修改', '服务端': service_name, '模块名': model_name, '接口名': api_name,
                                         '请求方式': api_method, '问题': '文档含有过多 404,应移除', '预期': str(api_codes_list)})
                    if api_url.find(':') != -1 and str(api_codes_list).find('404') == -1:
                        api_codes_list.append('404')
                        writer.writerow({'问题类型': '已知缺陷', '服务端': service_name, '模块名': model_name, '接口名': api_name,
                                         '请求方式': api_method, '问题': '缺少 404', '预期': str(api_codes_list)})
                    if api_params_name_list[0] != '' and str(api_codes_list).find('422') == -1:
                        api_codes_list.append('422')
                        writer.writerow({'问题类型': '已知缺陷', '服务端': service_name, '模块名': model_name, '接口名': api_name,
                                         '请求方式': api_method, '问题': '缺少 422', '预期': str(api_codes_list)})
                    if '404' in api_codes_list and api_url.find(':') == -1:
                        api_codes_list.remove('404')
                        writer.writerow({'问题类型': '已知缺陷', '服务端': service_name, '模块名': model_name, '接口名': api_name,
                                         '请求方式': api_method, '问题': '文档不该含有 404,应移除', '预期': str(api_codes_list)})
                    if '422' in api_codes_list and api_params_name_list[0] == '':
                        api_codes_list.remove('422')
                        writer.writerow({'问题类型': '已知缺陷', '服务端': service_name, '模块名': model_name, '接口名': api_name,
                                         '请求方式': api_method, '问题': '文档不该含有 422,应移除', '预期': str(api_codes_list)})
                    return_code = re.findall('20[0-9]', str(api_codes_list))
                    if return_code:
                        return_code = '返回 ' + str(return_code[0])
                    else:
                        return_code = ' 未识别到2xx的返回 '
                    if '200' not in api_codes_list and api_method == 'GET':
                        writer.writerow({'问题类型': '建议修改', '服务端': service_name, '模块名': model_name, '接口名': api_name,
                                         '请求方式': api_method, '问题': '应该返回 200, 但%s,请判断是否为文档及代码错误' % return_code,
                                         '预期': str(api_codes_list)})
                        if '201' not in api_codes_list and api_method == 'POST':
                            writer.writerow({'问题类型': '有待验证', '服务端': service_name, '模块名': model_name, '接口名': api_name,
                                             '请求方式': api_method, '问题': '%s,是否为特殊接口' % return_code})
                    elif '204' not in api_codes_list and api_method in ('PUT', 'DELETE', 'PATCH'):
                        writer.writerow({'问题类型': '建议修改', '服务端': service_name, '模块名': model_name, '接口名': api_name,
                                         '请求方式': api_method, '问题': '应该返回 204, 但%s,请判断是否为文档及代码错误' % return_code,
                                         '预期': str(api_codes_list)})
                    api_list = []
                    local = '%s_%s' % (service_name, model_name)
                    class_name = self._upper_name(model_name)
                    if flag != local:
                        flag = local
                        all_model_list.append(model_list)
                        model_list = []
                        lib_name, model_name = self._write_robot_file_settings(service_name, model_name)
                        class_name = self._write_library_head(lib_name, model_name)
                    api_list.append(service_name)
                    api_list.append(model_name)
                    api_list.append(api_name)
                    api_list.append(api_method)
                    api_list.append(api_url)
                    api_list.append(api_params_name_list)
                    api_list.append(api_codes_list)
                    api_list.append(lib_name)
                    api_list.append(return_entities)
                    api_list.append(api_params_nn_list)
                    api_list.append(api_params_type_list)
                    api_list.append(class_name)
                    model_list.append(api_list)
                    if index2 == 65535:
                        break
                    index2 += 1
            all_model_list.append(model_list)
            self.help_print('总计写入模块：%s个' % str(len(all_model_list) - 1))
            for i in range(0, len(all_model_list)):
                self.parse_model_file(all_model_list[i])

    # 解析模块文件
    def parse_model_file(self, model):
        case_switch = True
        keyword_switch = True
        id_in_url = []
        model_list_sort = []
        for i in range(0, 5):
            for j in model:
                if j[3] == 'POST' and i == 0:
                    model_list_sort.append(j)
                if j[3] == 'GET' and i == 1:
                    model_list_sort.append(j)
                if j[3] == 'PUT' and i == 2:
                    model_list_sort.append(j)
                if j[3] == 'PATCH' and i == 3:
                    model_list_sort.append(j)
                if j[3] == 'DELETE' and i == 4:
                    model_list_sort.append(j)
        for i in model_list_sort:
            url_parts = i[4].split('/')
            for j in url_parts:
                if j.find(':') != -1:
                    j = j.replace(':', '')
                    if j not in id_in_url:
                        id_in_url.append(j)
        for i in range(0, 3):
            for api in model_list_sort:
                params_txt = open('../cache/params/params_list.txt', "a+")
                service_name = api[0]
                model_name = api[1]
                api_name = api[2]
                api_method = api[3]
                api_url = api[4]
                api_params_name_list = api[5]
                api_codes_list = api[6]
                lib_name = api[7]
                return_entities = api[8]
                api_params_nn_list = api[9]
                api_params_type_list = api[10]
                class_name = api[11]
                api_codes_list_sort = api_codes_list
                if '403' in api_codes_list:
                    code_index = 0
                    for api_code in api_codes_list:
                        if api_code == '403':
                            api_codes_list_sort[0], api_codes_list_sort[code_index] = api_codes_list[code_index], \
                                                                                      api_codes_list[0]
                        code_index += 1
                if i == 0:
                    self._write_lib_file(class_name, lib_name, api_method, api_url, api_params_name_list)
                if i == 1:
                    self._write_robot_file_case(params_txt, service_name, model_name, api_name, api_method, api_url,
                                                api_params_name_list, api_codes_list_sort, return_entities,
                                                api_params_nn_list, api_params_type_list, case_switch)
                    case_switch = False
                if i == 2:
                    self._write_robot_file_keywords(service_name, model_name, api_method, api_url, api_codes_list_sort,
                                                    id_in_url, keyword_switch)
                    keyword_switch = False

    # 写入library头文件
    def _write_library_head(self, lib_name, model_name):
        self.help_print('正在写入文件：%s/__init__.py' % lib_name)
        lib_name = '../%s' % lib_name.replace('.', '/')
        lib = os.path.exists(lib_name)
        if not lib:
            os.makedirs(lib_name)
        class_name = self._upper_name(model_name)
        lib_import = lib_name.split('/')[1]
        open('%s/__init__.py' % lib_name, 'w+')
        folder = os.path.exists('%s/%sLibrary.py' % (lib_name, class_name))
        if folder:
            os.rename('%s/%sLibrary.py' % (lib_name, class_name), '%s/old_%sLibrary.py' % (lib_name, class_name))
        self.help_print('正在写入文件：%s/%sLibrary.py' % (lib_name, class_name))
        lib_file = open('%s/%sLibrary.py' % (lib_name, class_name), 'w+')
        lib_file.write('from %s.common import CommonLibrary\n\n\n' % lib_import)
        lib_file.write('class %sLibrary(CommonLibrary):\n' % class_name)
        lib_file.close()
        return class_name

    # 根据爬取的数据生成library
    def _write_lib_file(self, class_name, lib_name, api_method, api_url, api_params_name_list):
        api_method = self._upper_name(api_method)
        lib_name = lib_name.replace('.', '/')
        lib_file = open('../%s/%sLibrary.py' % (lib_name, class_name), 'a+')
        api_params = ''
        index = 0
        for i in api_params_name_list:
            index += 1
            if index != len(api_params_name_list) or index == 1:
                api_params = '%s"%s", ' % (api_params, i)
            elif index == len(api_params_name_list) and i != '':
                api_params = '%s"%s"' % (api_params, i)
        if api_params == '"", ':
            kwargs_name = ''
        else:
            kwargs_name = ', **kwargs'
        change_data = ''
        api_method = api_method.lower()
        if api_method == 'get':
            change_data = 'params=data'
        elif api_method in ('post', 'put', 'patch'):
            change_data = 'json=data'
        if len(api_params_name_list) > 0:
            change_data = ', %s' % change_data
        else:
            change_data = ''
        api_url_part = api_url.split('/')
        url_format = ''
        for i in api_url_part:
            if i.find(':') != -1:
                i = '{' + i.replace(':', '') + '}'
            if i != '':
                url_format = url_format + '/' + i
        method_name, id_name_list, url_params, format_data = self._parse_url_part(api_url)
        lib_file.write(
            '    def ' + api_method.lower() + method_name.lower() + '(self' + url_params + kwargs_name + '):\n')
        lib_file.write('        url = "{SERVER_DOMAIN}' + url_format + '".format(\n            SERVER_DOMAIN='
                                                                       'self.SERVER_DOMAIN' + format_data + ')\n')
        if api_params != '"", ':
            lib_file.write('        data = {}\n'
                           + '        for k, v in kwargs.items():\n'
                           + '            if k in (' + api_params + '):\n'
                           + '                data[k] = v\n')
        lib_file.write('        return self.client.' + api_method + '(url' + change_data + ')\n\n')
        lib_file.close()

    # 根据爬取的数据生成robot文件头
    def _write_robot_file_settings(self, service_name, model_name):
        pass
        full_name = '%s_%s' % (service_name, model_name)
        folder = os.path.exists('../tests/%s' % full_name)
        if not folder:
            os.makedirs('../tests/%s' % full_name)
        lib_name = ''
        setup = ''
        teardown = ''
        name_tag = ''
        if service_name == 'server':
            lib_name = 'robot_camera_monitor_server_library.'
            setup = 'Suite Setup  Login  ${admin_username}   ${admin_password}'
            teardown = 'Suite Teardown  Logout'
            name_tag = ''
        lib_name = lib_name[:-1] + '.' + model_name
        class_name = self._upper_name(model_name)
        folder = os.path.exists('../tests/%s/%ss.robot' % (full_name, model_name))
        if folder:
            os.rename('../tests/%s/%ss.robot' % (full_name, model_name), '../tests/%s/old_%ss.robot' %
                      (full_name, model_name))
            os.rename('../tests/%s/%ss.unauthorized.robot' % (full_name, model_name),
                      '../tests/%s/old_%ss.unauthorized.robot' % (full_name, model_name))

        self.help_print('正在写入文件：../tests/%s/%ss.robot' % (full_name, model_name))
        robot = open('../tests/%s/%ss.robot' % (full_name, model_name), 'w+')
        robot.write('*** Settings ***\n')
        robot.write('Documentation  ' + full_name + '\n')
        robot.write('Resource  ../resources.robot' + '\n')
        robot.write('Library  ' + lib_name + '.' + class_name + 'Library' + '\n')
        robot.write(setup + '\n')
        if teardown != '':
            robot.write(teardown + '\n')
        robot.write('Force Tags  model:' + full_name + '  ' + name_tag + '\n\n\n')
        self.help_print('正在写入文件：' + '../tests/' + full_name + '/' + model_name + 's.unauthorized.robot')
        robot = open('../tests/' + full_name + '/' + model_name + 's.unauthorized.robot', 'w+')
        robot.write('*** Settings ***\n')
        robot.write('Documentation  ' + full_name + '\n')
        robot.write('Resource  ../resources.robot' + '\n')
        robot.write('Library  ' + lib_name + '.' + class_name + 'Library' + '\n')
        robot.write('Force Tags  model:' + full_name + '  ' + name_tag + '\n\n\n')
        return lib_name, model_name

    # 根据爬取的数据生成robot文件test_case
    def _write_robot_file_case(self, params_txt, service_name, model_name, api_name, api_method, api_url,
                               api_params_name_list, api_codes_list, return_entities, api_params_nn_list,
                               api_params_type_list, case_switch):
        id_in_url = []
        url_parts = api_url.split('/')
        for j in url_parts:
            if j.find(':') != -1:
                j = j.replace(':', '')
                if j not in id_in_url:
                    id_in_url.append(j)
        full_name = service_name + '_' + model_name
        api_method = self._upper_name(api_method)
        method_name = (api_method + self._parse_url_part(api_url)[0]).lower().replace('_', ' ')
        for api_code in api_codes_list:
            wrong_id_value = ''
            if id_in_url:
                id_name = id_in_url
            else:
                id_name = 'Please_input'
            if api_url.find(':') == -1:
                flag = False
                lt_part = ' 列表'
            else:
                flag = True
                lt_part = ' 对象'
            if api_code == '200':
                kw_name = method_name + ' success ' + api_code
                tc_name = method_name + ' Success '
                st_part = '输入正确参数,'
                ed_part = ',返回的Json数据为 ' + return_entities + lt_part
            elif api_code == '201':
                kw_name = method_name + ' success ' + api_code
                tc_name = method_name + ' Success '
                st_part = '输入正确参数,'
                ed_part = ',返回的Json数据符合验证'
            elif api_code == '204':
                kw_name = method_name + ' success ' + api_code
                tc_name = method_name + ' Success '
                st_part = '输入正确参数,'
                ed_part = ',无Json数据返回'
            elif api_code == '404':
                kw_name = method_name + ' fail ' + api_code
                tc_name = method_name + ' Fail With Wrong Url'
                st_part = '输入正确参数及错误的url,'
                ed_part = ',无Json数据返回'
                wrong_id_value = 'wrong_url_id'
            elif api_code == '403':
                kw_name = method_name + ' fail ' + api_code
                tc_name = method_name + ' Fail Without Login'
                st_part = '未登录,'
                ed_part = ',无Json数据返回'
            elif api_code == '422':
                kw_name = method_name + ' fail ' + api_code
                tc_name = method_name + ' Fail With Wrong Params'
                st_part = '输入错误参数,'
                ed_part = ',返回的Json数据为错误信息'
            else:
                kw_name = ''
                tc_name = ''
                st_part = '暂无此类测试功能,'
                ed_part = ''
            ex_result = st_part + 'http响应码返回 ' + api_code + ed_part + '。'
            essential_params_part = ''
            unessential_params_part = ''
            if api_code == '422':
                success_value = '  success=False'
            else:
                success_value = ''
            for i in range(0, len(api_params_name_list)):
                params_name = str(api_params_name_list[i])
                not_none = api_params_nn_list[i]
                params_type = api_params_type_list[i].lower()
                if params_type == 'bool' or params_type == 'boolean':
                    if api_code != '422':
                        params_value = 'False'
                    else:
                        params_value = 'ThisIsRobot!'
                elif params_type in ('string', 'int', 'json', 'array', 'float', 'integer', 'object'):
                    if api_code != '422':
                        params_value = '${' + params_name + '}'
                    else:
                        params_value = '${' + params_name + '_422}'
                    params_txt.write(params_value + ',' + params_type + '\n')
                else:
                    params_value = '${Please_input}'

                if not_none == 'T':
                    essential_params_part = essential_params_part + params_name + '=' + params_value + '  '
                else:
                    unessential_params_part = unessential_params_part + params_name + '=' + params_value + '  '
            if api_code != '403':
                name_part = ''
            else:
                name_part = 'unauthorized.'
            format_kwp = ''
            for i in range(0, len(id_name)):
                if api_code == '404':
                    id_name_value = wrong_id_value
                else:
                    id_name_value = id_name[i]
                format_kwp = format_kwp + '  ' + id_name[i] + '=${' + id_name_value + '}'
            robot = open('../tests/' + full_name + '/' + model_name + 's.' + name_part + 'robot', 'a+')
            if case_switch is True:
                robot.write('*** Test Cases ***\n')
                if api_code != '403':
                    case_switch = False
            robot.write(tc_name + '\n')
            robot.write('   [Documentation]  接口名:' + api_name + '${\\n}\n   ...              请求方式:' + api_method +
                        '${\\n}\n   ...              预期结果:' + ex_result + '\n')
            robot.write('   [Tags]           Respcode:' + api_code + '\n')
            if flag is False and api_params_name_list != ['']:
                if api_code in ('403', '404'):
                    robot.write('   ' + kw_name + '   ' + essential_params_part + '  ' + unessential_params_part + '\n')
                else:
                    robot.write('   ${essential_params}  create dictionary  ' + essential_params_part + '\n')
                    robot.write('   ${unessential_params}  create dictionary  ' + unessential_params_part + '\n')
                    robot.write(
                        '   run every case by params   ' + kw_name + '   ${essential_params}  ${unessential_params}' +
                        success_value + '\n')
            if flag is False and api_params_name_list == ['']:
                robot.write('    ' + kw_name + '\n')
            if flag is True and api_params_name_list != ['']:
                if api_code in ('403', '404'):
                    robot.write('   ' + kw_name + '   ' + format_kwp + '  ' + essential_params_part + '  '
                                + unessential_params_part + '\n')
                else:
                    robot.write('   ${essential_params}  create dictionary  ' + essential_params_part + '\n')
                    robot.write('   ${unessential_params}  create dictionary  ' + unessential_params_part + '\n')
                    robot.write(
                        '   run every case by params   ' + kw_name + '   ${essential_params}  ${unessential_params}  ' +
                        format_kwp + success_value + '\n')
            if flag is True and api_params_name_list == ['']:
                robot.write('   ' + kw_name + '   ' + format_kwp + '\n')
            robot.write('\n')

    # 根据爬取的数据生成robot文件keywords
    def _write_robot_file_keywords(self, service_name, model_name, api_method, api_url, api_codes_list,
                                   id_in_url, keyword_switch):
        full_name = '%s_%s' % (service_name, model_name)
        api_method = self._upper_name(api_method)
        for api_code in api_codes_list:
            method_name = (api_method + self._parse_url_part(api_url)[0]).lower().replace('_', ' ')
            if api_code == '200':
                kw_name = method_name + ' Success ' + api_code
                json_name = full_name + '/' + method_name + '_' + api_code + '.json\n'
            elif api_code == '201':
                kw_name = method_name + ' Success ' + api_code
                json_name = full_name + '/' + method_name + '_' + api_code + '.json\n'
            elif api_code == '204':
                kw_name = method_name + ' Success ' + api_code
                json_name = '\n'
            elif api_code == '404':
                kw_name = method_name + ' Fail ' + api_code
                json_name = '\n'
            elif api_code == '403':
                kw_name = method_name + ' Fail ' + api_code
                json_name = '\n'
            elif api_code == '422':
                kw_name = method_name + ' Fail ' + api_code
                json_name = '\n'
            else:
                kw_name = ''
                json_name = '\n'
            json_name = json_name.replace(' ', '_')
            if api_code != '403':
                name_part = ''
            else:
                name_part = 'unauthorized.'
            robot = open('../tests/' + full_name + '/' + model_name + 's.' + name_part + 'robot', 'a+')
            if keyword_switch is True:
                robot.write('\n')
                if id_in_url:
                    robot.write('*** Variables ***\n')
                    if api_code == '403':
                        id_value = '1a2b3c4d5e6f7zz'
                    else:
                        id_value = ''
                    for var in id_in_url:
                        robot.write('${' + var + '}  ' + id_value + '\n')
                    robot.write('\n\n')
                robot.write('*** Keywords ***\n')
                if api_code != '403':
                    keyword_switch = False
            robot.write(kw_name + '\n')
            robot.write('   [Arguments]  &{kwargs}\n')
            robot.write('   ${resp}=  ' + method_name + '  &{kwargs}\n')
            robot.write('   expect status is ' + api_code + '  ${resp}  ' + json_name)
            if id_in_url != [] and api_code in ('200', '201') and api_method in ('Get', 'Post'):
                for k in range(0, len(id_in_url)):
                    robot.write('   ${' + id_in_url[k] + '}  set variable if  ${resp.json()}!=[]'
                                                         '  ${resp.json()[0][' + id_in_url[k] + ']}\n')
                    robot.write('   set global variable   ${' + id_in_url[k] + '}\n')
            robot.write('\n')

    @classmethod
    def _upper_name(cls, name, place=False):
        if '_' in name:
            str_list = name.split('_')
        else:
            str_list = name.split(' ')
        for index in range(0, len(str_list)):
            if place is False:
                end = ''
            else:
                end = ' '
            if str_list[index] != '':
                str_list[index] = str_list[index][0].upper() + str_list[index][1:].lower() + end
            else:
                continue
        return ''.join(str_list)

    # 把url处理为名字
    @classmethod
    def _parse_url_part(cls, api_url):
        url_parts = api_url.split("/")
        final_url_parts = []
        id_url_parts = []
        for i in url_parts:
            if i != '' and i.find(':') != -1:
                id_url_parts.append(i)

            if i != '' and i.find(':') == -1:
                final_url_parts.append(i)
        method_name = ''
        url_params = ''
        format_data = ''
        id_name_list = []
        for i in final_url_parts:
            method_name = method_name + '_' + i
        if id_url_parts:
            method_name = method_name + '_by'
            for i in id_url_parts:
                method_name = method_name + '_' + i.replace(':', '')
        if id_url_parts:
            for i in id_url_parts:
                id_name = i.replace(':', '')
                id_name_list.append(id_name)
                url_params = url_params + ', ' + id_name
                format_data = format_data + ', ' + id_name + '=' + id_name
        else:
            url_params = ''
        return method_name, id_name_list, url_params, format_data

    # run方法
    def run(self):
        self._parse_file()


if __name__ == '__main__':
    auto_write_robot = AutoWriteRobot()
    auto_write_robot.run()
