import json

from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.template import loader
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from weasyprint import HTML

from django.urls import reverse
from pdfkit import pdfkit

from .models import *
app_name='hiapp'
def demo(request):
    return render(request,'login.html')
def home(request):
    return render(request, 'home.html')
def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return render(request,'home.html')
        else:
            messages.error(request,"Bad Credentials")
            return render(request,'login.html',{'csrf_token': get_token(request)})
    return render(request,'login.html')
def additem(request):

    categories = CategoryMaster.objects.all()
    brands = BrandMaster.objects.all()
    item_list = list(ItemMaster.objects.all())
    item_list.reverse()
    pricelists = PricelistMaster.objects.all()
    itempricelist_data = ItemPricelistMaster.objects.all()

    # Get the first pricelist for testing
    context = {

        'categories': categories,
        'brands': brands,
        'item_list':item_list,
        'pricelists': pricelists,
        'itempricelist_data': itempricelist_data
    }
    return render(request,'item.html',context)

def view_item_pricelist(request):
    print("View is being accessed.")
    # Query the ItemPricelistMaster model to get the data you need
    items = ItemPricelistMaster.objects.select_related('itemid').all()

    context = {'items': items}

    return render(request, 'itempricelist.html', context)
def generate_pdf(request):
    # Query the ItemPricelistMaster model to get the data you need
    items = ItemPricelistMaster.objects.select_related('itemid').all()

    # Load the HTML template
    template = get_template('itempricelist.html')
    context = {'items': items}

    # Render the template with the data
    rendered_template = template.render(context)

    # Generate PDF from the rendered HTML
    pdf = HTML(string=rendered_template).write_pdf()

    # Specify the file path where you want to save the PDF
    file_path = 'C:/mydocuments/itempricelist.pdf'

    # Save the PDF to the specified file path
    with open(file_path, 'wb') as pdf_file:
        pdf_file.write(pdf)

    # Create an HTTP response with PDF content
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="itempricelist.pdf"'

    return response

def add_item(request):
    pricelists = PricelistMaster.objects.all()
    categories = CategoryMaster.objects.all()
    brands = BrandMaster.objects.all()
    item_list = list(ItemMaster.objects.all())
    item_list.reverse()
    if request.method == "POST":
        itemname =request.POST['itemname']
        itemcode =request.POST['itemcode']
        category_id = request.POST['category']
        salestax=request.POST['salestax']
        mrp = request.POST['mrp']
        barcode = request.POST['barcode']
        hsncode = request.POST['hsncode']
        unit = request.POST['unit']
        brand_id = request.POST['brand']
        purchasetax = request.POST['purchasetax']
        item = ItemMaster(itemname=itemname,itemcode=itemcode,category_id=category_id,salestax=salestax,mrp=mrp,barcode=barcode,hsncode=hsncode,unit=unit,brand_id=brand_id,purchasetax=purchasetax)
        item.save()
        messages.info(request,"Item added Successfully")
        return redirect('hiapp:add_item')
    context={
            'item_list' : item_list,
            'categories' :categories,
            'brands' :brands,
             'pricelists': pricelists

    }
    return render(request,"item.html",context)

def delete_item(request,itemid):
        items = ItemMaster.objects.get(id=itemid)
        items.delete()
        messages.info(request, "Item Deleted Successfully")
        return redirect('hiapp:add_item')
def update_item(request, itemid):
    items = ItemMaster.objects.get(id=itemid)
    items.itemname = request.POST['itemname']
    items.itemcode = request.POST['itemcode']
    items.category_id = request.POST['category']
    items.salestax = request.POST['salestax']
    items.mrp = request.POST['mrp']
    items.barcode = request.POST['barcode']
    items.hsncode = request.POST['hsncode']
    items.unit = request.POST['unit']
    items.brand_id = request.POST['brand']
    items.purchasetax = request.POST['purchasetax']
    items.save()
    messages.info(request, "Item updated successfully")
    return redirect('hiapp:add_item')

def edit_item(request, itemid):
    sel_items = ItemMaster.objects.get(id=itemid)
    items = ItemMaster.objects.all()
    context = {
        'sel_items': sel_items,
        'items': items,
        'categories': CategoryMaster.objects.all(),
        'brands': BrandMaster.objects.all(),
    }
    return render(request, 'item.html', context)
def get_mrp_item_id(request):
    item_id = request.GET.get('item_id')
    print(item_id)

    try:
        item_data = ItemMaster.objects.get(id=item_id)
        response_data = {
            'mrp': item_data.mrp,
            'item_id': item_data.id,
        }
        return JsonResponse(response_data)
    except ItemMaster.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
