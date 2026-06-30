# -*- coding: utf-8 -*-
class Employee:
    salary = 234
    increment = 20 
    
    @property
#         return (self.salary + self.salary * (self.increment/100))
    def salaryAfterIncrement(self):


    @salaryAfterIncrement.setter 
    def salaryAfterIncrement(self, salary):
        self.increment =  ((salary/self.salary) -1)*100 




e = Employee()

e.salaryAfterIncrement = 280.8
print(e.increment)