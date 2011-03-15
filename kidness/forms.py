# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from django import forms
from contact_form import forms as lfc_forms
import lfc.utils

class KidnessContactForm(lfc_forms.ContactForm):
    phone_number = forms.CharField(max_length=12,
                     widget=forms.TextInput(attrs=lfc_forms.attrs_dict),
                     label=_(u'Номер телефона'))
                           
    def __init__ (self, *args, **kwargs):
        super(KidnessContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].label=_(u'Ваше имя')
        self.fields['body'] = forms.CharField(max_length=15,
                     widget=forms.TextInput(attrs=lfc_forms.attrs_dict),
                     label=_(u'Предпочитаемое время звонка'))
        self.portal = lfc.utils.get_portal()
        
    def from_email(self):
        return self.portal.from_email

    def recipient_list(self):
        return self.portal.get_notification_emails()    
        
        
        