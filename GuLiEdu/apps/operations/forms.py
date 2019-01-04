import re

from django import forms
from .models import UserAsk


# class UserAskForm(forms.Form):
class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        # exclude = ['add_time']
        fields = ['name', 'course', 'phone']

        # fields = '__all__'

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # 匹配合法的手机号
        com = re.compile('^1([358][0-9]|4[579]|66|7[0135678]|9[89])[0-9]{8}$')
        # match 从头匹配,如果开始匹配错误,return None
        # search 如果匹配错误,会接着查找,直到找到合适的,全部不合适,才return None 两者均只返回一次
        if com.match(phone):
            return phone
        else:
            raise forms.ValidationError('输入的手机号码不合法')


class UserCommentForm(forms.Form):
    comment_course = forms.IntegerField(required=True)
    comment_content = forms.CharField(required=True, min_length=1, max_length=300)
