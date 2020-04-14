#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django import forms
from django_redis import get_redis_connection
import random
from platforms.models import AccountInfo
from utils.sms import send_sms_single


class RegisterModelForm(forms.ModelForm):
    username = forms.CharField(label='用户名', widget=forms.TextInput())
    email = forms.CharField(label='邮箱', widget=forms.EmailInput())
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        label='确认密码', widget=forms.PasswordInput())
    mobile_phone = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误')]
    )
    code = forms.CharField(label='验证码', widget=forms.TextInput())

    class Meta:
        model = AccountInfo
        # fields = '__all__'
        fields = ['username', 'email', 'password',
                  'confirm_password', 'mobile_phone', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class SmsSendForm(forms.Form):
    mobile_phone = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误')]
    )

    def clean_mobile_phone(self):
        """ 手机号校验钩子函数 """
        mobile_phone = self.cleaned_data['mobile_phone']

        # 校验短信模板
        sms_type = self.data.get('sms_type')
        template_id = settings.TENCENT_SMS_TEMPLATE_IDS.get(sms_type)
        if not template_id:
            raise ValidationError('不存在当前类型的短信模板')

        # 校验数据库中手机号是否已存在
        is_exists = AccountInfo.objects.filter(
            mobile_phone=mobile_phone).exists()
        if is_exists:
            raise ValidationError('手机号已存在！')

        # 发短信验证码
        code = random.randrange(100000, 999999)
        res = send_sms_single(mobile_phone, template_id, [code, ])
        if res['result'] != 0:
            raise ValidationError('短信发送失败：{}'.format(res['errmsg']))

        # 将验证码写入Redis
        conn = get_redis_connection()
        conn.set(mobile_phone, code, ex=60 * 2)

        return mobile_phone
