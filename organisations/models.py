from django.db import models
import uuid

from users.models import User

class Organisation(models.Model):
    orgId = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class UserOrganisation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'organisation')
        
    def __str__(self):
        return f'{self.user.firstName}-{self.organisation}'
