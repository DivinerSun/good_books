"""
用户相关业务：注册、登录、短信验证码、注销等等
"""

from django.shortcuts import render
from django.http import JsonResponse
from platforms.forms.account import RegisterModelForm, SmsSendForm


def sms_send(request):
    """
    发送短信
    :param request:
    :return:
    """
    form = SmsSendForm(data=request.GET)
    if form.is_valid():
        return JsonResponse({'status': True, 'msg': '短信发送成功'})

    return JsonResponse({'status': False, 'msg': '短信发送失败', 'error': form.errors})


def register(request):
    """
    用户注册
    :param request:
    :return:
    """
    form = RegisterModelForm()
    return render(request, 'register.html', {'form': form})
