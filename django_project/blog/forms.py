from django import forms
from django.contrib.auth.models import User

list_of_choices = (
    (1, 'summarization'),
    (2, 'generation'),
    (3, 'sentiment'),
    (4, 'QnA')
)

class NLPForm(forms.Form):
    input_text = forms.CharField(widget=forms.Textarea)
    what_to_do = forms.ChoiceField(choices=list_of_choices)
    question = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Input a Question here if QnA selected.'}))


    # class Meta:
    #     fields = ['input_text', 'what_to_do']