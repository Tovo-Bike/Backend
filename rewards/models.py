from django.db import models

class Title(models.Model):
    WORK = (('T', 'Taker'), ('R', 'Rider'))
    name = models.CharField(max_length=64)
    price = models.IntegerField()
    job = models.CharField(max_length=1, choices=WORK)
    image = models.ImageField(upload_to='titles')

    def __str__(self):
        return self.name