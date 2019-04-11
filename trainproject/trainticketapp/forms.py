from django import forms
from trainticketapp.models import TicketPreference
from django.core import validators
from django.db.models import Q

class TicketPreferenceForm(forms.ModelForm):
    CHOICES = (('Male', 'Male',), ('Female', 'Female',))
    Berth = (('Upper', 'Upper',), ('Lower', 'Lower',), ('Middle', 'Middle',), ('free', 'free',))
    gender = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
    berth_preference = forms.ChoiceField(widget=forms.Select, choices=Berth)

    class Meta:
        model=TicketPreference
        fields=('name','age','gender','berth_preference')

    def clean(self):
        print('total form validation')
        cleaned_data=super().clean()
        cnt=0
        bp=TicketPreference.objects.filter(~Q(berth_preference = '') & ~Q(berth_preference = 'free'))
        bp_lower=TicketPreference.objects.filter(~Q(berth_preference = '') & ~Q(berth_preference__startswith = 'L') & ~Q(berth_preference = 'free'))
        l=['U11','U12','L11','L12','M11','M12','U21','U22','L21','L22','M21','M22','U31','U32','L31','L32','M31','M32','U41','U42','L41','L42','M41','M42','free']
        if bp.count()==24:
            raise forms.ValidationError('No more berths left select Reserved seat button')
        if cleaned_data['age']<5 and cleaned_data['berth_preference'][0:5]!='free':
            raise forms.ValidationError('no ticket required for child select free')
        else:
            for j in l:
                cnt+=1
                if cleaned_data['berth_preference'][0]==j[0]:
                    e=TicketPreference.objects.filter(berth_preference__icontains=j)
                    if e:
                        continue
                    else:
                        cleaned_data['berth_preference']=j
                        break
                else:
                    if cnt==len(l):
                        raise forms.ValidationError('berth taken choose some other berth')

        if cleaned_data['age']<60 and cleaned_data['berth_preference'][0]=='L' and bp_lower.count()<16:
            raise forms.ValidationError('berth reserved for old persons')
        if cleaned_data['age']>5 and cleaned_data['berth_preference'][0]=='free':
            raise forms.ValidationError('free is allowed only for children below 5')
        if cleaned_data['name'].isalpha()!=True:
            raise forms.ValidationError('name should contain only alphabets')
        if cleaned_data['age']>60 and cleaned_data['berth_preference'][0]!='L':
            raise forms.ValidationError('please selct any lower berth')

        if cleaned_data['gender']=='Female':
            m=[]
            k=[]
            v=[]
            ticket1=TicketPreference.objects.exclude(berth_preference__exact='')
            tc=list(ticket1.values('berth_preference'))
            tc2=list(ticket1.values('gender'))
            i=0
            y=0
            while i<len(tc):
                k.append(tc[i]['berth_preference'])
                i+=1
            print('key')
            print(k)
            while y<len(tc2):
                m.append(tc2[y]['gender'])
                y+=1
            print('value')
            print(m)
            res = {}
            res = {k[i]: m[i] for i in range(len(k))}
            print(res)
            for x, y in res.items():
                if y=='Male':
                    v.append(x)
            count=0
            print('v')
            print(v)
            for s in v:
                if cleaned_data['berth_preference'][-2]==s[-2]:
                    print(cleaned_data['berth_preference'][-2])
                    count+=1
            print('count')
            print(count)
            if count>=4 and cleaned_data['age']<60:
                raise forms.ValidationError('Choose another berth since men are occupied in all berths in this coach')




class RACForm(forms.ModelForm):
    CHOICES = (('Male', 'Male',), ('Female', 'Female',))
    seats = (('RAC','RAC'),)
    gender = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
    rac_seats = forms.ChoiceField(widget = forms.Select, choices=seats)

    class Meta:
        model=TicketPreference
        fields=('name','age','gender','rac_seats')

    def clean(self):
        print('total form validation')
        cleaned_data=super().clean()
        bp=TicketPreference.objects.filter(~Q(berth_preference = '') & ~Q(berth_preference = 'free'))
        rc=TicketPreference.objects.filter(~Q(rac_seats = ''))
        if bp.count()<24:
            raise forms.ValidationError('do not select RAC seats,berths are available')
        if rc.count()==8:
            raise forms.ValidationError('select waiting list')
        if cleaned_data['name'].isalpha()!=True:
            raise forms.ValidationError('name should contain only alphabets')
        if cleaned_data['rac_seats']=='RAC':
            print('YES')
            RAC_Seat=['ra1','ra2','ra3','ra4','ra5','ra6','ra7','ra8']
            rac_seat_count=0
            for m in RAC_Seat:
                rac_seat_count+=1
                e=TicketPreference.objects.filter(rac_seats__icontains=m)
                print(e)
                if e:
                    continue
                else:
                    print('else')
                    cleaned_data['rac_seats']=m
                    break


class WaitingListForm(forms.ModelForm):
    CHOICES = (('Male', 'Male',), ('Female', 'Female',))
    seats = (('WList','WList'),)
    gender = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
    waiting_list = forms.ChoiceField(widget = forms.Select, choices=seats)

    class Meta:
        model=TicketPreference
        fields=('name','age','gender','waiting_list')

    def clean(self):
        print('total form validation')
        cleaned_data=super().clean()
        bp=TicketPreference.objects.filter(~Q(berth_preference = '') & ~Q(berth_preference = 'free'))
        rc=TicketPreference.objects.filter(~Q(rac_seats = ''))
        wl=TicketPreference.objects.filter(~Q(waiting_list = ''))
        if bp.count()<24:
            raise forms.ValidationError('do not select waiting list, berths are available')
        if rc.count()<8:
            raise forms.ValidationError('do not select waiting list, select RAC Seats')
        if wl.count()==5:
            raise forms.ValidationError('No more Ticket Available')
        if cleaned_data['name'].isalpha()!=True:
            raise forms.ValidationError('name should contain only alphabets')
        if TicketPreference.objects.count()<32:
            raise forms.ValidationError('select RAC')
        if cleaned_data['waiting_list']=='WList':
            print('YES')
            waiting_list=['wl1','wl2','wl3','wl4','wl5']
            wl_count=0
            for m in waiting_list:
                wl_count+=1
                e=TicketPreference.objects.filter(waiting_list__icontains=m)
                print(e)
                if e:
                    continue
                else:
                    print('else')
                    cleaned_data['waiting_list']=m
                    break
