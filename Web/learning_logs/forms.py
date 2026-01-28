from django import forms

from .models import Topic, Entry, PublicEntry, PublicTopic

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

class PublicTopicForm(forms.ModelForm):
    class Meta:
        model = PublicTopic
        fields = ['text']
        labels = {'text': ''}

class PublicEntryForm(forms.ModelForm):
    class Meta:
        model = PublicEntry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}