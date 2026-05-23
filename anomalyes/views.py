from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
# FILE UPLOAD AND VIEW
from  django.core.files.storage import FileSystemStorage
# SESSION
from django.conf import settings
from .models import *
from django.db.models import F, Count
import os
import json
from tensorflow.keras import backend as k
from ML import test1

def home(request):
    return render(request,'index.html')

def index(request):
    return render(request,'index.html')

def register(request):
    return render(request,'register.html')

def addregister(request):
    if request.method=="POST":
        name=request.POST.get('name') 
        email=request.POST.get('email')
        password=request.POST.get('password')
        phone=request.POST.get('phone')
        
        # Server-side validation
        if not name or not email or not password or not phone:
            return render(request, 'register.html', {'message': 'All fields are required'})
        
        import re
        if not re.match(r"^[A-Za-z\s]{3,50}$", name):
            return render(request, 'register.html', {'message': 'Invalid Name format'})
            
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render(request, 'register.html', {'message': 'Invalid Email format'})
            
        if not re.match(r"^[0-9]{10}$", phone):
            return render(request, 'register.html', {'message': 'Phone must be exactly 10 digits'})
            
        if len(password) < 6:
            return render(request, 'register.html', {'message': 'Password must be at least 6 characters'})

        if regtable.objects.filter(email=email).exists():
            return render(request, 'register.html', {'message': 'Email already registered'})
            
        ins=regtable(name=name,email=email,password=password,phone=phone)
        ins.save()
    return render(request,"index.html", {'message':'Succesfully Registered'})
def login(request):
    return render(request,'login.html')

def addlogin(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    if email=='admin@gmail.com'and password=='admin':
        request.session['admin@gmail.com']='admin@gmail.com'
        request.session['admin']='admin'
       
        return render(request,'index.html')

    elif regtable.objects.filter(email=email,password=password).exists():
        userdetails=regtable.objects.get(email=email,password=password)
        if userdetails.email==request.POST['email']:
            request.session['userid']=userdetails.id
            request.session['username']=userdetails.name 
            return render(request,'index.html')  
    else:
        return render(request, 'login.html', {'message':'Invalid Email or Password'})

def logout(request):
    session_keys=list(request.session.keys())   
    for key in session_keys:
            del request.session[key] 
    return redirect(index)

def viewuser(request):
    user=regtable.objects.all()
    return render(request,'viewuser.html',{'result':user})  

def upload(request):
    return render(request,'upload.html')
    
def addupload(request):
    if request.method == "POST":
        myfile=request.FILES['file'] 
        fs=FileSystemStorage()
        filename=fs.save(myfile.name,myfile)
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT,'input/test/test.csv'))
        except:
            pass
        fs=FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'input/test/'))  
        fs.save("test.csv", myfile) 
        fs=FileSystemStorage()
        fs.save(myfile.name,myfile) 
        k.clear_session()

        result=test1.predict()
        ins=uploadtable(images=filename,user_id=request.session['userid'],result=result)
        ins.save()
    return render(request,'upload.html',{'result':result})

def viewupload(request):
    user=uploadtable.objects.all()
    ww=regtable.objects.all()
    for i in user:
        for j in ww:
            if str(i.user_id) == str(j.id):
                i.user_id = j.name

    return render(request,'viewupload.html',{'result':user})    

