from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=100)
    height = models.FloatField()
    weight = models.FloatField()
    age = models.IntegerField()
    skills = models.JSONField()  # נניח שנשמור את המיומנויות בפורמט JSON

    def __str__(self):
        return self.name

