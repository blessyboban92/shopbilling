from datetime import date

from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.forms import modelformset_factory
import json
from datetime import datetime
from django.http import JsonResponse, HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import *

app_name = 'partyapp'
from hiapp.models import ItemMaster
page_load_counter = 1

def addparty(request):
    return render(request, 'party.html')


def add_party(request):
    party_list = list(PartyMaster.objects.all())
    party_list.reverse()
    if request.method == "POST":
        partyname = request.POST['partyname']
        partycode = request.POST['partycode']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        city = request.POST['city']
        state = request.POST['state']
        pin = request.POST['pin']
        mobile1 = request.POST['mobile1']
        mobile2 = request.POST['mobile2']
        email = request.POST['email']
        gst = request.POST['gst']
        pricelist = request.POST['pricelist']
        party = PartyMaster(partyname=partyname, partycode=partycode, address1=address1, address2=address2, city=city,
                            state=state,
                            pin=pin, mobile1=mobile1, mobile2=mobile2, email=email, gst=gst, pricelist=pricelist)
        party.save()
        messages.info(request, "Party Information added Successfully")
        return redirect(reverse('partyapp:add_party'))
    context = {
        'party_list': party_list,
    }
    return render(request, 'party.html', context)

def saleitem(request):
    sale_counter, created = SaleCounter.objects.get_or_create(id=1)
    sale_counter.saleno += 1
    sale_counter.save()
    current_year = datetime.now().year
    company_name = 'DM'  # Replace with your company name
    series_code = f"{company_name}/{current_year}/INV/{sale_counter.saleno}"
    items = ItemMaster.objects.all()
    return render(request, 'sale_item.html', {'items': items,'series_code': series_code})
def update_item_stock(itemname):
    try:
        # Get the ItemMaster instance by itemname
        item_master = ItemMaster.objects.get(itemname=itemname)

        # Calculate total quantity purchased for this item
        total_purchase_qty = PurchaseItem.objects.filter(itemname=item_master).aggregate(total=models.Sum('totalqty'))['total']
        total_purchase_qty = total_purchase_qty or 0  # Set to 0 if no purchases

        # Calculate total quantity sold for this item
        total_sale_qty = SaleItem.objects.filter(itemname=item_master).aggregate(total=models.Sum('totalqty'))['total']
        total_sale_qty = total_sale_qty or 0  # Set to 0 if no sales

        # Update the TotalCount field based on the calculations
        item_stock, created = ItemStockModel.objects.get_or_create(itemname=item_master)
        item_stock.TotalCount = total_purchase_qty - total_sale_qty
        item_stock.save()

    except ItemMaster.DoesNotExist:
        # Handle the case where the itemname is not found
        # You can log an error, return an error response, or perform other appropriate actions
        pass
def sale_item(request):
    if request.method == 'POST':
        sale_number = request.POST['sale_number']
        date = request.POST['date']
        party = request.POST['party']
        grandtotal = request.POST['grandtotal']

        # Create the sale model
        salemodel = SaleModel.objects.create(sale_number=sale_number, date=date, partyname=party,grandtotal=grandtotal)

        # Retrieve and process item data from the JSON field
        item_data_json = request.POST.get('item_data', '[]')
        item_data = json.loads(item_data_json)

        for item in item_data:
            itemname = item.get('itemname')

            mrp = item.get('mrp')
            unit = item.get('unit')
            purchasetax = item.get('purchasetax')
            totalqty = item.get('totalqty')
            total = item.get('total')

            SaleItem.objects.create(
                itemname=itemname,
                mrp=mrp,
                unit=unit,
                purchasetax=purchasetax,
                totalqty=totalqty,
                total=total,
                sale_model=salemodel
            )
            update_item_stock(itemname)
        upiamt = request.POST['upiamt']
        swipe = request.POST['swipe']
        cash = request.POST['cash']
        cashtendred = request.POST['cashtendred']
        balance = request.POST['balance']
        osamt = request.POST['osamt']
        creditamt = request.POST['creditamt']

        SalePayment.objects.create(
            upiamt=upiamt,
            swipe=swipe,
            cash=cash,
            cashtendred=cashtendred,
            balance=balance,
            osamt=osamt,
            creditamt=creditamt,
            payment_model=salemodel  # Link to the corresponding SaleModel
        )
        return redirect('partyapp:saleitem')

    return render(request, 'sale_item.html')
def purchaseitem(request):
    global page_load_counter  # Access the global page load counter

    # Generate the series code
    current_year = datetime.now().year
    company_name = 'DM'  # Replace with your company name
    series_code = f"{company_name}/{current_year}/PR/{page_load_counter}"

    # Increment the page load counter for the next page load
    page_load_counter += 1

    items = ItemMaster.objects.all()
    return render(request, 'purchase_item.html', {'items': items,'series_code': series_code})
def purchase_item(request):
    if request.method == 'POST':
        purchase_number = request.POST['purchase_number']
        date = request.POST['date']
        supinvoiceno = request.POST['supinvoiceno']
        supdate = request.POST['supdate']
        partyname = request.POST['party']
        grandtotal = request.POST['grandtotal']
        payment_method = request.POST['payment_method']

        # Create the sale model
        purchasemodel = PurchaseModel.objects.create(purchase_number=purchase_number, date=date, supinvoiceno=supinvoiceno,supdate=supdate,partyname=partyname,payment_method=payment_method,grandtotal=grandtotal)

        # Retrieve and process item data from the JSON field
        item_data_json = request.POST.get('item_data', '[]')
        item_data = json.loads(item_data_json)
        print(item_data)

        for item in item_data:
            itemname = item.get('itemname')
            mrp = item.get('mrp')
            unit = item.get('unit')
            purchasetax = item.get('purchasetax')
            totalqty = item.get('totalqty')
            total = item.get('total')

            PurchaseItem.objects.create(
                itemname=itemname,
                mrp=mrp,
                unit=unit,
                purchasetax=purchasetax,
                totalqty=totalqty,
                total=total,
                purchase_model=purchasemodel
            )
            update_item_stock(itemname)

        return redirect('partyapp:purchaseitem')

    return render(request, 'purchase_item.html')