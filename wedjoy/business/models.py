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

    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "business"

    def __str__(self):
        return self.business_name
    
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