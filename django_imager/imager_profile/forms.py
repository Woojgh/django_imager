from django import forms


class DocumentForm(forms.Form):
    image = forms.FileField(
        label='Select a file',
    )
