from django.db import models

class User(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=16)
    email = models.EmailField()
    weight = models.IntegerField(default=60)
    rose = models.IntegerField(default=0)
    gear = models.IntegerField(default=0)
    coin = models.IntegerField(default=0)
    reg_time = models.DateField(auto_now_add=True)
    title_equipped = models.ForeignKey('rewards.Title', on_delete=models.DO_NOTHING, related_name="title_euipped", null=True)
    titles_had = models.ManyToManyField('rewards.Title', related_name="titles_had")
    favorites = models.ManyToManyField('trips.Location', related_name="favorite_places")

    def __str__(self):
        return self.name