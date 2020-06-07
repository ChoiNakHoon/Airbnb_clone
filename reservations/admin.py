from django.contrib import admin
from . import models


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):

    """ Reservation Admin Definition """

    list_display = (
        "room",
        "check_in",
        "check_out",
        "guest",
        "is_progress",
        "is_finished",
    )


@admin.register(models.BookedDays)
class BookedDaysAdmin(admin.ModelAdmin):

    """ BookedDay Admin Definition """

    list_display = (
        "day",
        "reservation",
    )
