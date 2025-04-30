from django.db import models
from command.models import BaseModel
from users.models import User
from courses.models import Course
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()

    class Meta:
        unique_together = ['user', 'course']