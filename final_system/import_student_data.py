# import_student_data.py
import pandas as pd
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final_system')  # Adjust 'myproject' to your project's name
django.setup()

from final_system.models import studentInfo  # Import your model

# Read the Excel file
file_path = 'bsit-student-profilenew.xlsx'  # Adjust this to your actual file path
df = pd.read_excel(file_path)

# Iterate over the rows and save data to the database
for _, row in df.iterrows():
    student = studentInfo(
        studID=row['studID'],
        lrn=row['lrn'],
        lastname=row['lastname'],
        firstname=row['firstname'],
        middlename=row['middlename'],
        degree=row['degree'],
        yearlvl=row['yearlvl'],
        sex=row['sex'],
        emailadd=row['emailadd'],
        contact=row['contact']
    )
    student.save()

print("Data imported successfully!")
