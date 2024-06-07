from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import studentInfo, scholars, Requirement, applicants
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import RequirementForm, applicantsForm
from .models import scholars, SemesterDetails
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Sum

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@login_required
def adminhome(request):
    return render(request, 'adminhome.html', {})

def studenthome(request):
    return render(request, 'studenthome.html', {})

def logoutuser(request):
    logout(request)
    return redirect('signinuser')

def signupuser(request):
    error_message = None
    success_message = None

    if request.method == 'POST':
        studentID = request.POST.get('studID')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        try:
            student = studentInfo.objects.get(studID=studentID)
        except studentInfo.DoesNotExist:
            error_message = 'Invalid student ID.'

        if not error_message:
            if cpassword != password:
                error_message = 'Passwords do not match.'
            elif len(password) < 8:
                error_message = 'Password must be at least 8 characters.'
            elif User.objects.filter(username=studentID).exists():
                error_message = 'Student ID already exists.'
            elif User.objects.filter(email=email).exists():
                error_message = 'Email already exists.'
            else:
                user = User.objects.create_user(username=studentID, email=email, password=password)
                user.save()
                success_message = 'Account created successfully'
                return redirect('signinuser')

    return render(request, 'register.html', {'error_message': error_message, 'success_message': success_message})

def signinuser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('set_password')

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                return redirect('studenthome')
            else:
                messages.error(request, 'Invalid email or password')
        except User.DoesNotExist:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect('adminhome')
                else:
                    return redirect('studenthome')
            else:
                messages.error(request, 'Invalid email or password')

    return render(request, 'log.html')

def studentapplicationform(request):
    studID = request.user.username
    student = get_object_or_404(studentInfo, studID=studID)
    passed = applicants.objects.filter(studID_id=studID).exists()
    note = applicants.objects.filter(~Q(note=""), note__isnull=False)
    application_data = applicants.objects.filter(studID__studID=studID).first()
    context = {'student': student, 'passed': passed, 'note': note}
    print(note)

    if request.method == 'POST':
        action = request.POST.get('action')
        student_ID = request.POST.get('studID')
        print("1")
        if action == 'submit':
            print("2")
            form = applicantsForm(request.POST, request.FILES)
            print("3")
            # Check if the requirement already exists and note exists
            if application_data and note:
                print("4")
                cor_file = request.FILES.get('cor_file')
                grade_file = request.FILES.get('grade_file')
                schoolid_file = request.FILES.get('schoolid_file')
                scholar_type = request.POST.get('scholar_type')
                gpa = request.POST.get('gpa')
                print("5")
                # Update application data
                if cor_file:
                    print("6")
                    application_data.cor_file = cor_file
                print("7")
                if grade_file:
                    print("8")
                    application_data.grade_file = grade_file
                print("9")
                if schoolid_file:
                    print("10")
                    application_data.schoolid_file = schoolid_file
                print("11")
                if scholar_type:
                    print("12")
                    application_data.scholar_type = scholar_type
                print("13")
                if gpa:
                    print("14")
                    application_data.gpa = gpa
                print("15")
                application_data.note = ""
                application_data.save()
                return redirect('studentapplication')
            else:
                # Check if the requirement already exists
                if applicants.objects.filter(studID_id=student_ID).exists() and not note:
                    print("student id already exists")
                    context['error'] = "Student ID already exists"
                else:
                    if form.is_valid():
                        form.save()
                        print("form saved")
                        if applicants.objects.filter(studID_id=student_ID).exists():
                            passed = True
                        context.update({'passed': passed})
                        return render(request, 'studentapplicationform.html', context)  # Redirect to the same page or any other success page
                    else:
                        # Print form errors for debugging
                        print(form.errors)  # Add this line to print the form errors to the console
                        print("error form")

    return render(request, 'studentapplicationform.html', context)


