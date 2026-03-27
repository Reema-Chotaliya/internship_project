# Create your models here.
from django.db import models
from django.conf import settings
# Create your models here.
class business(models.Model):
    APPROVAL_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    business_name = models.CharField(max_length=150)
    description = models.TextField()
    category = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)

    views_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "business"

    def __str__(self):
        return self.business_name


class Review(models.Model):
    business = models.ForeignKey(business, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_replied = models.BooleanField(default=False)

    class Meta:
        db_table = 'review'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.business} ({self.rating})"

    @property
    def star_rating(self):
        full_stars = min(5, int(self.rating))
        half_star = 1 if (self.rating - full_stars >= 0.5) else 0
        empty_stars = 5 - full_stars - half_star
        return '★' * full_stars + ('½' if half_star else '') + '☆' * empty_stars


class Inquiry(models.Model):
    business = models.ForeignKey(business, on_delete=models.CASCADE, related_name='inquiries')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inquiry'
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry for {self.business} by {self.user}"


class promotion(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('expired', 'Expired'),
    )

    business = models.ForeignKey(business, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    discount_percent = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    class Meta:
        db_table = "promotion"

    def __str__(self):
        return self.title


class ViewTracking(models.Model):
    """Track individual page views for analytics"""
    business = models.ForeignKey(business, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'view_tracking'
        indexes = [
            models.Index(fields=['business', 'created_at']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.business} - {self.created_at}"