# *-coding:utf-8-*-
import re
import os


# 自动生成robot文件类
class AutoWriteRobot(object):
    # 解析爬取的数据
    def _parse_file(self, file_name):
        ptxt = open('../cache/params/params_list.txt', "w+")
        ptxt.write('')
        ptxt.close()
        file = open(file_name, 'r')
        index2 = 0
        flag = ''
        lib_name = ''
        model_list = []
        all_model_list = []
        txt = open('../cache/log/document_wrong.txt', "w+")
        for line in file:
            line = line.replace(' ', '')
            data = line.split('||')
            data[5] = data[5][1:-1].replace('\'', '').split(',')
            data[6] = data[6][1:-1].replace('\'', '').split(',')
            data[7] = data[7][1:-1].replace('\'', '').split(',')
            data[8] = data[8][1:-1].replace('\'', '').split(',')
            service_name = data[0]
            model_name = data[1]
            api_name = data[2]
            api_method = data[3]
            api_url = data[4]
            api_params_name_list = data[5]
            api_params_type_list = data[6]
            api_params_nn_list = data[7]
            api_codes_list = list(data[8])
            return_entities = data[9]
            if api_url.find(':') != -1 and str(api_codes_list).find('404') == -1:
                api_codes_list.append('404')
                txt.write(service_name+'_'+model_name+':'+api_name+'：缺少 404,加入后:'+str(api_codes_list)+'\n')
            if api_params_name_list[0] != '' and str(api_codes_list).find('422') == -1:
                api_codes_list.append('422')
                txt.write(service_name+'_'+model_name+':'+api_name+'：缺少 422,加入后:'+str(api_codes_list)+'\n')
            if len(re.findall('404', str(api_codes_list))) > 1:
                index = []
                for i in api_codes_list:
                    if i not in index:
                        index.append(i)
                api_codes_list = index
                txt.write(service_name+'_'+model_name + ':' + api_name + '：含有过多 404,移除后:' + str(api_codes_list)+'\n')
            api_list = []
            if flag != service_name+'_'+model_name:
                flag = service_name + '_' + model_name
                if index2 != 0:
                    all_model_list.append(model_list)
                model_list = []
                lib_name = self._write_robot_file_settings(service_name, model_name, api_codes_list)
                self._write_library_head(lib_name, model_name)
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
            model_list.append(api_list)
            if index2 == 10000:
                break
            index2 += 1
        print(len(all_model_list))
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
            urls_id = i[4].split(':')
            if len(urls_id) > 1 and urls_id[1] not in id_in_url:
                id_in_url.append(urls_id[1])
        for i in range(0, 3):
            for api in model_list_sort:
                ptxt = open('../cache/params/params_list.txt', "a+")
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
                if i == 0:
                    self._write_lib_file(lib_name, model_name, api_method, api_url, api_params_name_list)
                if i == 1:
                    self._write_robot_file_case(ptxt, service_name, model_name, api_name, api_method, api_url,
                                                api_params_name_list, api_codes_list, return_entities,
                                                api_params_nn_list, api_params_type_list, case_switch)
                    case_switch = False
                if i == 2:
                    self._write_robot_file_keywords(service_name, model_name, api_method, api_url, api_codes_list,
                                                    id_in_url, keyword_switch)
                    keyword_switch = False

    # 写入library头文件
    def _write_library_head(self, lib_name, model_name):
        lib_name = '../'+lib_name.replace('.', '/')
        lib = os.path.exists(lib_name)
        if not lib:
            os.makedirs(lib_name)
        class_name = self._upper_name(model_name)
        lib_import = lib_name.split('/')[1]
        open(lib_name + '/' + '__init__.py', 'w+')
        lib_file = open(lib_name + '/' + class_name + 'Library.py', 'w+')
        lib_file.write('from '+lib_import+'.common import CommonLibrary\n\n\n')
        lib_file.write('class ' + class_name + 'Library(CommonLibrary):\n')
        lib_file.close()

    # 根据爬取的数据生成library
    def _write_lib_file(self, lib_name, model_name, api_method, api_url, api_params_name_list):
        api_method = self._upper_name(api_method)
        class_name = self._upper_name(model_name)
        lib_name = lib_name.replace('.', '/')
        lib_file = open('../'+lib_name + '/' + class_name + 'Library.py', 'a+')
        url_parts = api_url.split("/:")
        url_part_one = url_parts[0]
        method_name = str(url_part_one).split('/')
        if len(method_name) > 1 and method_name[-2] != '':
            method_name = method_name[-2]+'_'+method_name[-1]
        else:
            method_name = method_name[-1]
        if len(url_parts) > 1:
            id_name = url_parts[1].split("/")[0]
            if len(url_parts[1].split("/")) > 1:
                url_end = '/' + url_parts[1].split("/")[1]
            else:
                url_end = ''
            url_params = ', '+id_name
        else:
            id_name = ''
            url_params = ''
            url_end = ''
        format_data = ''
        if id_name != '':
            format_data = ', '+id_name+'='+id_name
            id_in_name = '/{'+id_name+'}'
        else:
            id_in_name = ''
        change_data = ''
        api_method = api_method.lower()
        if api_method == 'get':
            change_data = 'params=data'
        elif api_method in ('post', 'put', 'patch'):
            change_data = 'json=data'
        if len(api_params_name_list) > 1:
            change_data = ', '+change_data
        else:
            change_data = ''
        api_params = ''
        index = 0
        for i in api_params_name_list:
            index += 1
            if index != len(api_params_name_list) or index == 1:
                api_params = api_params + '"' + i + '", '
            elif index == len(api_params_name_list) and i != '':
                api_params = api_params + '"' + i + '"'
        if api_params == '"", ':
            kwargs_name = ''
        else:
            kwargs_name = ', **kwargs'
        if id_name != '':
            str1 = '_by_'
        else:
            str1 = ''
        if url_end != '':
            method_name = url_end.replace('/', '')
        method_name = (api_method + '_' + method_name + str1 + id_name).lower()
        lib_file.write('    def ' + method_name + '(self' + url_params + kwargs_name+'):\n')
        lib_file.write('        url = "{SERVER_DOMAIN}'+url_part_one+id_in_name+url_end
                       + '".format(\n            SERVER_DOMAIN=self.SERVER_DOMAIN'+format_data+')\n')
        if api_params != '"", ':
            lib_file.write('        data = {}\n'
                           + '        for k, v in kwargs.items():\n'
                           + '            if k in ('+api_params+'):\n'
                           + '                data[k] = v\n')
        lib_file.write('        return self.client.'+api_method+'(url'+change_data+')\n\n')
        lib_file.close()

    # 根据爬取的数据生成robot文件头
    def _write_robot_file_settings(self, service_name, model_name, api_codes_list):
        full_name = service_name+'_'+model_name
        folder = os.path.exists('../tests/'+full_name)
        if not folder:
            os.makedirs('../tests/'+full_name)
        lib_name = ''
        setup = ''
        teardown = ''
        name_tag = ''
        if service_name == 'admin':
            lib_name = 'robot_car_wash_server_library.'
            setup = 'Suite Setup  Login  ${admin_username}   ${admin_password}'
            teardown = 'Suite Teardown  Logout'
            name_tag = '虾洗后台'
        elif service_name == 'app':
            lib_name = 'robot_car_wash_app_library.'
            setup = 'Suite Setup  Login  ${app_username}  ${app_password}'
            teardown = ''
            name_tag = '虾客APP'
        elif service_name == 'wxmp':
            lib_name = 'robot_car_wash_wxmp_library.'
            setup = 'Suite Setup  Login By Openid  ${openid}'
            teardown = ''
            name_tag = '车主微信端'
        lib_name = lib_name[:-1]+'.'+model_name
        class_name = self._upper_name(model_name)
        robot = open('../tests/'+full_name+'/'+model_name+'s.robot', 'w+')
        robot.write('*** Settings ***\n')
        robot.write('Documentation  '+full_name+'\n')
        robot.write('Resource  ../resources.robot'+'\n')
        robot.write('Library  '+lib_name+'.'+class_name+'Library'+'\n')
        robot.write(setup+'\n')
        robot.write(teardown+'\n')
        robot.write('Force Tags  model:'+full_name+'  '+name_tag+'\n\n\n')
        if '403' in api_codes_list:
            name_part = 'unauthorized.'
        else:
            name_part = 'please_delete.'
        robot = open('../tests/' + full_name + '/' + model_name + 's.'+name_part+'robot', 'w+')
        robot.write('*** Settings ***\n')
        robot.write('Documentation  ' + full_name + '\n')
        robot.write('Resource  ../resources.robot' + '\n')
        robot.write('Library  ' + lib_name + '.' + class_name + 'Library' + '\n')
        robot.write('Force Tags  model:' + full_name + '  ' + name_tag + '\n\n\n')
        return lib_name

    # 根据爬取的数据生成robot文件test_case
    def _write_robot_file_case(self, ptxt, service_name, model_name, api_name, api_method, api_url, api_params_name_list,
                               api_codes_list, return_entities, api_params_nn_list, api_params_type_list, case_switch):
        full_name = service_name+'_'+model_name
        api_method = self._upper_name(api_method)
        url_parts = api_url.split("/:")
        url_part_one = url_parts[0]
        method_name = str(url_part_one).split('/')
        if len(method_name) > 1 and method_name[-2] != '':
            method_name = method_name[-2]+' '+method_name[-1].replace('_', ' ')
        else:
            method_name = method_name[-1].replace('_', ' ')
        print(method_name)
        if len(url_parts) > 1:
            id_name = url_parts[1].split("/")[0].replace('_', ' ')
            if len(url_parts[1].split("/")) > 1:
                url_end = '/' + url_parts[1].split("/")[1]
            else:
                url_end = ''
        else:
            id_name = ''
            url_end = ''
        if id_name != '':
            str1 = ' by '
        else:
            str1 = ''
        if url_end != '':
            method_name = url_end.replace('/', '')
        method_name = (api_method + ' ' + method_name + str1 + id_name).lower()
        method_name = self._upper_name(method_name, place=True)
        for api_code in api_codes_list:
            wrong_id_name = ''
            if len(api_url.split(':')) > 1:
                id_name = api_url.split(':')[1]
            else:
                id_name = 'Please_input'
            if api_url.find(':') == -1:
                flag = False
                lt_part = ' 列表'
            else:
                flag = True
                lt_part = ' 对象'
            if api_code == '200':
                kw_name = method_name + 'Success ' + api_code
                tc_name = method_name + 'Success '
                st_part = '输入正确参数,'
                ed_part = ',返回的Json数据为 '+return_entities+lt_part
            elif api_code == '201':
                kw_name = method_name + 'Success ' + api_code
                tc_name = method_name + 'Success '
                st_part = '输入正确参数,'
                ed_part = ',返回的Json数据符合验证'
            elif api_code == '204':
                kw_name = method_name + 'Success ' + api_code
                tc_name = method_name + 'Success '
                st_part = '输入正确参数,'
                ed_part = ',无Json数据返回'
            elif api_code == '404':
                kw_name = method_name + 'Fail ' + api_code
                tc_name = method_name + 'Fail With Wrong Url'
                st_part = '输入正确参数及错误的url,'
                ed_part = ',无Json数据返回'
                wrong_id_name = 'wrong_url_id'
            elif api_code == '403':
                kw_name = method_name + 'Fail ' + api_code
                tc_name = method_name + 'Fail Without Login'
                st_part = '未登录,'
                ed_part = ',无Json数据返回'
            elif api_code == '422':
                kw_name = method_name + 'Fail ' + api_code
                tc_name = method_name + 'Fail With Wrong Params'
                st_part = '输入错误参数,'
                ed_part = ',返回的Json数据为错误信息'
            else:
                kw_name = ''
                tc_name = ''
                st_part = '暂无此类测试功能,'
                ed_part = ''
            ex_result = st_part+'http响应码返回 '+api_code+ed_part+'。'
            essential_params_part = ''
            unessential_params_part = ''
            for i in range(0, len(api_params_name_list)):
                params_name = str(api_params_name_list[i])
                not_none = api_params_nn_list[i]
                params_type = api_params_type_list[i].lower()
                if params_type == 'bool' or params_type == 'boolean':
                    params_value = 'False'
                elif params_type in ('string', 'int', 'json', 'array', 'float'):
                    params_value = '${' + params_name + '}'
                    ptxt.write(params_value+'\n')
                else:
                    params_value = '${Please_input}'

                if not_none == 'T':
                    essential_params_part = essential_params_part+params_name+'='+params_value+'  '
                else:
                    unessential_params_part = unessential_params_part+params_name+'='+params_value+'  '
            if api_code == '404':
                id_name_value = wrong_id_name
            else:
                id_name_value = id_name
            if api_code != '403':
                name_part = ''
            else:
                name_part = 'unauthorized.'
            robot = open('../tests/' + full_name + '/' + model_name + 's.'+name_part+'robot', 'a+')
            if case_switch is True:
                robot.write('*** Test Cases ***\n')
                if api_code != '403':
                    case_switch = False
            robot.write(tc_name+'\n')
            robot.write('   [Documentation]  接口名:' + api_name + '${\\n}\n   ...              请求方式:' + api_method +
                        '${\\n}\n   ...              预期结果:'+ex_result+'\n')
            robot.write('   [Tags]           Respcode:'+api_code+'\n')
            if flag is False and api_params_name_list != ['']:
                robot.write('   ${essential_params}  create list  '+essential_params_part+'\n')
                robot.write('   ${unessential_params}  create list  '+unessential_params_part+'\n')
                robot.write('   run every case by params  '+kw_name+'  ${essential_params}  ${unessential_params}\n')
            if flag is False and api_params_name_list == ['']:
                robot.write('    '+kw_name+'\n')
            if flag is True and api_params_name_list != ['']:
                robot.write('   ${essential_params}  create list  '+essential_params_part+'\n')
                robot.write('   ${unessential_params}  create list  '+unessential_params_part+'\n')
                robot.write('   run every case by params  '+kw_name+'  ${essential_params}  ${unessential_params}  ' +
                            id_name+'=${'+id_name_value+'}\n')
            if flag is True and api_params_name_list == ['']:
                robot.write('   '+kw_name+'  '+id_name+'=${'+id_name_value+'}\n')
            robot.write('\n')

    # 根据爬取的数据生成robot文件keywords
    def _write_robot_file_keywords(self, service_name, model_name, api_method, api_url, api_codes_list,
                                   id_in_url, keyword_switch):
        full_name = service_name+'_'+model_name
        api_method = self._upper_name(api_method)
        for api_code in api_codes_list:
            url_parts = api_url.split("/:")
            url_part_one = url_parts[0]
            method_name = str(url_part_one).split('/')
            if len(method_name) > 1 and method_name[-2] != '':
                method_name = method_name[-2] + ' ' + method_name[-1].replace('_', ' ')
            else:
                method_name = method_name[-1].replace('_', ' ')
            print(method_name)
            if len(url_parts) > 1:
                id_name = url_parts[1].split("/")[0].replace('_', ' ')
                if len(url_parts[1].split("/")) > 1:
                    url_end = '/' + url_parts[1].split("/")[1]
                else:
                    url_end = ''
            else:
                id_name = ''
                url_end = ''
            if id_name != '':
                str1 = ' by '
            else:
                str1 = ''
            if url_end != '':
                method_name = url_end.replace('/', '')
            method_name = (api_method + ' ' + method_name + str1 + id_name).lower()
            method_name = self._upper_name(method_name, place=True)
            if api_code == '200':
                kw_name = method_name + 'Success ' + api_code
                json_name = full_name+'/'+method_name+api_code+'.json\n'
            elif api_code == '201':
                kw_name = method_name + 'Success ' + api_code
                json_name = full_name+'/'+method_name+api_code+'.json\n'
            elif api_code == '204':
                kw_name = method_name + 'Success ' + api_code
                json_name = '\n'
            elif api_code == '404':
                kw_name = method_name + 'Fail ' + api_code
                json_name = '\n'
            elif api_code == '403':
                kw_name = method_name + 'Fail ' + api_code
                json_name = '\n'
            elif api_code == '422':
                kw_name = method_name + 'Fail ' + api_code
                json_name = '\n'
            else:
                kw_name = ''
                json_name = '\n'
            json_name = json_name.replace(' ', '_')
            if api_code != '403':
                name_part = ''
            else:
                name_part = 'unauthorized.'
            robot = open('../tests/' + full_name + '/' + model_name + 's.'+name_part+'robot', 'a+')
            if keyword_switch is True:
                robot.write('\n')
                if id_in_url:
                    robot.write('*** Variables ***\n')
                    for var in id_in_url:
                        robot.write('${'+var+'}\n')
                    robot.write('\n\n')
                robot.write('*** Keywords ***\n')
                if api_code != '403':
                    keyword_switch = False
            robot.write(kw_name+'\n')
            robot.write('   [Arguments]  &{kwargs}\n')
            robot.write('   ${resp}=  '+method_name+'  &{kwargs}\n')
            robot.write('   expect status is '+api_code+'  ${resp}  '+json_name)
            if id_in_url != [] and api_code in ('200', '201') and api_method in ('Get', 'Post'):
                for k in range(0, len(id_in_url)):
                    robot.write('   ${'+id_in_url[k]+'}  set variable if  ${resp.json()}!=[]'
                                '  ${resp.json()[0]['+id_in_url[k]+']}\n')
                    robot.write('   set global variable   ${'+id_in_url[k]+'}\n')
            robot.write('\n')

    @staticmethod
    def _upper_name(name, place=False):
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
                str_list[index] = str_list[index][0].upper()+str_list[index][1:].lower()+end
            else:
                continue
        return ''.join(str_list)

    # run方法
    def run(self):
        self._parse_file('../cache/document/auto_write_robot.txt')


if __name__ == '__main__':
    auto_write_robot = AutoWriteRobot()
    auto_write_robot.run()