def adminapplication(request):
    studID = request.user.username
    scholar_type = request.GET.get('scholar_type')
    context = {}

    if request.method == 'POST':
        action = request.POST.get('action')
        applicant_id = request.POST.get('applicant_id')
        note = request.POST.get('note')  # Changed from notee to note
        
        if action == 'UPDATE':
            try:
                application_data = applicants.objects.get(id=applicant_id)
                if note:  # Check if note is not empty
                    application_data.note = note
                    application_data.save()
                    print("Note updated")
            except applicants.DoesNotExist:
                print("Applicant not found")
        elif action == 'ACCEPT':
            try:
                application_data = applicants.objects.get(id=applicant_id)
                application_data.status = "ACCEPTED"
                application_data.save()
                print("Application accepted")
            except applicants.DoesNotExist:
                print("Applicant not found")
        elif action == 'REJECTED':
            try:
                application_data = applicants.objects.get(id=applicant_id)
                application_data.delete()
                print("Application rejected")
            except applicants.DoesNotExist:
                print("Applicant not found")
        
    # Query applicant_data based on scholar_type
    if scholar_type:
        student_data = studentInfo.objects.all()
        if scholar_type == 'all':
            applicant_data = applicants.objects.filter(status='PENDING')
        else:
            applicant_data = applicants.objects.filter(status='PENDING', scholar_type=scholar_type)
    else:
        student_data = studentInfo.objects.all()
        applicant_data = applicants.objects.filter(status='PENDING')

    context = { 'student_data': student_data, 'applicant_data': applicant_data }
    
    return render(request, 'adminapplication.html', context)

@login_required
def adminreqsubmission(request):
    student_type = request.GET.get('student_type')
    context = {}

    if student_type == 'SCHOLAR':
        scholar_data = scholars.objects.all()
        requirement_data = Requirement.objects.filter(type='SCHOLAR')
        context = {
            'student_type': student_type,
            'scholar_data': scholar_data,
            'requirement_data': requirement_data,
        }
        for scholar in requirement_data:
            print("COR File URL:", scholar.cor_file.url)
            print("Grade File URL:", scholar.grade_file.url)
            print("School ID File URL:", scholar.schoolid_file.url)
            print()
    elif student_type == 'NON_SCHOLAR':
        scholar_data = scholars.objects.all()
        requirement_data = Requirement.objects.filter(type='NONSCHOLAR')
        context = {
            'student_type': student_type,
            'requirement_data': requirement_data,
        }
    
    return render(request, 'adminrequirements.html', context)


def studentreqsubmission(request):
    studID = request.user.username  # Get the logged-in user's student ID
    print("student id of the logged in user: ", studID)
    semester = request.POST.get('semester')
    passed = Requirement.objects.filter(studID_id=studID).exists()  # Check if the student ID and semester exist in the Requirement class
    student = get_object_or_404(studentInfo, studID=studID)

    # Print all records of the Requirement class
    requirements = Requirement.objects.all()
    for req in requirements:
        print(f"ID: {req.id}")
        print(f"Student ID: {req.studID.studID}")
        print(f"Semester: {req.semester}")
        print(f"GPA: {req.gpa}")
        print(f"COR File: {req.cor_file.url if req.cor_file else 'No COR File'}")
        print(f"Grade File: {req.grade_file.url if req.grade_file else 'No Grade File'}")
        print(f"School ID File: {req.schoolid_file.url if req.schoolid_file else 'No School ID File'}")
        print(f"Submission Date: {req.submission_date}")
        print(f"Units: {req.units}")
        print(f"Note: {req.note}")
        print(f"Type: {req.type}")
        print("---------------")

    context = {
        'student': student,
        'passed': passed
    }
    print(context)
    return render(request, 'studentrequirements.html', context)


def save_requirements(request):
    passed = False
    if request.method == 'POST':
        student_ID = request.POST.get('student_ID')
        semester = request.POST.get('semester')

        # Check if the requirement already exists
        if Requirement.objects.filter(studID_id=student_ID, semester=semester).exists():
            messages.error(request, 'You already have passed the requirements for this semester.')
        else:
            form = RequirementForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Requirements submitted successfully.')
                if Requirement.objects.filter(studID_id=student_ID, semester=semester).exists():
                    passed = True
                return render(request, 'studentrequirements.html', {'passed': passed})  # Redirect to the same page or any other success page
            else:
                # Print form errors for debugging
                print(form.errors)  # Add this line to print the form errors to the console
                messages.error(request, 'Error in form submission.')

        return render(request, 'studentrequirements.html', {'form': form, 'student': student})  # Pass form back to the template
    else:
        form = RequirementForm()
        student = get_object_or_404(studentInfo, studID=request.user.username)
    return render(request, 'studentrequirements.html', {'form': form, 'student': student})
                  
