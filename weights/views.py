# Create your views here.

from django.shortcuts import render
from .forms import WeightForm
from .models import WeightEntry
from datetime import datetime
from django.http import HttpResponse
from fpdf import FPDF
from zoneinfo import ZoneInfo



now = datetime.now(ZoneInfo("Asia/Dhaka"))
timeNow = now.strftime("%d-%B-%y %I:%M:%S %p")
today = now.strftime("%d-%B-%y")
timeStamp = now.strftime("%I_%M_%S_%p_%d_%B_%y")


class WeightReportPDF(FPDF):
	def header(self):
		self.set_font("Helvetica", style="B", size=14)
		self.cell(0, 8, "SR BRIDGE SCALE", ln=True, align="C")
		self.set_font("Helvetica", size=10)
		self.cell(0, 6, "RAIPUR ROAD TULATOLI LAKSHMIPUR Mob. 01731273113, 01722200634", ln=True, align="C")
		self.ln(5)
		self.set_font("Helvetica", style="B", size=12)
		self.set_x(80)
		self.cell(50, 8, "Weight Report", border=1, ln=True, align="C")
		self.ln(5)

	def footer(self):
		self.set_y(-40)
		self.set_font("Helvetica", size=10)
		self.cell(40, 10, "Received by", border="T", align="C")
		self.cell(10, 0, "", border="1", align="C")
		self.cell(40, 10, "Supervised by", border="T", align="C")
		self.cell(10, 0, "", border="1", align="C")
		self.cell(40, 10, "Operated by", border="T", align="C")
		self.cell(10, 0, "", border="1", align="C")
		self.cell(40, 10, "Authorized by", border="T", align="C")
		self.ln(10)

	def report_body(self, data):
		self.set_font("Helvetica", size=10)
		net_weight = int(data["load_weight"]) - int(data["unload_weight"])
		rows = [
			["Weight ID: " + data["weight_id"], "Scale ID: " + data["scale_id"]],
			["Vehicle No: " + data["vehicle_no"], "Party Type: " + data["party_type"]],
			["Client Name: " + data["client_name"], "Print Date: " + data["print_date"]],
			["Challan/LC No: " + data["challan_no"], "Driver Contact: " + data["driver_contact"]],
			["Item Name: " + data["item_name"], "QTY: " + data["qty"]],
			["Load Weight: " + data['load_weight'] + " Kg", "Load Weight Date: " + data["load_weight_date"]],
			["Unload Weight: " + data['unload_weight'] + " Kg Deduct: " + data['deduct'] + " Kg", "Unload Weight Date: " + data["unload_weight_date"]],
			["Net Weight: " + str(net_weight) + " Kg"]
		]
		col_widths = [100, 90]
		for row in rows:
			for index, cell in enumerate(row):
				if "Net Weight" in cell:
					self.cell(190, 7, cell, border=1)
				else:
					self.cell(col_widths[index], 7, cell, border=1)
			self.ln()


def weight_entry_view(request):
	if request.method == 'POST':
		form = WeightEntryForm(request.POST)
		if form.is_valid():
			entry = form.save()

			data = {
				"weight_id": entry.weight_id,
				"scale_id": entry.scale_id,
				"vehicle_no": entry.vehicle_no,
				"party_type": entry.party_type,
				"client_name": entry.client_name,
				"print_date": today,
				"challan_no": entry.challan_no,
				"item_name": entry.item_name,
				"qty": entry.qty,
				"load_weight": str(entry.load_weight),
				"load_weight_date": timeNow,
				"unload_weight": str(entry.unload_weight),
				"unload_weight_date": timeNow,
				"deduct": entry.deduct,
				"net_weight": "",
				"driver_contact": entry.driver_contact
			}

			pdf = WeightReportPDF()
			pdf.add_page()
			pdf.report_body(data)

			response = HttpResponse(content_type='application/pdf')
			response['Content-Disposition'] = f'attachment; filename="{entry.client_name}_{timeStamp}.pdf"'
			pdf_output = pdf.output(dest='S').encode('latin1')
			response.write(pdf_output)
		return response
	else:
		form = WeightEntryForm()

	return render(request, 'weights/weight_entry.html', {'form': form})



def weight_list(request):
	entries = WeightEntry.objects.all().order_by('-id')
	return render(request, 'weights/list.html', {'entries': entries})