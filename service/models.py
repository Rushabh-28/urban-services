from django.db import models
from user.models import User


cityChoices = (
("Kolhapur","Kolhapur"),
("Mumbai","Mumbai"),
("Surat","Surat"),
("Ahmedabad","Ahmedabad"),
("Pune","Pune"),
("Gandhinagar","Gandhinagar"),
)

stateChoices = (
("Gujarat","Gujarat"),
("Maharashtra","Maharashtra"),
)

class Cat(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Subcategory(models.Model):
    cat = models.ForeignKey(Cat,on_delete=models.CASCADE,null = True)#choices=catChoices)        
    name = models.CharField(max_length=255)

    
    def __str__(self):
        return self.name
    
class Type(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    cat = models.ForeignKey(Cat,on_delete=models.CASCADE)#choices=catChoices)        
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE)#choices=subcategoryChoices)
    type = models.ForeignKey(Type,on_delete=models.CASCADE)#choices=typeChoices)
    fees_amount = models.DecimalField(max_digits=10, decimal_places=2)
    area = models.CharField(max_length=255)
    city = models.CharField(max_length=255,choices=cityChoices)
    state = models.CharField(max_length=255,choices=stateChoices)
    serviceprovider = models.ForeignKey(User,on_delete=models.CASCADE, null = True)

    class Meta:
        db_table = "service"
        
        
    def __str__(self):
            return self.name
        
        

class Urban(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    urbanImage = models.ImageField(upload_to="uploads/")
    
    
    
    class Meta:
        db_table = "urban"
    
    def __str__(self):
        return self.name


