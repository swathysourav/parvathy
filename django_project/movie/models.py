from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    movie_name=models.CharField(max_length=250)
    movie_description=models.TextField()
    release_date = models.DateTimeField(default=timezone.now)
    movie_image=models.ImageField(null=True,blank=True,upload_to='gallery')
    movie_user=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    actors=models.CharField(max_length=250)
    youtube=models.CharField(max_length=250)
    def __str__(self):
        return self.movie_name
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})


class ReviewRating(models.Model):
    movie_title=models.ForeignKey(Post,null=True,on_delete=models.CASCADE)
    review_user=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    review=models.TextField(max_length=250)
    rating=models.FloatField(default=0)
    def __str__(self):
        return self.review_user
    def get_absolute_url(self):
        return reverse('post-review',kwargs={'pk':self.pk})
