from django.db import models


class CustomReservationManager(models.Manager):

    """ CustomREservation Manager Difinition """

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.models.DoesNotExists:
            return None
