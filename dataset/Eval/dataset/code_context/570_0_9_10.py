# -*- coding: utf-8 -*-
marks1 = int(input("Enter Marks 1: "))
marks2 = int(input("Enter Marks 2: "))
marks3 = int(input("Enter Marks 3: "))

# Check for total percentage
total_percentage = (100*(marks1 + marks2 + marks3))/300


    print("You are passed:", total_percentage)

else:
    print("You failed, try again next year:", total_percentage)
