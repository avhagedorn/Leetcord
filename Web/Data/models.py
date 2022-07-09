from django.db import models

# Create your models here.
class Member(models.Model):
    discordID = models.BigIntegerField()
    discordName = models.CharField(max_length=35)
    discordPFP = models.URLField()
    date_verified = models.DateField(auto_now_add=True)

class Problem(models.Model):
    class DIFFICULTY_CHOICES(models.IntegerChoices):
        EASY = 0, "Easy"
        MEDIUM = 1, "Medium"
        HARD = 2, "Hard"
    problem_number = models.SmallIntegerField()
    slug = models.CharField(max_length=200)
    difficulty = models.SmallIntegerField(choices=DIFFICULTY_CHOICES.choices)

class Solve(models.Model):
    solvee = models.ForeignKey("Member",related_name="Solves",on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    problem = models.ForeignKey("Problem", related_name="Solves",on_delete=models.CASCADE)
    takeaway = models.CharField(max_length=255)
