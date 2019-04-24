*** Settings ***
Documentation  admin_wechat_reply
Resource  ../resources.robot
Library  robot_car_wash_server_library.wechat_reply.WechatReplyLibrary
Force Tags  model:admin_wechat_reply  虾洗后台


Post Admin Wachat Replys Fail Without Login
   [Documentation]  接口名:添加--公众号关注/自定义回复${\n}
   ...              请求方式:Post${\n}
   ...              预期结果:未登录,http响应码返回 403,无Json数据返回。
   [Tags]           Respcode:403
   ${essential_params}  create list  category=${category}  reply_type=${reply_type}  content=${content}  
   ${unessential_params}  create list  
   run every case by params  Post Admin Wachat Replys Fail 403  ${essential_params}  ${unessential_params}

Get Admin Wachat Replys Fail Without Login
   [Documentation]  接口名:查询--公众号关注/自定义回复${\n}
   ...              请求方式:Get${\n}
   ...              预期结果:未登录,http响应码返回 403,无Json数据返回。
   [Tags]           Respcode:403
    Get Admin Wachat Replys Fail 403

Put Admin Wachat Replys By Wechat Reply Id Fail Without Login
   [Documentation]  接口名:修改--公众号关注/自定义回复${\n}
   ...              请求方式:Put${\n}
   ...              预期结果:未登录,http响应码返回 403,无Json数据返回。
   [Tags]           Respcode:403
   ${essential_params}  create list  category=${category}  reply_type=${reply_type}  content=${content}  
   ${unessential_params}  create list  
   run every case by params  Put Admin Wachat Replys By Wechat Reply Id Fail 403  ${essential_params}  ${unessential_params}  wechat_reply_id=${wechat_reply_id}

Delete Admin Wachat Replys By Wechat Reply Id Fail Without Login
   [Documentation]  接口名:添删除--公众号关注/自定义回复${\n}
   ...              请求方式:Delete${\n}
   ...              预期结果:未登录,http响应码返回 403,无Json数据返回。
   [Tags]           Respcode:403
   Delete Admin Wachat Replys By Wechat Reply Id Fail 403  wechat_reply_id=${wechat_reply_id}

Post Admin Wachat Replys Fail 403
   [Arguments]  &{kwargs}
   ${resp}=  Post Admin Wachat Replys   &{kwargs}
   expect status is 403  ${resp}  

Get Admin Wachat Replys Fail 403
   [Arguments]  &{kwargs}
   ${resp}=  Get Admin Wachat Replys   &{kwargs}
   expect status is 403  ${resp}  

Put Admin Wachat Replys By Wechat Reply Id Fail 403
   [Arguments]  &{kwargs}
   ${resp}=  Put Admin Wachat Replys By Wechat Reply Id   &{kwargs}
   expect status is 403  ${resp}  

Delete Admin Wachat Replys By Wechat Reply Id Fail 403
   [Arguments]  &{kwargs}
   ${resp}=  Delete Admin Wachat Replys By Wechat Reply Id   &{kwargs}
   expect status is 403  ${resp}  

