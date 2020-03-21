from django import forms

from backend.models import Article


class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'text', 'topic')

    def clean_title(self):
        title = self.cleaned_data['title']
        if title.startswith("a"):
            self.add_error('text', "Ne moze so a be!")
            # raise forms.ValidationError("Ne moze so 'ab'!")
        return title

    def clean_topic(self):
        topic = self.cleaned_data['topic']
        print(topic)
        return topic
