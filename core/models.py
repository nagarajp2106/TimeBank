from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = [
        ('instructor', 'Instructor'),
        ('learner', 'Learner'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='learner')
    bio = models.TextField(blank=True, default='')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_instructor(self):
        return self.role == 'instructor'

    @property
    def is_learner(self):
        return self.role == 'learner'


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.IntegerField(default=50)

    def __str__(self):
        return f"{self.user.username}'s Wallet – {self.balance} coins"


class Course(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Programming'),
        ('design', 'Design'),
        ('music', 'Music'),
        ('language', 'Language'),
        ('fitness', 'Fitness'),
        ('cooking', 'Cooking'),
        ('photography', 'Photography'),
        ('business', 'Business'),
        ('marketing', 'Marketing'),
        ('other', 'Other'),
    ]

    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_created')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other')
    duration = models.CharField(max_length=50, help_text="e.g. '4 weeks', '10 hours'")
    cost = models.PositiveIntegerField(help_text="Time Coins required")
    youtube_url = models.URLField(blank=True, default='', help_text="YouTube video URL")
    notes = models.TextField(blank=True, default='', help_text="Course notes or additional resources")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def enrolled_count(self):
        return self.enrollments.filter(status='approved').count()

    @property
    def pending_count(self):
        return self.enrollments.filter(status='pending').count()

    def get_youtube_embed_url(self):
        """Convert a YouTube URL to an embeddable URL."""
        url = self.youtube_url
        if not url:
            return ''
        # Handle youtu.be short links
        if 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[-1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        # Handle youtube.com/watch?v= links
        if 'watch?v=' in url:
            video_id = url.split('watch?v=')[-1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        # Handle youtube.com/embed/ links (already embedded)
        if '/embed/' in url:
            return url
        return ''


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ['course', 'learner']
        ordering = ['-requested_at']

    def __str__(self):
        return f"{self.learner.username} → {self.course.title} ({self.status})"


class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_received')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.PositiveIntegerField()
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.amount} coins"
