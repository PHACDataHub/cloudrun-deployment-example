from django.db import models



class City(models.Model):
    city = models.CharField(max_length=100, primary_key=True)
    # description = models.TextField
    description = models.CharField(max_length=400)
    # city_image = models.ImageField(upload_to='images/', None=True)
   
    def __str__(self):
            return self.city


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)