def calculate_gpa_from_text(text):
    grades_units = {}
    total_units = 0  # Initialize total units
    for line in text.split('\n'):
        parts = line.split()
        if len(parts) >= 3:
            subject = ' '.join(parts[:-2])
            try:
                grade = float(parts[-2])
                units = float(parts[-1])
                grades_units[subject] = (grade, units)
                total_units += units  # Accumulate total units
            except ValueError:
                continue
        elif line.startswith("Total units"):
            total_units = float(line.split()[-1])  # Extract total units from "Total units" line

    grade_points_mapping = {
        4.0: 4.0,
        3.5: 3.5,
        3.0: 3.0,
        2.5: 2.5,
        2.0: 2.0,
        1.5: 1.5,
        1.0: 1.0,
        0.0: 0.0
    }

    total_grade_points = 0

    for grade, units in grades_units.values():
        total_grade_points += grade_points_mapping.get(grade, 0) * units

    gpa = total_grade_points / total_units if total_units > 0 else 0

    return round(gpa, 2), total_units, total_grade_points

def process_grade_image(request):
    if request.method == 'POST' and request.FILES.get('gradeFile'):
        grade_file = request.FILES['gradeFile']
        fs = FileSystemStorage()
        filename = fs.save(grade_file.name, grade_file)
        file_path = fs.path(filename)

        # Preprocess the image for better OCR accuracy
        image = Image.open(file_path)
        image = image.convert('L')  # Convert to grayscale
        image = image.filter(ImageFilter.SHARPEN)  # Sharpen the image
        image = ImageEnhance.Contrast(image).enhance(2)  # Enhance contrast
        extracted_text = pytesseract.image_to_string(image)

        # Print the extracted text in the terminal
        print("Extracted Text:")
        print(extracted_text)

        # Calculate GPA, total units, and total grade points from the extracted text
        gpa, total_units, total_grade_points = calculate_gpa_from_text(extracted_text)

        # Clean up the uploaded file
        os.remove(file_path)

        # Print the values in the terminal
        print("GPA:", gpa)
        print("Total Units:", total_units)
        print("Total Grade Points:", total_grade_points)

        return JsonResponse({'success': True, 'gpa': gpa, 'total_units': total_units})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

