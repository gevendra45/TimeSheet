from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from .utils import render_to_pdf
from django.shortcuts import render, redirect
from .models import Logintime
from .forms import InputId, AddDetail
import datetime

def get_report_details(a):
	nwtime = 0
	wtime = 0

	for i in range(len(a)):
		nwtime+=a[i].nwtime
		wtime+=a[i].wtime
	
	template = get_template('report.html')
	context = {
		"empid" : a[0].empid,
		"intime" : a[0].intime,
		"outtime" : a[len(a)-1].outtime,
		"whours" : wtime,
		"nwhours" : nwtime
	}
	return context

# Create your views here.
def register_home(request): 
	form = AddDetail(request.POST or None)
	if form.is_valid():
		empid = request.POST.get("empid")
		today = datetime.date.today()
		today_str = today.strftime("%d%m%Y")
		a = today_str+request.POST.get("intime")
		time1 = datetime.datetime.strptime(a,"%d%m%Y%H%M")
		a = today_str+request.POST.get("outtime")
		outtime=time2 = datetime.datetime.strptime(a,"%d%m%Y%H%M")
		dateTimeDifference = time2-time1
		dateTimeDifferenceInHours = dateTimeDifference.total_seconds()
		nwtime=0
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
				nwtime = round(dateTimeDifferenceInHours/3600, 2)
				if int(dateTimeDifferenceInHours) <= 0:
					context = { 
						"message" : "Either the same entry is present or either time slots are mentioned for Employee ID previously."
					}
					return render(request, "message.html", context)
		wtime = round(dateTimeDifferenceInHours/3600, 2)
		obj = Logintime.objects.create(empid=empid, intime=time1, outtime = outtime, wtime = wtime, nwtime = nwtime)
		obj.save()
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
			context = get_report_details(a)
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
		context = get_report_details(a)
		template = get_template('timesheet.html')
		html = template.render(context)
		pdf = render_to_pdf('timesheet.html', context)
		if pdf:
			return HttpResponse(pdf, content_type='application/pdf')
	return redirect(nodata_found) 