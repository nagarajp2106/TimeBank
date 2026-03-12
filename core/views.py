from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.utils import timezone
from .models import User, Wallet, Course, Enrollment, Transaction
from .forms import SignupForm, LoginForm, CourseForm


# ─── Landing ────────────────────────────────────────────────────────────────────

def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/landing.html')


# ─── Auth ────────────────────────────────────────────────────────────────────────

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Wallet.objects.create(user=user, balance=50)
            login(request, user)
            messages.success(request, f'Welcome to TimeBank, {user.username}! You have 50 Time Coins to get started.')
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('landing')


# ─── Dashboard Router ────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    if request.user.is_instructor:
        return redirect('instructor_dashboard')
    return redirect('learner_dashboard')


# ─── Instructor Dashboard ────────────────────────────────────────────────────────

@login_required
def instructor_dashboard(request):
    if not request.user.is_instructor:
        return redirect('learner_dashboard')

    user = request.user
    courses = Course.objects.filter(instructor=user)
    wallet = user.wallet

    # Stats
    total_courses = courses.count()
    total_students = Enrollment.objects.filter(course__instructor=user, status='approved').count()
    pending_requests = Enrollment.objects.filter(course__instructor=user, status='pending')
    coins_earned = Transaction.objects.filter(receiver=user).aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'courses': courses,
        'wallet': wallet,
        'total_courses': total_courses,
        'total_students': total_students,
        'pending_requests': pending_requests,
        'coins_earned': coins_earned,
    }
    return render(request, 'core/instructor_dashboard.html', context)


# ─── Course CRUD ──────────────────────────────────────────────────────────────────

@login_required
def create_course(request):
    if not request.user.is_instructor:
        messages.error(request, 'Only instructors can create courses.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, f'Course "{course.title}" created successfully!')
            return redirect('instructor_dashboard')
    else:
        form = CourseForm()
    return render(request, 'core/course_form.html', {'form': form, 'action': 'Create'})


@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f'Course "{course.title}" updated successfully!')
            return redirect('instructor_dashboard')
    else:
        form = CourseForm(instance=course)
    return render(request, 'core/course_form.html', {'form': form, 'action': 'Edit', 'course': course})


@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        title = course.title
        course.delete()
        messages.success(request, f'Course "{title}" deleted.')
        return redirect('instructor_dashboard')
    return render(request, 'core/confirm_delete.html', {'course': course})


# ─── Enrollment Management ──────────────────────────────────────────────────────

@login_required
def manage_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, course__instructor=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'approve' and enrollment.status == 'pending':
            learner_wallet = enrollment.learner.wallet
            instructor_wallet = request.user.wallet
            cost = enrollment.course.cost

            if learner_wallet.balance < cost:
                messages.error(request, f'{enrollment.learner.username} does not have enough Time Coins.')
                return redirect('instructor_dashboard')

            # Transfer coins
            learner_wallet.balance -= cost
            learner_wallet.save()
            instructor_wallet.balance += cost
            instructor_wallet.save()

            # Update enrollment
            enrollment.status = 'approved'
            enrollment.resolved_at = timezone.now()
            enrollment.save()

            # Create transaction
            Transaction.objects.create(
                sender=enrollment.learner,
                receiver=request.user,
                enrollment=enrollment,
                amount=cost,
                description=f'Enrollment in "{enrollment.course.title}"',
            )

            messages.success(request, f'Enrollment approved! {cost} coins received.')

        elif action == 'reject' and enrollment.status == 'pending':
            enrollment.status = 'rejected'
            enrollment.resolved_at = timezone.now()
            enrollment.save()
            messages.info(request, 'Enrollment request rejected.')

    return redirect('instructor_dashboard')


# ─── Learner Dashboard ──────────────────────────────────────────────────────────

@login_required
def learner_dashboard(request):
    if not request.user.is_learner:
        return redirect('instructor_dashboard')

    user = request.user
    wallet = user.wallet
    enrolled_courses = Enrollment.objects.filter(learner=user, status='approved')
    pending_requests = Enrollment.objects.filter(learner=user, status='pending')
    coins_spent = Transaction.objects.filter(sender=user).aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'wallet': wallet,
        'enrolled_courses': enrolled_courses,
        'pending_requests': pending_requests,
        'coins_spent': coins_spent,
        'enrolled_count': enrolled_courses.count(),
    }
    return render(request, 'core/learner_dashboard.html', context)


# ─── Marketplace ─────────────────────────────────────────────────────────────────

@login_required
def marketplace(request):
    courses = Course.objects.all()
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(instructor__username__icontains=query)
        )
    if category:
        courses = courses.filter(category=category)

    categories = Course.CATEGORY_CHOICES

    context = {
        'courses': courses,
        'query': query,
        'selected_category': category,
        'categories': categories,
    }
    return render(request, 'core/marketplace.html', context)


# ─── Course Detail ───────────────────────────────────────────────────────────────

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user

    is_enrolled = False
    enrollment_status = None
    if user.is_learner:
        enrollment = Enrollment.objects.filter(course=course, learner=user).first()
        if enrollment:
            is_enrolled = enrollment.status == 'approved'
            enrollment_status = enrollment.status

    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'enrollment_status': enrollment_status,
        'embed_url': course.get_youtube_embed_url(),
    }
    return render(request, 'core/course_detail.html', context)


# ─── Enroll ──────────────────────────────────────────────────────────────────────

@login_required
def enroll_course(request, course_id):
    if not request.user.is_learner:
        messages.error(request, 'Only learners can enroll in courses.')
        return redirect('marketplace')

    course = get_object_or_404(Course, id=course_id)

    if course.instructor == request.user:
        messages.error(request, "You can't enroll in your own course.")
        return redirect('course_detail', course_id=course.id)

    # Check if already enrolled or pending
    existing = Enrollment.objects.filter(course=course, learner=request.user).first()
    if existing:
        messages.warning(request, f'You already have a {existing.status} enrollment for this course.')
        return redirect('course_detail', course_id=course.id)

    # Check balance
    if request.user.wallet.balance < course.cost:
        messages.error(request, 'You do not have enough Time Coins for this course.')
        return redirect('course_detail', course_id=course.id)

    if request.method == 'POST':
        Enrollment.objects.create(course=course, learner=request.user, status='pending')
        messages.success(request, 'Enrollment request sent! Waiting for instructor approval.')
        return redirect('learner_dashboard')

    return redirect('course_detail', course_id=course.id)


# ─── My Courses (Learner) ───────────────────────────────────────────────────────

@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(learner=request.user, status='approved').select_related('course', 'course__instructor')
    return render(request, 'core/my_courses.html', {'enrollments': enrollments})


# ─── Wallet ──────────────────────────────────────────────────────────────────────

@login_required
def wallet_view(request):
    wallet = request.user.wallet
    sent = Transaction.objects.filter(sender=request.user)
    received = Transaction.objects.filter(receiver=request.user)
    # Combine and sort
    transactions = sorted(
        list(sent) + list(received),
        key=lambda t: t.timestamp,
        reverse=True
    )
    total_earned = received.aggregate(total=Sum('amount'))['total'] or 0
    total_spent = sent.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'wallet': wallet,
        'transactions': transactions,
        'total_earned': total_earned,
        'total_spent': total_spent,
    }
    return render(request, 'core/wallet.html', context)
