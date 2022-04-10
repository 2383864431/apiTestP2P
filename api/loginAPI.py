import app
import requests

class loginAPI():
    # 初始化每个接口的接口地址
    # app.BASE_URL是每个接口的公共访问地址，在app.py中定义
    def __init__(self):
        self.getImgCode_url = app.BASE_URL +'/common/public/verifycode1/'#获取图片验证码的接口URL
        self.getSmsCode_url = app.BASE_URL + '/member/public/sendSms'#获取短信验证码的接口URL
        self.register_url = app.BASE_URL + '/member/public/reg'#获取注册的接口URL
        self.login_url = app.BASE_URL + '/member/public/login'#获取登录的接口URL
    # 定义发送图片验证码的接口的函数，该函数的返回值为发送图片验证码的接口地址
    def getImgCode(self,session,r):
        # 定义获取图片验证码的域名(URL+参数)
        url = self.getImgCode_url + r
        response = session.get(url)
        return response
    # 函数返回获取到的浏览器地址(URL+参数)

    def getSmsCode(self,session,phone,imgVerifyCode):
        #准备参数
        data = {'phone': phone,'imgVerifyCode': imgVerifyCode ,'type':'reg'}
        #发送请求
        response = session.post(self.getSmsCode_url,data=data)
        #返回响应
        return response

    def register(self,session,phone,pwd,imgVerifyCode='8888',phoneCode='666666',dyServer='on',invite_phone=''):
        data = {"phone": phone,
                "password": pwd,
                "verifycode": imgVerifyCode,
                "phone_code": phoneCode,
                "dy_server": dyServer,
                'invite_phone':invite_phone}
        response = session.post(self.register_url,data=data)
        return response

    def login(self,session,phone='13033447711',pwd='test123'):
        data = {"keywords": phone,"password": pwd}
        response = session.post(self.login_url,data=data)
        return response