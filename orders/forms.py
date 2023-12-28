from django import forms
from phonenumber_field.formfields import PhoneNumberField


class CreateOrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone_number = PhoneNumberField(required=False)
    requires_delivery = forms.ChoiceField(
        choices=[
            ("0", False),
            ("1", True),
        ],
    )
    shipping_address = forms.CharField(required=False)
    city = forms.CharField(required=False)
    country = forms.CharField(required=False)
    zipcode = forms.IntegerField(required=False)
    payment_on_get = forms.ChoiceField(
        choices=[
            ("0", 'False'),
            ("1", 'True'),
        ],
    )