def scholars_profile_admin(request):
    studID = request.user.username
    scholar_type = request.GET.get('scholar_type', '').lower()  # Convert to lowercase
    context = {}
    
    if request.method == 'POST':
        action = request.POST.get('action')
        applicant_id = request.POST.get('applicant_id')
        amount = request.POST.get('amount')
        year = request.POST.get('year')

        if action == 'ADD':
            applicant = applicants.objects.get(pk=applicant_id)
            if applicant.gpa <= 3:
                scholar = scholars.objects.create(
                    studID=applicant.studID,
                    scholar_type=applicant.scholar_type,
                    amount=amount,
                    gpa=applicant.gpa,
                    year=year,
                    remarks="PASSED"
                )
                scholar.save()
                print("data save.")
                applicant.status = 'APPROVED'  # Update status to 'APPROVED'
                applicant.save()
                return redirect('profile')
        
    if scholar_type == 'ched full merit':
        student_data = studentInfo.objects.all()
        applicant_data = applicants.objects.filter(status='ACCEPTED', scholar_type='ched full merit')
        context = { 'student_data': student_data, 'applicant_data': applicant_data }
    elif scholar_type == 'ched half merit':
        student_data = studentInfo.objects.all()
        applicant_data = applicants.objects.filter(status='ACCEPTED', scholar_type='ched half merit')
        context = { 'student_data': student_data, 'applicant_data': applicant_data }
    elif scholar_type == 'ched tulong dunong':
        student_data = studentInfo.objects.all()
        applicant_data = applicants.objects.filter(status='ACCEPTED', scholar_type='ched tulong dunong')
        context = { 'student_data': student_data, 'applicant_data': applicant_data }
    elif scholar_type == 'ched tes':
        student_data = studentInfo.objects.all()
        applicant_data = applicants.objects.filter(status='ACCEPTED', scholar_type='ched tes')
        context = { 'student_data': student_data, 'applicant_data': applicant_data }
    elif scholar_type == 'ateasp':
        student_data = studentInfo.objects.all()
        applicant_data = applicants.objects.filter(status='ACCEPTED', scholar_type='ateasp')
        context = { 'student_data': student_data, 'applicant_data': applicant_data }
    elif scholar_type == 'dost undergrad':
        student_data = studentInfo.objects.all()
        applicant_data = applicants.objects.filter(status='ACCEPTED', scholar_type='dost undergrad')
        context = { 'student_data': student_data, 'applicant_data': applicant_data }
    elif scholar_type == 'with high honor':
        student_data = studentInfo.objects.all()
        applicant_data = applicants.objects.filter(status='ACCEPTED', scholar_type='with high honor')
        context = { 'student_data': student_data, 'applicant_data': applicant_data }
    elif scholar_type == 'natures spring':
        student_data = studentInfo.objects.all()
        applicant_data = applicants.objects.filter(status='ACCEPTED', scholar_type='natures spring')
        context = { 'student_data': student_data, 'applicant_data': applicant_data }
    elif scholar_type == 'life foundation':
        student_data = studentInfo.objects.all()
        applicant_data = applicants.objects.filter(status='ACCEPTED', scholar_type='life foundation')
        context = { 'student_data': student_data, 'applicant_data': applicant_data }
    elif scholar_type == 'all':
        student_data = studentInfo.objects.all()
        applicant_data = applicants.objects.filter(status='ACCEPTED')
        context = { 'student_data': student_data, 'applicant_data': applicant_data }
    else:
        student_data = studentInfo.objects.all()
        applicant_data = applicants.objects.filter(status='ACCEPTED')
        context = { 'student_data': student_data, 'applicant_data': applicant_data }
    return render(request, 'scholarsprofileadmin.html', context)

    
    # scholar_type = request.GET.get('scholar_type')
    # context = {}
    # print(scholar_type)
    
    
    
    # if scholar_type:
    #     if scholar_type == 'all':
    #         application_data = applicants.objects.filter(status='ACCEPTED')
    #     elif scholar_type == 'ched full merit':
    #         application_data = applicants.objects.filter(status='ACCEPTED', scholar_type=scholar_type)
    #     elif scholar_type == 'ched half merit':
    #         application_data = applicants.objects.filter(status='ACCEPTED', scholar_type=scholar_type)
    #     elif scholar_type == 'ched tulong dunong':
    #         application_data = applicants.objects.filter(status='ACCEPTED', scholar_type=scholar_type)
    #     elif scholar_type == 'ched tes':
    #         application_data = applicants.objects.filter(status='ACCEPTED', scholar_type=scholar_type)
    #     elif scholar_type == 'ateasp':
    #         application_data = applicants.objects.filter(status='ACCEPTED', scholar_type=scholar_type)
    #     elif scholar_type == 'dost undergrad':
    #         application_data = applicants.objects.filter(status='ACCEPTED', scholar_type=scholar_type)
    #     elif scholar_type == 'with high honor':
    #         application_data = applicants.objects.filter(status='ACCEPTED', scholar_type=scholar_type)
    #     elif scholar_type == 'natures spring':
    #         application_data = applicants.objects.filter(status='ACCEPTED', scholar_type=scholar_type)
    #     elif scholar_type == 'life foundation':
    #         application_data = applicants.objects.filter(status='ACCEPTED', scholar_type=scholar_type)
    #     else:
    #         application_data = applicants.objects.filter(status='ACCEPTED')
    # else:
    #     application_data = applicants.objects.filter(status='ACCEPTED')
    
    # student_data = studentInfo.objects.all()
    # context = { 'student_data': student_data, 'application_data': application_data }
    
    return render(request, 'scholarsprofileadmin.html', context)

        
    # print("Request method:", request.method)
    # if request.method == 'POST':
    #     applicant_id = request.POST.get('applicant_id')
    #     print("Applicant ID from POST:", applicant_id)
    #     if applicant_id:
    #         try:
    #             application_data = applicants.objects.filter(id=applicant_id)
    #             print("Application data:", application_data)
    #         except applicants.DoesNotExist:
    #             print("Applicant does not exist")
    #             application_data = []
    # else:
    #     application_data = applicants.objects.all()
    #     print("All application data:", application_data)
        
    
    

