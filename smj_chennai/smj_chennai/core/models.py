from django.db import models

# Create your models here.
class Documents(models.Model):
    docket_date = models.DateTimeField()
    docket_number = models.IntegerField()
    party = models.ForeignKey("Party", models.DO_NOTHING, db_column="party")
    no_of_pack = models.IntegerField()
    station = models.CharField(max_length=10)
    weight = models.FloatField()
    rate = models.FloatField()
    charge = models.FloatField()
    other_charge = models.FloatField()
    total = models.FloatField()
    paid = models.FloatField()
    dispatch = models.CharField(max_length=50)
    pay_mode = models.CharField(max_length=50)
    bill_status = models.CharField(max_length=50)
    remarks = models.CharField(max_length=250)
    cgst = models.FloatField()
    sgst = models.FloatField()
    igst = models.FloatField()
    round_amt = models.FloatField()
    type = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "documents"


class Party(models.Model):
    name = models.CharField(unique=True, max_length=250)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = "party"


class Charges(models.Model):
    document = models.OneToOneField("Documents", models.DO_NOTHING)
    lr_date = models.DateField()
    dispatch_expense = models.FloatField()
    dispatch_paid_on = models.DateTimeField(blank=True, null=True)
    door_delivery_expense = models.FloatField()
    door_delivery_paid_on = models.DateField(blank=True, null=True)
    pay_method = models.CharField(max_length=50)
    any_other_expense = models.FloatField(blank=True, null=True)
    any_other_expense_paid_on = models.DateTimeField(blank=True, null=True)
    any_other_expense_pay_method = models.CharField(
        max_length=50, blank=True, null=True
    )
    party = models.ForeignKey("Party", models.DO_NOTHING, db_column="party")
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "charges"
