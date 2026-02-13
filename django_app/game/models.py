from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Play(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    story_id = models.IntegerField()
    
    ending_page_id = models.IntegerField()
    
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Story ID {self.story_id} played at {self.created_at} by {self.user.username}"
    
class Review(models.Model):
    story_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate from 1 to 5 stars"
    )
    text = models.TextField(blank=True, help_text="Optional comment")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('story_id', 'user')

    def __str__(self):
        return f"Review by {self.user.username} on Story {self.story_id}"