from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):

    """ Create Review Form Definition """

    class Meta:
        model = models.Review
        fields = (
            "reivew",
            "cleanliness",
            "accuracy",
            "communication",
            "location",
            "check_in",
            "value",
        )

    def save(self):
        review = super().save(commit=False)
        return review
