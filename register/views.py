from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from .utils import render_to_pdf
from django.shortcuts import render, redirect
from .models import Logintime
from .forms import InputId, AddDetail
import datetime

def register_counter(request): 
	form = InputId(request.POST or None)
	if form.is_valid():
		empid=request.POST.get("empid")
		rdate = datetime.date.today()
		x=Logintime.objects.filter(empid=request.POST.get("empid"), rdate = datetime.date.today())
		if len(x)==0:
			print("Arrived office")
			obj = Logintime.objects.create(
				empid=empid, 
				intime=datetime.datetime.now(), 
				outtime = datetime.datetime.now(), 
				wtime = 0, 
				nwtime = 0,
				io='I'
			)
			obj.save()
			context = { 
				"message" : "Submitted Successfully Your Timesheet Couter Started."
			}
			return render(request, "message.html", context)
		else:
			if x[len(x)-1].io=='I':
				print("i am going out")
				intime = (x[len(x)-1].intime).replace(tzinfo=None)
				wtime=round((datetime.datetime.now()-intime).total_seconds()/3600, 2)
				if len(x)>1:
					wtime+=x[len(x)-1].wtime
				updt=Logintime.objects.get(
					empid = empid, 
					rdate = rdate, 
					intime = x[len(x)-1].intime
				)
				updt.outtime = datetime.datetime.now()
				updt.wtime = wtime 
				updt.io='O'
				updt.save()
				context = { 
					"message" : "Submitted Successfully Your Timesheet Couter Stopped."
				}
				return render(request, "message.html", context)

			if x[len(x)-1].io=='O':
				print("i am returning office")
				outtime = (x[len(x)-1].outtime).replace(tzinfo=None)
				nwtime=round((datetime.datetime.now()-outtime).total_seconds()/3600, 2)
				obj = Logintime.objects.create(
					empid=empid,
					intime=datetime.datetime.now(),
					outtime = datetime.datetime.now(),
					wtime = x[len(x)-1].wtime, 
					nwtime = x[len(x)-1].nwtime+nwtime,
					io='I'
				)
				obj.save()
				context = { 
					"message" : "Submitted Successfully Your Timesheet Couter Started."
				}
				return render(request, "message.html", context)
	context = { 
		"form" : form,
		"message" : "Start Counter by input your Employee ID",
		"link" : "http://localhost:8000/getid/",
		"button"  : "Fetch Report"
	}
	return render(request, "getid.html", context)

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

def approval(request):
	context = { 
		"message" : "Your Request has been Submitted for approval !!!."
	}
	return render(request, "message.html", context)

def get_id(request):
	if request.method == 'POST':
		a=Logintime.objects.filter(empid=request.POST.get("empid"), rdate = datetime.date.today())
		if len(a)>0:
			if a[len(a)-1].io=='I':
				outtime = datetime.datetime.now()
				intime = (a[len(a)-1].intime).replace(tzinfo=None)
				wtime=round((outtime-intime).total_seconds()/3600, 2)+round(a[len(a)-1].wtime,2)
			if a[len(a)-1].io=='O':
				outtime = a[len(a)-1].outtime
				wtime = a[len(a)-1].wtime
			if len(a)>0:
				context = {
					"empid"   : a[0].empid,
					"intime"  : a[0].intime,
					"outtime" : outtime,
					"whours"  : wtime,
					"nwhours" : a[len(a)-1].nwtime
				}
				return render(request, "report.html", context)
		else:
			return redirect(nodata_found)
	else:
		form = InputId()
		context = { 
			"form" : form,
			"message" : "Input EmpID to fetch your Time Sheet report",
			"link" : "http://localhost:8000/",
			"button"  : "Fill Timesheet"
		}
	return render(request, "getid.html", context)

def generate_report(request, id=None):
	a=Logintime.objects.filter(empid=id, rdate = datetime.date.today())
	if len(a)>0:
		print("calculating")
		if a[len(a)-1].io=='I':
			outtime = datetime.datetime.now()
			intime = (a[len(a)-1].intime).replace(tzinfo=None)
			wtime=round((outtime-intime).total_seconds()/3600, 2)+round(a[len(a)-1].wtime,2)
		if a[len(a)-1].io=='O':
			outtime = a[len(a)-1].outtime
			wtime = a[len(a)-1].wtime
		if len(a)>0:
			context = {
				"empid"   : a[0].empid,
				"intime"  : a[0].intime,
				"outtime" : outtime,
				"whours"  : wtime,
				"nwhours" : a[len(a)-1].nwtime
			}
		template = get_template('timesheet.html')
		html = template.render(context)
		pdf = render_to_pdf('timesheet.html', context)
		if pdf:
			print("sendind pdf")
			return HttpResponse(pdf, content_type='application/pdf')
	print("hi i am here")
	return redirect(nodata_found) 