def attack_analysis(request):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
    import io, base64

    def fig_to_b64(fig):
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight',
                    facecolor=fig.get_facecolor(), edgecolor='none', dpi=130)
        buf.seek(0)
        encoded = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close(fig)
        return encoded

    uploads = uploadtable.objects.all()
    attack_counts = {}
    for row in uploads:
        label = row.result.strip() if row.result else 'Unknown'
        attack_counts[label] = attack_counts.get(label, 0) + 1

    labels = list(attack_counts.keys())
    counts = list(attack_counts.values())
    total  = sum(counts)

    BAR_IMG = PIE_IMG = HORIZ_IMG = None

    if total > 0:
        PALETTE = [
            '#a78bfa','#f87171','#60a5fa','#34d399',
            '#fbbf24','#f472b6','#818cf8','#67e8f9',
            '#fde68a','#6ee7b7',
        ]
        colors  = [PALETTE[i % len(PALETTE)] for i in range(len(labels))]
        BG      = '#0d0d24'
        CLR_DIM = '#aaaaaa'
        CLR_WH  = '#ffffff'
        CLR_CC  = '#cccccc'
        GRID_C  = (1.0, 1.0, 1.0, 0.08)

        # ── BAR CHART ──
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_facecolor(BG)
        ax.set_facecolor(BG)
        bars = ax.bar(labels, counts, color=colors, edgecolor='none', width=0.55, zorder=3)
        ax.set_xlabel('Attack Type', color=CLR_DIM, fontsize=10)
        ax.set_ylabel('Count',       color=CLR_DIM, fontsize=10)
        ax.set_title('Attack Frequency', color=CLR_WH, fontsize=13, fontweight='bold', pad=14)
        ax.tick_params(colors=CLR_DIM, labelsize=9)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.yaxis.grid(True, color=GRID_C, linewidth=0.7, zorder=0)
        ax.set_axisbelow(True)
        for bar, val in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                    str(val), ha='center', va='bottom', color=CLR_WH, fontsize=9, fontweight='bold')
        plt.xticks(rotation=30, ha='right')
        BAR_IMG = fig_to_b64(fig)

        # ── PIE CHART ──
        fig2, ax2 = plt.subplots(figsize=(7, 4))
        fig2.patch.set_facecolor(BG)
        ax2.set_facecolor(BG)
        wedges, texts, autotexts = ax2.pie(
            counts, labels=None, colors=colors,
            autopct='%1.1f%%', startangle=140,
            wedgeprops=dict(edgecolor=BG, linewidth=2),
            pctdistance=0.78,
        )
        for at in autotexts:
            at.set_color(CLR_WH); at.set_fontsize(9)
        legend_patches = [mpatches.Patch(color=colors[i], label=labels[i]) for i in range(len(labels))]
        ax2.legend(handles=legend_patches, loc='center left', bbox_to_anchor=(1.01, 0.5),
                   frameon=False, fontsize=9)
        for text in ax2.get_legend().get_texts():
            text.set_color(CLR_CC)
        ax2.set_title('Attack Distribution', color=CLR_WH, fontsize=13, fontweight='bold', pad=14)
        PIE_IMG = fig_to_b64(fig2)

        # ── HORIZONTAL BAR (ranked) ──
        sorted_pairs = sorted(zip(counts, labels), reverse=True)
        s_counts = [p[0] for p in sorted_pairs]
        s_labels = [p[1] for p in sorted_pairs]
        s_colors = [colors[labels.index(l)] for l in s_labels]

        fig3, ax3 = plt.subplots(figsize=(7, max(3, len(labels)*0.55 + 1)))
        fig3.patch.set_facecolor(BG)
        ax3.set_facecolor(BG)
        hbars = ax3.barh(s_labels, s_counts, color=s_colors, edgecolor='none', height=0.55, zorder=3)
        ax3.invert_yaxis()
        ax3.set_xlabel('Count', color=CLR_DIM, fontsize=10)
        ax3.set_title('Ranked Threat Overview', color=CLR_WH, fontsize=13, fontweight='bold', pad=14)
        ax3.tick_params(colors=CLR_DIM, labelsize=9)
        for spine in ax3.spines.values():
            spine.set_visible(False)
        ax3.xaxis.grid(True, color=GRID_C, linewidth=0.7, zorder=0)
        ax3.set_axisbelow(True)
        for bar, val in zip(hbars, s_counts):
            ax3.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                     str(val), va='center', color=CLR_WH, fontsize=9, fontweight='bold')
        HORIZ_IMG = fig_to_b64(fig3)

    # sort for table
    sorted_attacks = sorted(attack_counts.items(), key=lambda x: x[1], reverse=True)
    top_attack = sorted_attacks[0][0] if sorted_attacks else '—'

    context = {
        'attack_counts' : sorted_attacks,
        'total'         : total,
        'top_attack'    : top_attack,
        'unique_types'  : len(labels),
        'bar_img'       : BAR_IMG,
        'pie_img'       : PIE_IMG,
        'horiz_img'     : HORIZ_IMG,
    }
    return render(request, 'attack_analysis.html', context)

# ── USER: Submit Complaint ──
def complaint(request):
    return render(request, 'complaint.html', {'message': None})

def addcomplaint(request):
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        user_id = request.session.get('userid')
        if subject and message and user_id:
            ins = complainttable(user_id=user_id, subject=subject, message=message)
            ins.save()
            return render(request, 'complaint.html', {'message': 'Your complaint has been submitted successfully!'})
        else:
            return render(request, 'complaint.html', {'message': 'Please fill in all fields.'})
    return redirect('/')

# ── USER: View Own Complaints ──
def mycomplaints(request):
    user_id = request.session.get('userid')
    data = complainttable.objects.filter(user_id=str(user_id)).order_by('-date')
    return render(request, 'mycomplaints.html', {'complaints': data})

# ── ADMIN: View All Complaints ──
def viewcomplaints(request):
    all_complaints = complainttable.objects.all().order_by('-date')
    users = regtable.objects.all()
    user_map = {str(u.id): u.name for u in users}
    for c in all_complaints:
        c.user_name = user_map.get(str(c.user_id), 'Unknown')
    return render(request, 'viewcomplaints.html', {'complaints': all_complaints})

def accept_complaint(request, id):
    complaint = complainttable.objects.get(id=id)
    complaint.status = 'Accepted'
    complaint.save()
    return redirect('/viewcomplaints/')
