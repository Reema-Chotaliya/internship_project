from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib import messages

from .decorators import role_required
from .forms import OwnerProfileUpdateForm , EventProfileUpdateForm

from django.shortcuts import render
from django.db.models.functions import TruncMonth
from django.db.models import Count
from events.models import EventRegistration

from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import io


@login_required
@role_required(allowed_roles=["event_organizer", "owner"])
def export_attendees(request):
    # Fetch data similar to attendeesevent
    registrations = EventRegistration.objects.filter(event__organizer=request.user).select_related('event', 'user')

    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Attendees"

    # Headers
    headers = ['Name', 'Email', 'Event', 'Status', 'RSVP Date']
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num, value=header)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')

    # Data rows
    row_num = 2
    status_mapping = {
        'registered': 'Pending',
        'attended': 'Confirmed',
        'cancelled': 'Cancelled'
    }

    for reg in registrations:
        name = f"{reg.user.first_name} {reg.user.last_name}".strip() or reg.user.username
        email = reg.user.email
        event_title = reg.event.title
        status = status_mapping.get(reg.status, reg.status)
        rsvp_date = reg.registration_date.date().strftime('%Y-%m-%d')

        ws.cell(row=row_num, column=1, value=name)
        ws.cell(row=row_num, column=2, value=email)
        ws.cell(row=row_num, column=3, value=event_title)
        ws.cell(row=row_num, column=4, value=status)
        ws.cell(row=row_num, column=5, value=rsvp_date)

        row_num += 1

    # Auto-adjust column widths
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    # Create response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=attendees.xlsx'

    # Save to response
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    response.write(buffer.getvalue())

    return response


# ================= DASHBOARDS =================

@login_required
@role_required(allowed_roles=["owner"])
def business_owner_dashboard(request):
    return render(request, "localcommunity/businessowner/businessowner.html")


@login_required
@role_required(allowed_roles=["user"])
def user_dashboard(request):
    return render(request, "core/index.html")


# ================= BUSINESS OWNER PAGES =================

def businessownerdashboard(request):
    return render(request, "localcommunity/businessowner/businessowner.html")


def mybusinesses(request):
    return render(request, "localcommunity/businessowner/mybusinesses.html")


def addbusiness(request):
    return render(request, "localcommunity/businessowner/addbusiness.html")


def reviews(request):
    return render(request, "localcommunity/businessowner/reviews.html")


def analyticsbusiness(request):
    return render(request, "localcommunity/businessowner/analyticsbusiness.html")


# ================= SETTINGS (FIXED) =================

@login_required
@role_required(allowed_roles=["owner"])
def settingsbusiness(request):

    user = request.user

    if request.method == 'POST':
        form = OwnerProfileUpdateForm(request.POST, instance=user)

        if form.is_valid():

            # ✅ DON'T SAVE YET
            user_obj = form.save(commit=False)

            # password fields
            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')

            # 👉 if user trying to change password
            if current_password or new_password or confirm_password:

                if not user.check_password(current_password):
                    messages.error(request, "Current password is incorrect")
                    return render(request, 'localcommunity/businessowner/settingsbusiness.html', {"form": form})

                if new_password != confirm_password:
                    messages.error(request, "New passwords do not match")
                    return render(request, 'localcommunity/businessowner/settingsbusiness.html', {"form": form})

                # ✅ set new password
                user_obj.set_password(new_password)

                # save BEFORE updating session
                user_obj.save()

                # keep user logged in
                update_session_auth_hash(request, user_obj)

                messages.success(request, "Password updated successfully")

            else:
                # ✅ save normal profile updates
                user_obj.save() 
                messages.success(request, "Profile updated successfully")

            return redirect('localcommunity:businessownerdashboard')

        else:
            print(form.errors)

    else:
        form = OwnerProfileUpdateForm(instance=user)

    return render(request, 'localcommunity/businessowner/settingsbusiness.html', {"form": form})


# ================= LOGOUT =================

def logoutbusiness(request):
    logout(request)
    return redirect('login')  # change to your login URL name


# ================= EVENT STUDIO =================

from django.utils import timezone
from events.models import Event, EventRegistration

@login_required
@role_required(allowed_roles=["event_organizer"])
def eventstudio(request):
    if not request.user.is_authenticated:
        return redirect('login')

    today = timezone.localdate()
    user_events = Event.objects.filter(organizer=request.user)

    upcoming_events = user_events.filter(event_date__gte=today).order_by('event_date')

    total_events = user_events.count()
    total_rsvps = EventRegistration.objects.filter(event__organizer=request.user).count()
    attended = EventRegistration.objects.filter(event__organizer=request.user, status='attended').count()
    avg_attendance = round((attended / total_rsvps * 100), 2) if total_rsvps else 0

    event_cards = []
    for ev in upcoming_events:
        rsvp_count = EventRegistration.objects.filter(event=ev).count()
        max_participants = ev.max_participants or 1
        progress_percent = min(100, int((rsvp_count / max_participants) * 100)) if max_participants > 0 else 0
        event_cards.append({
            'title': ev.title,
            'approval_status': ev.approval_status,
            'event_date': ev.event_date,
            'start_time': ev.start_time,
            'rsvp_count': rsvp_count,
            'max_participants': max_participants,
            'progress_percent': progress_percent,
            'status_display': 'Published' if ev.approval_status == 'approved' else ('Pending' if ev.approval_status == 'pending' else 'Cancelled'),
        })

    return render(request, "localcommunity/eventstudio/eventstudio.html", {
        'total_events': total_events,
        'total_rsvps': total_rsvps,
        'avg_attendance': avg_attendance,
        'total_comments': 0,
        'upcoming_events': event_cards,
    })

