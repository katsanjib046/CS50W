from django import forms
from .models import Category

class CreateListing(forms.Form):
    listing_name = forms.CharField(label="Item's name", max_length=100)
    starting_bid = forms.IntegerField(label="Starting Price in USD")
    image = forms.ImageField()
    description = forms.CharField(widget=forms.Textarea)

    # make a select button
    categoryChoices = [(item.name, item.name) for item in Category.objects.all().order_by("name")]
    category = forms.CharField(label="Category",widget=forms.Select(choices=categoryChoices))