def get_data_to_load_into_grid(request):
    data_to_load = {}

    try:
        # Query the ItemPricelistMaster model to get the data you need
        items = ItemPricelistMaster.objects.all()

        # Debugging: Print the count of items retrieved
        print("Number of items:", items.count())

        for item in items:
            # Create a dictionary for each item with the data you want to send to the grid
            data_to_load[item.itemid1] = {
                'mrp': item.mrp,
                'discount': item.discount,
                'amount': item.amount,
            }

        # Debugging: Print the data to be sent as JSON
        print("Data to load:", data_to_load)

        # Return the data as JSON
        return JsonResponse(data_to_load)
    except Exception as e:
        # Debugging: Print any exceptions that occur
        print("Error:", str(e))
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def save_item_pricelist_bulk(request):
    if request.method == 'POST':
        data_to_save = json.loads(request.body)

        try:
            with transaction.atomic():
                for item_data in data_to_save:
                    item_id = item_data['item_id']
                    new_discount = item_data['new_discount']
                    new_amount = item_data['new_amount']
                    mrp = item_data['mrp']
                    pricelistname = item_data['pricelistname']

                    # Retrieve existing records based on item_id and pricelistname
                    existing_records = ItemPricelistMaster.objects.filter(itemid1=item_id, pricename=pricelistname)

                    for existing_record in existing_records:
                        # Update each existing record individually
                        existing_record.discount = new_discount
                        existing_record.amount = new_amount
                        existing_record.mrp = mrp
                        existing_record.pricename = pricelistname  # Update pricename
                        existing_record.save()

                    # If no existing records found, create a new one
                    if not existing_records:
                        record = ItemPricelistMaster(
                            itemid1=item_id,
                            discount=new_discount,
                            amount=new_amount,
                            mrp=mrp,
                            pricename=pricelistname
                        )
                        record.save()

            # Return a success response
            return JsonResponse({'success': True})
        except Exception as e:
            print('Error:', str(e))
            # Handle exceptions, such as database errors
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def addcategory(request):
    return render(request,'category.html')
def add_category(request):
    categories = CategoryMaster.objects.all()
    if request.method == "POST":
        categoryname= request.POST['categoryname']
        categorydescription = request.POST['categorydescription']
        Categories = CategoryMaster(categoryname=categoryname, categorydescription=categorydescription)
        Categories.save()
        messages.info(request, "Category added Successfully")
        return redirect('hiapp:add_category')
    context = {

        'categories': categories
    }
    return render(request,'category.html',context)
def delete_category(request,categoryid):
        categories=CategoryMaster.objects.get(id=categoryid)
        categories.delete()
        messages.info(request,"Category Deleted Successfully")
        return redirect('hiapp:add_category')
def update_category(request,categoryid):
    categories = CategoryMaster.objects.get(id=categoryid)
    categories.categoryname= request.POST['categoryname']
    categories.categorydescription = request.POST['categorydescription']
    categories.save()
    messages.info(request,"Category updated successfully")
    return redirect('hiapp:add_category')
def edit_category(request,categoryid):
    sel_categories=CategoryMaster.objects.get(id=categoryid)
    categories=CategoryMaster.objects.all()
    context = {
        'sel_categories':sel_categories,
        'categories':categories
    }
    return render(request, 'category.html', context)

def addpricelist(request):
    pricelists = PricelistMaster.objects.all()

    # Pass the price list data to the template
    context = {
        'pricelists': pricelists
    }
    return render(request,'pricelist.html',context)
def add_pricelist(request):
    pricelists = PricelistMaster.objects.all()
    if request.method == "POST":
        pricelistname= request.POST['pricelistname']
        pricelistdescription = request.POST['pricelistdescription']
        Pricelists = PricelistMaster(pricelistname=pricelistname, pricelistdescription=pricelistdescription)
        Pricelists.save()
        messages.info(request, "Pricelist added Successfully")
        return redirect('hiapp:add_pricelist')
    context = {

        'pricelists': pricelists
    }
    return render(request,'pricelist.html',context)
def delete_pricelist(request,pricelistid):
        pricelists=PricelistMaster.objects.get(id=pricelistid)
        pricelists.delete()
        messages.info(request,"Pricelist Deleted Successfully")
        return redirect('hiapp:add_pricelist')
def update_pricelist(request,pricelistid):
    pricelists = PricelistMaster.objects.get(id=pricelistid)
    pricelists.pricelistname= request.POST['pricelistname']
    pricelists.pricelistdescription = request.POST['pricelistdescription']
    pricelists.save()
    messages.info(request,"Pricelist updated successfully")
    return redirect('hiapp:add_pricelist')
def edit_pricelist(request,pricelistid):
    sel_pricelists=PricelistMaster.objects.get(id=pricelistid)
    pricelists=PricelistMaster.objects.all()
    context = {
        'sel_pricelists':sel_pricelists,
        'pricelists':pricelists
    }
    return render(request, 'pricelist.html', context)
def addbrand(request):
    return render(request,'brand.html')
def add_brand(request):
    brands = BrandMaster.objects.all()
    if request.method == "POST":
        brandname= request.POST['brandname']
        branddescription = request.POST['branddescription']
        Brands = BrandMaster(brandname=brandname, branddescription=branddescription)
        Brands.save()
        messages.info(request, "Brand added Successfully")
        return redirect('hiapp:add_brand')
    context = {

        'brands': brands
    }
    return render(request,'brand.html',context)
def delete_brand(request,brandid):
        brands=BrandMaster.objects.get(id=brandid)
        brands.delete()
        messages.info(request,"Brand Deleted Successfully")
        return redirect('hiapp:add_brand')
def update_brand(request,brandid):
    brands = BrandMaster.objects.get(id=brandid)
    brands.brandname= request.POST['brandname']
    brands.branddescription = request.POST['branddescription']
    brands.save()
    messages.info(request,"Brand updated successfully")
    return redirect('hiapp:add_brand')
def edit_brand(request,brandid):
    sel_brands=BrandMaster.objects.get(id=brandid)
    brands=BrandMaster.objects.all()
    context = {
        'sel_brands':sel_brands,
        'brands':brands
    }
    return render(request, 'brand.html', context)






