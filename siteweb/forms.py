
from django import forms
from .models import Review, Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {'title': 'Titre', 'description': 'Description'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 7})}


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[("0", "0"), ("1", "1"), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], required=False)

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {'headline': 'Titre', 'rating': 'Note', 'body': 'Commentaire'}
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.RadioSelect(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 7})}


class SearchUser(forms.Form):
    search_user = forms.CharField(max_length=20, required=True, label='Nom utilisateur',
                                  widget=forms.TextInput(attrs={'placeholder': 'Recherche utilisateur'}))