def add_scholar(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        applicant_id = request.POST.get('applicant_id')
        
        if action == 'ADD':
            try:
                applicant = applicants.objects.get(id=applicant_id)
                scholar_id = request.POST.get('scholarid')
                amount = request.POST.get('amount')
                gpa = applicant.gpa
                year = request.POST.get('year')

                # Calculate remarks based on GPA
                remarks = "PASSED" if gpa <= 3 else "FAILED"

                # Create a new scholar entry
                scholar = scholars.objects.create(
                    scholar_ID=scholar_id,
                    studID=applicant.studID,
                    scholar_type=applicant.scholar_type,
                    amount=amount,
                    gpa=gpa,
                    year=year,
                    remarks=remarks
                )

                # Set the status of the applicant to 'ACCEPTED'
                applicant.status = 'APPROVED'
                applicant.save()
                print("saved")
                return redirect('profile')
            except Exception as e:
                return redirect('profile')
            


def scholars_profile_student(request):
    studID = request.user.username
    application_data = applicants.objects.filter(studID__studID=studID).first()
    student_data = studentInfo.objects.filter(studID=studID).first()
    scholars_table = scholars.objects.filter(studID_id=studID).first()
    note = applicants.objects.filter(~Q(note=""), note__isnull=False)
    app_exist = application_data is not None
    exist = scholars_table is not None
    edit_mode = False
    
    print("1")
    if request.method == 'POST':
        print("2")
        action = request.POST.get('action')
        print("3")
        if action == 'EDIT':
            print("4")
            edit_mode = True
        elif action == 'DONE':
            print("5")
            if application_data:
                print("6")
                cor_file = request.FILES.get('cor_file')
                print("7")
                grade_file = request.FILES.get('grade_file')
                print("8")
                schoolid_file = request.FILES.get('schoolid_file')
                print("COR: ",cor_file)
                print("GRADE: ", grade_file)
                print("SCHOOL ID: ", schoolid_file)
                print("9")
                
                if cor_file:
                    print("10")
                    application_data.cor_file = cor_file
                    print("11")
                if grade_file:
                    print("12")
                    application_data.grade_file = grade_file
                    print("13")
                if schoolid_file:
                    print("14")
                    application_data.schoolid_file = schoolid_file
                    print("15")
                print("16")
                application_data.gpa = request.POST.get('gpa', application_data.gpa)
                print("17")
                application_data.save()
                print("18")
            print("19")
            edit_mode = False
        elif action == 'CANCEL':
            print("20")
            if application_data:
                print("21")
                application_data.delete()
                return redirect('profile_student')

    context = {
        'application_data': application_data,
        'student_data': student_data,
        'scholars_table': scholars_table,
        'app_exist': app_exist,
        'exist': exist,
        'note': note,
        'edit_mode': edit_mode,
        'cor_file_url': application_data.cor_file.url if application_data and application_data.cor_file else None,
        'grade_file_url': application_data.grade_file.url if application_data and application_data.grade_file else None,
        'schoolid_file_url': application_data.schoolid_file.url if application_data and application_data.schoolid_file else None,
        'gpa_current': application_data.gpa if application_data and application_data.gpa else None,
    }
    
    return render(request, 'scholarsprofilestudent.html', context)


def grade_submission(request):
    return render(request, 'gradesubmission.html', {})

def mentorship(request):
    return render(request, 'mentorship.html', {})



def search_student(request):
    query = request.GET.get('search_id')
    student = None
    invalid = False
    invalid_input = False
    is_scholar = False
    not_scholar = False
    scholar = None  # Initialize scholar object to None
    if query:
        if query.isnumeric():
            try:
                student = studentInfo.objects.get(studID=query)
                # Check if the student is a scholar
                if scholars.objects.filter(studID=query).exists():
                    scholar = scholars.objects.get(studID=query)
                    is_scholar = True
                    not_scholar = False
                    print("Not: ",not_scholar)
                    print("Yes: ",is_scholar)
                else:
                    not_scholar = True
                    is_scholar = False
                    print("Not: ",not_scholar)
                    print("Yes: ",is_scholar)
            except studentInfo.DoesNotExist:
                student = None
                invalid = True
        else:
            invalid_input = True
    return render(request, 'scholarsprofileadmin.html', {'student': student, 'invalid': invalid, 'invalid_input': invalid_input, 'is_scholar': is_scholar, 'scholar': scholar, 'not_scholar': not_scholar})


# ------------------------------------    dayag code    --------------------
def chedreports(request):
    return render(request, 'chedreports.html', {})


def chedreports_merit(request):
    # Get the selected semester and year from the GET parameters
    selected_semester = request.GET.get('semester', 'all')
    selected_year = request.GET.get('scholarship_year', '')

    # Fetch scholars based on the selected criteria
    scholars_list = scholars.objects.filter(scholar_type__in=['Full Merit', 'Half Merit'])

    if selected_semester != 'all' or selected_year:
        scholar_ids = SemesterDetails.objects.all()
        
        if selected_semester != 'all':
            scholar_ids = scholar_ids.filter(semester=selected_semester)
        
        if selected_year:
            scholar_ids = scholar_ids.filter(year=selected_year)
        
        scholar_ids = scholar_ids.values_list('scholar_id', flat=True)
        scholars_list = scholars_list.filter(scholar_ID__in=scholar_ids)

    context = {
        'scholars': scholars_list,
        'semester': selected_semester,
        'scholarship_year': selected_year,
    }
    return render(request, 'dayag/ched_merit.html', context)

def chedreports_TES(request):
    return render(request, 'dayag/ched_tes.html', {})

from django.shortcuts import render
from django.db.models import Sum
from .models import scholars, SemesterDetails

def chedreports_TDP(request):
    tulong_dunong_program_scholars = scholars.objects.filter(scholar_type='Tulong Dunong Program')
    
    for scholar in tulong_dunong_program_scholars:
        first_semester_details = scholar.semester_details.filter(semester='1').first()
        second_semester_details = scholar.semester_details.filter(semester='2').first()
        
        scholar.total_1st_semester = first_semester_details.amount if first_semester_details else 0
        scholar.date_received_1st_semester = first_semester_details.date_added if first_semester_details else None
        
        scholar.total_2nd_semester = second_semester_details.amount if second_semester_details else 0
        scholar.date_received_2nd_semester = second_semester_details.date_added if second_semester_details else None
        
        # Print statements for debugging
        print(f"Scholar ID: {scholar.scholar_ID}")
        print(f"1st Semester - Amount: {scholar.total_1st_semester}, Date Received: {scholar.date_received_1st_semester}")
        print(f"2nd Semester - Amount: {scholar.total_2nd_semester}, Date Received: {scholar.date_received_2nd_semester}")
    
    total_1st_semester = SemesterDetails.objects.filter(scholar__in=tulong_dunong_program_scholars, semester='1').aggregate(total=Sum('amount'))['total'] or 0
    total_2nd_semester = SemesterDetails.objects.filter(scholar__in=tulong_dunong_program_scholars, semester='2').aggregate(total=Sum('amount'))['total'] or 0
    
    return render(request, 'dayag/ched_tdp.html', {
        'scholars': tulong_dunong_program_scholars,
        'total_1st_semester': total_1st_semester,
        'total_2nd_semester': total_2nd_semester,
    })


from django.shortcuts import render
from django.db.models import Sum
from .models import SemesterDetails

def chedreports_Coscho(request):
    semester = request.GET.get('semester', 'all')
    scholarship_year = request.GET.get('scholarship_year', '')  # Default to scholarship year 2023
    
    # Filter based on semester and scholarship year
    filters = {'scholar__scholar_type': 'Coscho'}
    
    if semester != 'all':
        filters['semester'] = semester
        
    if scholarship_year:
        filters['year'] = scholarship_year
    
    # Get the list of scholars and their amounts
    scholars_list = SemesterDetails.objects.filter(**filters).select_related('scholar__studID')
    
    # Calculate the total billing amount
    total_billing = scholars_list.aggregate(total=Sum('amount'))['total'] or 0
    
    return render(request, 'dayag/ched_coscho.html', {
        'scholars_list': scholars_list, 
        'total_billing': total_billing, 
        'semester': semester, 
        'scholarship_year': scholarship_year
    })

def adminliquidation(request):
    return render(request, 'adminliquidation.html', {})


def adminliquidation_TES(request):
    return render(request, 'dayag/liquidation_TES.html', {})

def adminliquidation_CoScho(request):
    return render(request, 'dayag/liquidation_CoScho.html', {})

def adminliquidation_TDP(request):
    return render(request, 'dayag/liquidation_TDP.html', {})

def transactionreports(request):
    return render(request, 'transactionreports.html', {})

def scholarship_program(request):
    return render(request, 'dayag/scholarship_program.html', {})

def scholarship_billing_report(request):
    return render(request, 'dayag/scholarship_billing_report.html', {})

def Admin_cost_liquidation(request):
    return render(request, 'dayag/Admin_cost_liquidation.html', {})
