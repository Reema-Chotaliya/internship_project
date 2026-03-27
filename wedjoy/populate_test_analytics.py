"""
ANALYTICS TEST DATA GENERATOR
Run: python manage.py shell < populate_test_analytics.py
"""

from django.utils import timezone
from datetime import timedelta
from business.models import ViewTracking, business, Review, Inquiry
from core.models import User
from random import randint, choice
import sys

# Get or create test owner
owner, created = User.objects.get_or_create(
    username='testowner',
    defaults={'email': 'testowner@test.com', 'role': 'owner'}
)

# Get owner's businesses
owner_businesses = business.objects.filter(owner_id=owner)

if not owner_businesses.exists():
    print("❌ No businesses found for owner. Creating test business...")
    test_business = business.objects.create(
        owner_id=owner,
        business_name="Test Business Co.",
        description="Test business for analytics",
        category="Services",
        contact_number="1234567890",
        email="test@business.com",
        address="123 Main St",
        latitude=0.0,
        longitude=0.0,
        approval_status='approved'
    )
    owner_businesses = business.objects.filter(owner_id=owner)

print(f"📊 Found {owner_businesses.count()} businesses for owner '{owner.username}'")

# ============ POPULATE VIEW TRACKING DATA ============

print("\n📈 Generating ViewTracking data (90 days)...")

view_count = 0
for business_obj in owner_businesses:
    # Random views per day distribution
    for day_offset in range(90):
        # Random number of views per day (0-20)
        views_per_day = randint(5, 25)
        
        for _ in range(views_per_day):
            # Random time within the day
            hour = randint(0, 23)
            minute = randint(0, 59)
            
            ViewTracking.objects.create(
                business=business_obj,
                user=choice([owner, None]),  # Some anonymous
                session_id=f"session_{day_offset}_{randint(0, 1000)}",
                created_at=timezone.now() - timedelta(
                    days=day_offset,
                    hours=hour,
                    minutes=minute
                )
            )
            view_count += 1

print(f"✅ Created {view_count} view records")

# ============ POPULATE REVIEW DATA ============

print("\n⭐ Generating Review data...")

review_count = 0
reviewers = User.objects.filter(role='user')[:10]

for business_obj in owner_businesses:
    # 5-15 reviews per business over 90 days
    for _ in range(randint(5, 15)):
        reviewer = choice(reviewers) if reviewers.exists() else owner
        
        Review.objects.create(
            business=business_obj,
            user=reviewer,
            rating=float(randint(2, 5) + randint(0, 1) * 0.5),
            review_text=f"Great service! Rating for {business_obj.business_name}.",
            created_at=timezone.now() - timedelta(days=randint(0, 90))
        )
        review_count += 1

print(f"✅ Created {review_count} review records")

# ============ POPULATE INQUIRY DATA ============

print("\n❓ Generating Inquiry data...")

inquiry_count = 0
for business_obj in owner_businesses:
    # 3-10 inquiries per business over 90 days
    for _ in range(randint(3, 10)):
        inquirer = choice(reviewers) if reviewers.exists() else owner
        
        Inquiry.objects.create(
            business=business_obj,
            user=inquirer,
            message=f"Are you available for {business_obj.category}?",
            created_at=timezone.now() - timedelta(days=randint(0, 90))
        )
        inquiry_count += 1

print(f"✅ Created {inquiry_count} inquiry records")

# ============ SUMMARY ============

print("\n" + "="*50)
print("📊 ANALYTICS DATA GENERATION SUMMARY")
print("="*50)
print(f"Owner: {owner.username}")
print(f"Businesses: {owner_businesses.count()}")
print(f"Views: {ViewTracking.objects.filter(business__in=owner_businesses).count()}")
print(f"Reviews: {Review.objects.filter(business__in=owner_businesses).count()}")
print(f"Inquiries: {Inquiry.objects.filter(business__in=owner_businesses).count()}")
print("="*50)
print("✅ Dashboard ready! Visit: /dashboard/analyticsbusiness/")
print("="*50)
