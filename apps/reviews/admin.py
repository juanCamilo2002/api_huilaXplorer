from django.contrib import admin
from django import forms
from .models import Review
# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'tourist_spot', 'rating', 'comment', 'created_at', 'updated_at']
    search_fields = ['user', 'tourist_spot']
    list_filter = ['rating', 'created_at', 'updated_at']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
        }


class ReviewTabularInline(admin.TabularInline):
    model = Review
    extra = 0
    form = ReviewForm


admin.site.register(Review, ReviewAdmin)