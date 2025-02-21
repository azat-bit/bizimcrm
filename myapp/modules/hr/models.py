from django.db import models

class JobPosition(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    job_position = models.ForeignKey(JobPosition, on_delete=models.SET_NULL, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    hire_date = models.DateField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job_position.title}"

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.DateField()
    salary_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.first_name} - {self.month}"

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Beklemede'),
        ('approved', 'Onaylandı'),
        ('denied', 'Reddedildi'),
    ], default='pending')

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.status}"
