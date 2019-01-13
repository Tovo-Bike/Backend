from django.db import models

class User(models.Model):
    GENDER = (('M', 'Male'), ('F', "Female"))
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    email = models.EmailField()
    gender = models.CharField(max_length=1, choices=GENDER)
    weight = models.IntegerField(default=60)
    rose = models.IntegerField(default=0)
    gear = models.IntegerField(default=0)
    coin = models.IntegerField(default=0)
    score_as_taker = models.IntegerField(default=0)
    times_as_taker = models.IntegerField(default=0)
    score_as_rider = models.IntegerField(default=0)
    times_as_rider = models.IntegerField(default=0)
    reg_time = models.DateField(auto_now_add=True)
    title_equipped = models.ForeignKey('rewards.Title', on_delete=models.DO_NOTHING, related_name="title_euipped", blank=True, null=True)
    titles_had = models.ManyToManyField('rewards.Title', related_name="titles_had", blank=True)
    favorites = models.ManyToManyField('trips.Location', related_name="favorite_places", blank=True)

    def __str__(self):
        return self.name