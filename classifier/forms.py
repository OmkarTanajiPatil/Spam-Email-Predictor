from django import forms
class MailForm(forms.Form):
    message = forms.CharField(
        label='Email content',
        widget=forms.Textarea(attrs={'rows': 8, 'placeholder': 'Paste the email body here...'}),
        max_length=5000,
    )
