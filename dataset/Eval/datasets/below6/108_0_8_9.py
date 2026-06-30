# -*- coding: utf-8 -*-
class Employee:
    salary = 234
    increment = 20 
    
    @property
    def salaryAfterIncrement(self):


    @salaryAfterIncrement.setter 
    def salaryAfterIncrement(self, salary):
        self.increment =  ((salary/self.salary) -1)*100 

#         return (self.salary + self.salary * (self.increment/100))



e = Employee()

e.salaryAfterIncrement = 280.8
print(e.increment)