from django import forms

from user.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dating_sex', 'location', 'min_distance', 'max_distance',
                  'min_dating_age', 'max_dating_age', 'vibration',
                  'only_matche', 'auto_play']

    def clean_max_distance(self):
        cleaned = super().clean()
        if cleaned['min_distance'] > cleaned['max_distance']:
            raise forms.ValidationError('min_distance 必须小于 max_distance')
        return cleaned['max_distance']

    def clean_max_dating_age(self):
        cleaned = super().clean()
        if cleaned['min_dating_age'] > cleaned['max_dating_age']:
            raise forms.ValidationError('min_dating_age 必须小于 max_dating_age')
        return cleaned['max_dating_age']
