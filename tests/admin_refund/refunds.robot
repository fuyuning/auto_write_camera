*** Settings ***
Documentation  admin_refund
Resource  ../resources.robot
Library  robot_car_wash_server_library.refund.RefundLibrary
Suite Setup  Login  ${admin_username}   ${admin_password}
Suite Teardown  Logout
Force Tags  model:admin_refund  虾洗后台


*** Test Cases ***
Get Admin Refunds Success 
   [Documentation]  接口名:获取退款${\n}
   ...              请求方式:Get${\n}
   ...              预期结果:输入正确参数,http响应码返回 200,返回的Json数据为 Refund 列表。
   [Tags]           Respcode:200
   ${essential_params}  create list  order_id=${order_id}  
   ${unessential_params}  create list  
   run every case by params  Get Admin Refunds Success 200  ${essential_params}  ${unessential_params}

Get Admin Refunds Fail With Wrong Params
   [Documentation]  接口名:获取退款${\n}
   ...              请求方式:Get${\n}
   ...              预期结果:输入错误参数,http响应码返回 422,返回的Json数据为错误信息。
   [Tags]           Respcode:422
   ${essential_params}  create list  order_id=${order_id_422}  
   ${unessential_params}  create list  
   run every case by params  Get Admin Refunds Fail 422  ${essential_params}  ${unessential_params}


*** Keywords ***
Get Admin Refunds Success 200
   [Arguments]  &{kwargs}
   ${resp}=  Get Admin Refunds   &{kwargs}
   expect status is 200  ${resp}  admin_refund/Get_Admin_Refunds_200.json

Get Admin Refunds Fail 422
   [Arguments]  &{kwargs}
   ${resp}=  Get Admin Refunds   &{kwargs}
   expect status is 422  ${resp}  

