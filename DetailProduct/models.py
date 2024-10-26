from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from Homepage.models import Phone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_user')
    product = models.ForeignKey(Phone, on_delete=models.CASCADE, related_name='product_reviews')
    content = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    date_added = models.DateTimeField(default=timezone.now)
    last_edited = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.rating}/5 for {self.product}"
    
    def save(self, *args, **kwargs):
        if self.pk:  
            self.last_edited = timezone.now()
        super().save(*args, **kwargs)
        

@receiver(post_save, sender=Review)
def update_phone_rating(sender, instance, created, **kwargs):
    phone = instance.product
    if created:
        if instance.rating == 1:
            phone.one_star += 1
        elif instance.rating == 2:
            phone.two_star += 1
        elif instance.rating == 3:
            phone.three_star += 1
        elif instance.rating == 4:
            phone.four_star += 1
        elif instance.rating == 5:
            phone.five_star += 1
    else:
        old_rating = instance.__class__.objects.get(pk=instance.pk).rating
        if old_rating != instance.rating:
            if old_rating == 1:
                phone.one_star -= 1
            elif old_rating == 2:
                phone.two_star -= 1
            elif old_rating == 3:
                phone.three_star -= 1
            elif old_rating == 4:
                phone.four_star -= 1
            elif old_rating == 5:
                phone.five_star -= 1
            if instance.rating == 1:
                phone.one_star += 1
            elif instance.rating == 2:
                phone.two_star += 1
            elif instance.rating == 3:
                phone.three_star += 1
            elif instance.rating == 4:
                phone.four_star += 1
            elif instance.rating == 5:
                phone.five_star += 1

    phone.save()

@receiver(pre_delete, sender=Review)
def remove_phone_rating(sender, instance, **kwargs):
    phone = instance.product
    if instance.rating == 1:
        phone.one_star -= 1
    elif instance.rating == 2:
        phone.two_star -= 1
    elif instance.rating == 3:
        phone.three_star -= 1
    elif instance.rating == 4:
        phone.four_star -= 1
    elif instance.rating == 5:
        phone.five_star -= 1

    phone.save()
