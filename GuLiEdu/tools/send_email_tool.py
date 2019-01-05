from users.models import EmailVerifyCode

# from random import randrange
from random import choice
from django.core.mail import send_mail
from GuLiEdu.settings import EMAIL_FROM


def get_random_code(code_length):
    code_source = '1234567890qwertyuiopasdfghkjlzcxvbbnmQWERTYUIOOPASDFGHJKLZXCVBNM'
    code = ''
    for i in range(code_length):
        # 随机选择一个字符
        code += choice(code_source)
        # str = code_source[randrange(0, len(code_source)-1)]
        # code += str
        # print('$$$$$$$$$$$$$$', code)
    return code


def send_email_code(email, send_type):
    # 1, 创建邮箱验证码对象, 保存数据库, 用于以后做对比
    code = get_random_code(6)
    a = EmailVerifyCode()
    a.email = email
    a.send_type = send_type
    a.code = code
    a.save()

    # 2, 正式发邮件功能
    if send_type == 1:
        send_title = '欢迎注册人工智能小镇网站:'
        send_body = '请点击以下链接进行激活您的账号: \n' \
                    'http://127.0.0.1:8000/users/user_active/'+code
        send_mail(send_title, send_body, EMAIL_FROM, [email])

    if send_type == 2:
        send_title = '人工智能小镇网站密码重置系统:'
        send_body = '请点击以下链接进行重置您的密码: \n' \
                    'http://127.0.0.1:8000/users/user_reset/'+code
        send_mail(send_title, send_body, EMAIL_FROM, [email])

    if send_type == 3:
        send_title = '人工智能小镇网站修改邮箱验证码系统:'
        send_body = '您的验证码是:' + code
        send_mail(send_title, send_body, EMAIL_FROM, [email])