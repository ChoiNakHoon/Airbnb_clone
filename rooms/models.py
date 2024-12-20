from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_countries.fields import CountryField
from core import models as core_models
from users import models as users_models
from cal import Calendar


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    # Room 유형를 나타내는 카테고리
    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ Room Model Definition """

    class Meta:
        verbose_name = "Room Type"


class Amenity(AbstractItem):

    """ Amenity Model Definition """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """ HouseRule Model Definition """

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Rooms Model Definition """

    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rule = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)
    latitude = models.CharField(max_length=20, default="37.2429359")
    longitude = models.CharField(max_length=20, default="131.8580873")
    likes = models.ManyToManyField("users.User", related_name="posts", blank=True)

    def __str__(self):
        return self.name

    def total_rating(self):
        all_reviews = self.reviews.all()
        total_avg = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                total_avg += review.rating_avg()
            return round(total_avg / len(all_reviews), 2)
        return 0

    total_rating.short_description = ".Avg"

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    # Admin side에 유용한 기능. 현재 index의 페이지로 이동
    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    # 각 room에서 첫번째 사진을 가져 옵니다.
    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]  # unpacking list
            return photo.file.url
        except ValueError:
            return None

    # Room에 4장의 사진을 가져 옵니다.
    def get_next_four_photo(self):
        photo = self.photos.all()[1:5]
        return photo

    def get_calendars(self):
        now = timezone.now()
        this_year = now.year
        this_month = now.month
        next_month = now.month + 1
        if this_month == 12:
            next_month = 1
        this_month_cal = Calendar(this_year, this_month)
        next_month_cal = Calendar(this_year, next_month)
        return [this_month_cal, next_month_cal]

    def get_likes_count(self):
        return self.likes.count()

    get_likes_count.short_description = "like_count"
