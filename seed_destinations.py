import os
import json
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'balaji_holidays.settings')
import django
django.setup()

from destinations.models import Destination

if not Destination.objects.exists():
    Destination.objects.create(
        name='Santorini',
        country='Greece',
        description='A postcard-perfect island known for caldera sunsets, whitewashed villages, and romantic stays.',
        short_description='Sunset views, cliffside stays, and unforgettable dinners.',
        price_per_person=Decimal('1290.00'),
        rating=Decimal('4.8'),
        categories=json.dumps(['Island', 'Beach', 'Romantic']),
        image_url='https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?auto=format&fit=crop&w=900&q=80',
        is_featured=True,
        is_popular=True,
        best_season='May - October',
        language='Greek',
        currency='EUR',
    )
    Destination.objects.create(
        name='Kyoto',
        country='Japan',
        description='A timeless city of temples, tea houses, gardens, and seasonal festivals.',
        short_description='Culture-rich streets, gardens, and traditional cuisine.',
        price_per_person=Decimal('1180.00'),
        rating=Decimal('4.7'),
        categories=json.dumps(['City', 'Culture', 'Food']),
        image_url='https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=900&q=80',
        is_featured=True,
        is_popular=True,
        best_season='March - May',
        language='Japanese',
        currency='JPY',
    )
    Destination.objects.create(
        name='Marrakech',
        country='Morocco',
        description='A sensory-rich destination blending souks, riads, and desert adventures.',
        short_description='Colorful streets, rich food, and timeless architecture.',
        price_per_person=Decimal('980.00'),
        rating=Decimal('4.6'),
        categories=json.dumps(['City', 'Culture', 'Adventure']),
        image_url='https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=900&q=80',
        is_featured=False,
        is_popular=True,
        best_season='October - April',
        language='Arabic',
        currency='MAD',
    )
    Destination.objects.create(
        name='Queenstown',
        country='New Zealand',
        description='A dramatic alpine playground with lakes, adventure sports, and breathtaking scenery.',
        short_description='Adventure, lakeside views, and luxury lodges.',
        price_per_person=Decimal('1450.00'),
        rating=Decimal('4.9'),
        categories=json.dumps(['Adventure', 'Nature', 'Scenic']),
        image_url='https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=900&q=80',
        is_featured=True,
        is_popular=True,
        best_season='December - March',
        language='English',
        currency='NZD',
    )

print('Destination count:', Destination.objects.count())
