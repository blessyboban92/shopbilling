from django.db import models
from hiapp.models import ItemMaster
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

app_name = 'hiapp'


class PartyMaster(models.Model):
    partyname = models.CharField(max_length=30)
    partycode = models.CharField(max_length=10)
    address1 = models.TextField()
    address2 = models.TextField()
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=20)
    pin = models.CharField(max_length=10)
    mobile1 = models.CharField(max_length=12)
    mobile2 = models.CharField(max_length=12)
    email = models.CharField(max_length=40)
    gst = models.CharField(max_length=5)
    pricelist = models.CharField(max_length=15)

    def __str__(self):
        return self.partyname
class SaleCounter(models.Model):
    saleno = models.PositiveIntegerField(default=1)

class SaleModel(models.Model):
    sale_number = models.CharField(max_length=20)
    date = models.DateField(auto_now=True,auto_now_add=False)
    party = models.ForeignKey(PartyMaster, on_delete=models.CASCADE, null=True, default=None)
    partyname = models.CharField(max_length=40)
    grandtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.sale_number

class SaleItem(models.Model):
    itemname = models.CharField(max_length=100,null=True, blank=True)
    mrp = models.IntegerField(null=True, blank=True)
    unit = models.CharField(max_length=15,null=True,blank=True)
    purchasetax = models.IntegerField(null=True,blank=True)
    totalqty = models.IntegerField(null=True,blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    sale_model = models.ForeignKey(SaleModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.itemname
class PurchaseModel(models.Model):
    PAYMENT_CHOICES = (
        ('cash', 'Cash Purchase'),
        ('credit', 'Credit'),
    )
    purchase_number = models.CharField(max_length=15)
    date = models.DateField(auto_now=True,auto_now_add=False)
    supinvoiceno = models.CharField(max_length=15)
    supdate = models.DateField(auto_now=True,auto_now_add=False)
    party = models.ForeignKey(PartyMaster, on_delete=models.CASCADE, null=True, default=None)
    partyname = models.CharField(max_length=40)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    grandtotal= models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.purchase_number
class PurchaseItem(models.Model):
    itemname = models.CharField(max_length=100,null=True, blank=True)
    mrp = models.IntegerField(null=True, blank=True)
    unit = models.CharField(max_length=15,null=True,blank=True)
    purchasetax = models.IntegerField(null=True,blank=True)
    totalqty = models.IntegerField(null=True,blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    purchase_model = models.ForeignKey(PurchaseModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.itemname
class SalePayment(models.Model):
    upiamt = models.DecimalField(max_digits=10, decimal_places=2)
    swipe = models.DecimalField(max_digits=10, decimal_places=2)
    cash = models.DecimalField(max_digits=10,decimal_places=2)
    cashtendred = models.DecimalField(max_digits=10,decimal_places=2)
    balance = models.DecimalField(max_digits=10,decimal_places=2)
    osamt = models.DecimalField(max_digits=10,decimal_places=2)
    creditamt = models.DecimalField(max_digits=10,decimal_places=2)
    payment_model = models.ForeignKey(SaleModel, on_delete=models.CASCADE)
class ItemStockModel(models.Model):
    date = models.DateField(auto_now_add=True)
    itemname = models.ForeignKey(ItemMaster, on_delete=models.CASCADE)
    TotalCount = models.IntegerField(default=0)

    def update_stock_count(self):
        # Calculate total quantity purchased for this item
        total_purchase_qty = PurchaseItem.objects.filter(itemname=self.itemname).aggregate(total=models.Sum('totalqty'))['total']
        total_purchase_qty = total_purchase_qty or 0  # Set to 0 if no purchases

        # Calculate total quantity sold for this item
        total_sale_qty = SaleItem.objects.filter(itemname=self.itemname).aggregate(total=models.Sum('totalqty'))['total']
        total_sale_qty = total_sale_qty or 0  # Set to 0 if no sales

        # Update the TotalCount field based on the calculations
        self.TotalCount = total_purchase_qty - total_sale_qty
        self.save()
# @receiver([post_save, post_delete], sender=PurchaseItem)
# @receiver([post_save, post_delete], sender=SaleItem)







