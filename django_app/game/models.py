from django.db import models
from django.utils import timezone

# Create your models here.
class Play(models.Model):
    story_id = models.IntegerField()
    
    ending_page_id = models.IntegerField()
    
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Story ID {self.story_id} played at {self.created_at}"