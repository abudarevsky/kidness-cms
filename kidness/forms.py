# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from django import forms
from contact_form import forms as lfc_forms
import lfc.utils

class KidnessContactForm(lfc_forms.ContactForm):
    phone_number = forms.CharField(max_length=20,
                     widget=forms.TextInput(attrs=lfc_forms.attrs_dict),
                     label=_(u'*Номер телефона'), required =True)
    program = forms.CharField(max_length=1024, widget=forms.widgets.HiddenInput())
    def __init__ (self, *args, **kwargs):
        super(KidnessContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].label=_(u'*Ваше имя')
        self.fields['email'].label=_(u'Адрес электронной почты')
        self.fields['email'].required=False
        self.fields['time'] = forms.CharField(max_length=15,
                     widget=forms.TextInput(),
                     label=_(u'Предпочитаемое время звонка'), required=False)
        self.fields['body']=forms.CharField(widget=forms.Textarea(attrs={'cols':20,'rows':5}),
                              label=_(u'Комментарии'), required=False)
        self.fields.keyOrder = [
            'name',
            'phone_number',
            'time',
            'email',
            'body',
            'program'
        ]

        self.portal = lfc.utils.get_portal()
    
    def from_email(self):
        return self.portal.from_email

    def recipient_list(self):
        return self.portal.get_notification_emails()    
        
        
        