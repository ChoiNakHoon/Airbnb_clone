from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.
@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


# Inline-Admin
# Admin 안에 FK로 묶인 Admin을 넣을 수 있음?
class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """ Room Admin Definition """

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "host",
                    "name",
                    "description",
                    "contry",
                    "city",
                    "address",
                    "price",
                    "room_type",
                )
            },
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")},),
        (
            "More About the Space",
            {"fields": ("amenities", "facilities", "house_rule")},
        ),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths",)}),
    )
    list_display = (
        "name",
        "contry",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rule",
        "city",
    )

    raw_id_fields = ("host",)

    search_fields = ("^city", "^host__username")

    filter_horizontal = ("amenities", "facilities", "house_rule")

    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    # mark_safe
    # html 코드를 직접 넣기 위한 방법
    # 위 기능을 사용하지 않으면 장고에서 html tag 및 script 를 사용 할 수 없음
    # safety 하기 때문에 (해킹 방지)
    def get_thumbnail(self, obj):
        return mark_safe('<img width="100px" src="{}"/>'.format(obj.file.url))

    get_thumbnail.short_description = "Thumbnail"
