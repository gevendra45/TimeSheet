from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from .utils import render_to_pdf
from django.shortcuts import render, redirect
from .models import Logintime
from .forms import InputId, AddDetail
import datetime

# Create your views here.
def register_home(request):
	form = AddDetail(request.POST or None)
	if form.is_valid():
		today = datetime.date.today()
		today_str = today.strftime("%d%m%Y")
		a = today_str+request.POST.get("intime")
		time1 = datetime.datetime.strptime(a,"%d%m%Y%H%M")
		a = today_str+request.POST.get("outtime")
		time2 = datetime.datetime.strptime(a,"%d%m%Y%H%M")
		dateTimeDifference = time2-time1
		dateTimeDifferenceInHours = dateTimeDifference.total_seconds()
		if int(dateTimeDifferenceInHours) <= 0:
			context = { 
				"message" : "Out Time mentioned is smaller than In Time."
			}
			return render(request, "message.html", context)
		else:
			x=Logintime.objects.filter(empid=request.POST.get("empid"), rdate = datetime.date.today())
			r=[]
			if len(x)>0:
				for i in x:
					pass
				time2 = datetime.datetime.combine(datetime.date.today(), i.outtime)
				dateTimeDifference = time1-time2
				dateTimeDifferenceInHours = dateTimeDifference.total_seconds()
				if int(dateTimeDifferenceInHours) <= 0:
					context = { 
						"message" : "Either the same entry is present or either time slots are mentioned for Employee ID previously."
					}
					return render(request, "message.html", context)
		instance = form.save(commit=False)
		instance.save()
		return redirect(register_succ)
	context = { 
		"form" : form
	}
	return render(request, "putid.html", context)

def register_succ(request):
	context = { 
		"message" : "Submitted Successfully !!!."
	}
	return render(request, "message.html", context)

def nodata_found(request):
	context = { 
		"message" : "No data found !!!."
	}
	return render(request, "message.html", context)

def get_id(request):
	if request.method == 'POST':
		a=Logintime.objects.filter(empid=request.POST.get("empid"), rdate = datetime.date.today())
		if len(a)>0:
			outtime = a[len(a)-1].outtime
			intime = a[0].intime
			nwtime = 0
			wtime = 0

			for i in range(len(a)):
				if i>0:
					nwtime+=(datetime.datetime.strptime(str(a[i].intime),"%H:%M:%S")-datetime.datetime.strptime(str(a[i-1].outtime),"%H:%M:%S")).total_seconds()
				wtime+=(datetime.datetime.strptime(str(a[i].outtime),"%H:%M:%S")-datetime.datetime.strptime(str(a[i].intime),"%H:%M:%S")).total_seconds()

			nwtime = round(nwtime/3600, 2)
			wtime = round(wtime/3600, 2)
	
			template = get_template('timesheet.html')
			context = {
				"empid" : a[0].empid,
				"intime" : intime,
				"outtime" : outtime,
				"whours" : wtime,
				"nwhours" : nwtime
			}

			return render(request, "report.html", context)
		else:
			return redirect(nodata_found)
	else:
		form = InputId()
		context = { 
			"form" : form
		}
	return render(request, "getid.html", context)

def generate_report(request, id=None):
	a=Logintime.objects.filter(empid=id, rdate = datetime.date.today())
	if len(a)>0:
		outtime = a[len(a)-1].outtime
		intime = a[0].intime
		nwtime = 0
		wtime = 0

		for i in range(len(a)):
			if i>0:
				nwtime+=(datetime.datetime.strptime(str(a[i].intime),"%H:%M:%S")-datetime.datetime.strptime(str(a[i-1].outtime),"%H:%M:%S")).total_seconds()
			wtime+=(datetime.datetime.strptime(str(a[i].outtime),"%H:%M:%S")-datetime.datetime.strptime(str(a[i].intime),"%H:%M:%S")).total_seconds()

		nwtime = round(nwtime/3600, 2)
		wtime = round(wtime/3600, 2)
	
		template = get_template('timesheet.html')
		context = {
			"empid" : a[0].empid,
			"intime" : intime,
			"outtime" : outtime,
			"whours" : wtime,
			"nwhours" : nwtime
		}
		
		html = template.render(context)
		pdf = render_to_pdf('timesheet.html', context)
		if pdf:
			return HttpResponse(pdf, content_type='application/pdf')
	return redirect(nodata_found)