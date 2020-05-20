from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    RATING_DEFAULT = 0
    RATING_ONE = 1
    RATING_TWO = 2
    RATING_THREE = 3
    RATING_FOUR = 4
    RATING_FIVE = 5
    RATING_CHOICES = (
        (RATING_DEFAULT, "I need some help!"),
        (RATING_ONE, "I'm really upset"),
        (RATING_TWO, "I've got a problem"),
        (RATING_THREE, "Things are pretty good"),
        (RATING_FOUR, "Feeling Great!"),
        (RATING_FIVE, "Fantistic"),
    )
    reivew = models.TextField()
    cleanliness = models.IntegerField(choices=RATING_CHOICES, default=RATING_DEFAULT)
    accuracy = models.IntegerField(choices=RATING_CHOICES, default=RATING_DEFAULT)
    communication = models.IntegerField(choices=RATING_CHOICES, default=RATING_DEFAULT)
    location = models.IntegerField(choices=RATING_CHOICES, default=RATING_DEFAULT)
    check_in = models.IntegerField(choices=RATING_CHOICES, default=RATING_DEFAULT)
    value = models.IntegerField(choices=RATING_CHOICES, default=RATING_DEFAULT)
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return "{0} - {1} From {2}".format(
            self.reivew, self.room.name, self.user.username
        )

    def rating_avg(self):
        avg = (
            self.cleanliness
            + self.accuracy
            + self.communication
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)