@login_required
@role_required(allowed_roles=["event_organizer"])
def eventstudiodashboard(request):
    return render(request, "localcommunity/eventstudio/eventstudio.html")


def myevents(request):
    return render(request, "localcommunity/eventstudio/myevents.html")


def createevent(request):
    return render(request, "localcommunity/eventstudio/createevent.html")


@login_required
@role_required(allowed_roles=["event_organizer", "owner"])
def attendeesevent(request):
    # Fetch all registrations for events organized by the user
    registrations = EventRegistration.objects.filter(event__organizer=request.user).select_related('event', 'user')

    # Prepare attendee data
    attendees = []
    for reg in registrations:
        status_mapping = {
            'registered': 'Pending',
            'attended': 'Confirmed',
            'cancelled': 'Cancelled'
        }
        attendees.append({
            'name': f"{reg.user.first_name} {reg.user.last_name}".strip() or reg.user.username,
            'email': reg.user.email,
            'event_title': reg.event.title,
            'status': status_mapping.get(reg.status, reg.status),
            'rsvp_date': reg.registration_date.date(),
            'registration': reg  # for actions if needed
        })

    # Calculate stats
    confirmed_count = sum(1 for a in attendees if a['status'] == 'Confirmed')
    pending_count = sum(1 for a in attendees if a['status'] == 'Pending')
    cancelled_count = sum(1 for a in attendees if a['status'] == 'Cancelled')

    # Get all emails for mailto
    all_emails = ','.join([a['email'] for a in attendees])

    context = {
        'attendees': attendees,
        'confirmed_count': confirmed_count,
        'pending_count': pending_count,
        'cancelled_count': cancelled_count,
        'all_emails': all_emails,
    }

    return render(request, "localcommunity/eventstudio/attendeesevent.html", context)


# def analyticsevent(request):

#     # ---------------- DASHBOARD COUNTS ----------------
#     total_rsvps = EventRegistration.objects.filter(status='registered').count()

#     total_events = EventRegistration.objects.values('event').distinct().count()

#     attended = EventRegistration.objects.filter(status='attended').count()

#     avg_attendance = (attended / total_rsvps * 100) if total_rsvps > 0 else 0


#     # ---------------- MONTHLY CHART ----------------
#     data = EventRegistration.objects.annotate(
#         month=TruncMonth('registration_date')
#     ).values('month').annotate(
#         total=Count('id')
#     ).order_by('month')

#     months = []
#     counts = []

#     for d in data:
#         months.append(d['month'].strftime('%b'))  # Jan, Feb
#         counts.append(d['total'])


#     # ---------------- EVENT PERFORMANCE ----------------
#     from events.models import Event

#     events = Event.objects.annotate(
#         rsvp_count=Count('eventregistration')
#     )


#     return render(request, 'localcommunity/eventstudio/analyticsbusiness.html', {
#         'total_rsvps': total_rsvps,
#         'total_events': total_events,
#         'avg_attendance': round(avg_attendance, 2),

#         'months': months,
#         'counts': counts,
#         'events': events
#     })


@login_required
@role_required(allowed_roles=["event_organizer"])
def settingsevent(request):
    
    user = request.user

    if request.method == 'POST':
        form = EventProfileUpdateForm(request.POST, instance=user)

        if form.is_valid():

            user_obj = form.save(commit=False)

            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')

            if current_password or new_password or confirm_password:

                if not user.check_password(current_password):
                    messages.error(request, "Current password is incorrect")
                    return render(request, 'localcommunity/eventstudio/settingsevent.html', {"form": form})

                if new_password != confirm_password:
                    messages.error(request, "New passwords do not match")
                    return render(request, 'localcommunity/eventstudio/settingsevent.html', {"form": form})

                user_obj.set_password(new_password)
                user_obj.save()
                update_session_auth_hash(request, user_obj)

                messages.success(request, "Password updated successfully")

            else:
                user_obj.save()
                messages.success(request, "Profile updated successfully")

            return redirect('localcommunity:eventstudiodashboard')

        else:       
            print(form.errors)

    else:
        form = EventProfileUpdateForm(instance=user)
    
    # ✅ FIX IS HERE
    return render(request, "localcommunity/eventstudio/settingsevent.html", {"form": form})


def logoutevent(request):
    logout(request)
    return redirect('login')  # change if needed