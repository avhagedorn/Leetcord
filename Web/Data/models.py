from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete

# Create your models here.
class Member(models.Model):
    discordID = models.BigIntegerField(unique=True)
    discordName = models.CharField(max_length=35)
    discordPFP = models.URLField()
    date_verified = models.DateField(auto_now_add=True)
    num_solutions = models.SmallIntegerField(default=0)
    # Store num solutions in order to speed up leeterboard command.
    # Instead of searching solution and counting it, individually we can store the num completed here.

    def __str__(self) -> str:
        return f"Member {self.discordName} verified on {self.date_verified.strftime('%B %e, %Y')}"

class Problem(models.Model):
    class DIFFICULTY_CHOICES(models.IntegerChoices):
        EASY = 0, "Easy"
        MEDIUM = 1, "Medium"
        HARD = 2, "Hard"
    problem_number = models.SmallIntegerField(unique=True)
    problem_name = models.CharField(max_length=200)
    premium = models.BooleanField()
    slug = models.CharField(max_length=200)
    difficulty = models.SmallIntegerField(choices=DIFFICULTY_CHOICES.choices)


    def __str__(self) -> str:
        return f"Leetcode {self.problem_number}.) {self.problem_name} | {self.get_difficulty_display()}"


class Solve(models.Model):
    solvee = models.ForeignKey("Member",related_name="Solves",on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    problem = models.ForeignKey("Problem", related_name="Solves",on_delete=models.CASCADE)
    takeaway = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self) -> str:
        return f"{self.solvee.discordName}'s solution to {self.problem} on {self.date}"

    def save(self, *args, **kwargs) -> None:
        self.solvee.num_solutions += 1
        self.solvee.save()
        return super().save(*args, **kwargs)


@receiver(pre_delete, sender=Solve)
def decrement_deleted_solve(sender,instance,**kwargs):
    instance.solvee.num_solutions -= 1
    instance.solvee.save()


