from django.db import models

class Location(models.Model):
    longtitude = models.DecimalField(max_digits=9, decimal_places=3)
    latitude = models.DecimalField(max_digits=9, decimal_places=3)
    description = models.CharField(max_length=128)

    def __str__(self):
        return self.description


class Trip(models.Model):
    taker = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="taker", null=True)
    rider = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="rider")
    depart_lon = models.DecimalField(max_digits=9, decimal_places=6)
    depart_lat = models.DecimalField(max_digits=9, decimal_places=6)
    dest_lon = models.DecimalField(max_digits=9, decimal_places=6)
    dest_lat = models.DecimalField(max_digits=9, decimal_places=6)
    taker_score = models.IntegerField(null=True)
    rider_score = models.IntegerField(null=True)
    start_time = models.DateTimeField(null=True)
    arrival_time = models.DateTimeField(null=True)

    def __str__(self):
        return "{} takes {}".format(self.taker, self.rider)


class Report(models.Model):
    transaction = models.ForeignKey('Trip', on_delete=models.CASCADE, related_name="transaction")
    context = models.CharField(max_length=128)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.context)[:10]

