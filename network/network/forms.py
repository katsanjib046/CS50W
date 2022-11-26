from django import forms

class PostForm(forms.Form):
    postContent = forms.CharField(label="", widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class CommentForm(forms.Form):
    commentText = forms.CharField(label="Comment", widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

