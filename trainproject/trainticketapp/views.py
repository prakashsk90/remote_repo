from django.shortcuts import render,redirect
from trainticketapp.models import TicketPreference
from trainticketapp import forms
from django.db.models import Q


# Create your views here.

def home_view(request):
    return render(request,'trainticketapp/home.html')


def book_view(request):
    form=forms.TicketPreferenceForm()
    if request.method=='POST':
        form=forms.TicketPreferenceForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/home')

    return render(request,"trainticketapp/book.html",{"form":form})

def rac_seats(request):
    form=forms.RACForm()
    if request.method=='POST':
        form=forms.RACForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/home')

    return render(request,"trainticketapp/rac_seats.html",{"form":form})

def waiting_list(request):
    form=forms.WaitingListForm()
    if request.method=='POST':
        form=forms.WaitingListForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/home')

    return render(request,"trainticketapp/waiting_list.html",{"form":form})

def print_booked_tickets(request):
    ticket=TicketPreference.objects.filter(~Q(berth_preference = '') & ~Q(berth_preference = 'free'))
    count=ticket.count()
    return render(request,'trainticketapp/booked_tickets.html',{'ticket':ticket,'count':count})

def print_booked_RAC_tickets(request):
    ticket=TicketPreference.objects.exclude(rac_seats__exact='')
    count=ticket.count()
    return render(request,'trainticketapp/booked_RAC_tickets.html',{'ticket':ticket,'count':count})

def alloted_waiting_list(request):
    ticket=TicketPreference.objects.exclude(waiting_list__exact='')
    count=ticket.count()
    return render(request,'trainticketapp/alloted_waiting_list.html',{'ticket':ticket,'count':count})

def delete_view(request,id):
    tickt=TicketPreference.objects.get(id=id)
    print(tickt)
    tk=tickt.berth_preference
    tickt.delete()
    rc=TicketPreference.objects.filter(~Q(rac_seats = ''))
    num=0
    for r in rc:
        if num==0:
            temp=r.rac_seats
            r.berth_preference=tk
            r.rac_seats=''
            num+=1
            r.save()
        else:
            temp1=r.rac_seats
            r.rac_seats=temp
            temp=temp1
            r.save()
    wl=TicketPreference.objects.filter(~Q(waiting_list = ''))
    num=0
    for w in wl:
        if num==0:
            temp_wl=w.waiting_list
            w.rac_seats=temp
            w.waiting_list=''
            num+=1
            w.save()
        else:
            temp1_wl=w.waiting_list
            w.waiting_list=temp_wl
            temp_wl=temp1_wl
            w.save()

    return redirect('/home')

def print_available_tickets(request):
    n=[]
    x=TicketPreference.objects.count()
    print(x)

    bert=[]
    Berth = ['U11','U12','L11','L12','M11','M12','U21','U22','L21','L22','M21','M22','U31','U32','L31','L32','M31','M32','U41','U42','L41','L42','M41','M42']
    for o in Berth:
        d=TicketPreference.objects.filter(berth_preference__icontains=o)
        if not d:
            bert.append(o)

    count=len(bert)
    return render(request,'trainticketapp/available_tickets.html',{'bert':bert,'count':count})
