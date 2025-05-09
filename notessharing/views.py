"""Import all modules and packages here"""
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from nssapp.models import CustomUser,UserReg,Notes
User = get_user_model()

def index(request): # pylint: disable=missing-function-docstring
    return render(request,'index.html')

@login_required(login_url = '/')
def base(request): # pylint: disable=missing-function-docstring
    return render(request, 'base.html')

def dashboard(request): # pylint: disable=missing-function-docstring
    user_admin = request.user
    try:
        user_reg = UserReg.objects.get(admin=user_admin) # pylint: disable=no-member
    except UserReg.DoesNotExist: # pylint: disable=no-member
        messages.error(request, "User registration details not found.")
        return render(request, 'dashboard.html')

    uploadedsub_count = Notes.objects.filter(nsuser=user_reg).count() # pylint: disable=no-member
    user_notes = Notes.objects.filter(nsuser=user_reg) # pylint: disable=no-member

    # Initialize file count
    total_files = 0

    # Count files for each note
    for note in user_notes:
        if note.file1:
            total_files += 1
        if note.file2:
            total_files += 1
        if note.file3:
            total_files += 1
        if note.file4:
            total_files += 1

    context = {
        'uploadedsub_count': uploadedsub_count,
        'total_files': total_files,
    }

    return render(request, 'dashboard.html', context)


def login_view(request): # pylint: disable=missing-function-docstring
    return render(request,'login.html')


def do_logout(request): # pylint: disable=missing-function-docstring
    logout(request)
    request.session.flush()  # Clear the session including CSRF token
    return redirect('login')

def do_login(request): # pylint: disable=missing-function-docstring
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('dashboard')
            return redirect('dashboard')
        messages.error(request, 'Email or Password is not valid')
        return redirect('login')  # Redirect back to the login page with an error message
        # If the request method is not POST, redirect to the login page with an error message
    messages.error(request, 'Invalid request method')
    return redirect('login')


def user_signup(request): # pylint: disable=missing-function-docstring
    if request.method == "POST":
        pic = request.FILES.get('pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobno = request.POST.get('mobno')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email already exist')
            return redirect('usersignup')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,'Username already exist')
            return redirect('usersignup')
        user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            user_type=2,
            profile_pic = pic,
        )
        user.set_password(password)
        user.save()
        nsuser = UserReg(
            admin = user,
            mobilenumber = mobno,
        )
        nsuser.save()
        messages.success(request,'Signup Successfully')
    return render(request,'signup.html')


@login_required(login_url='/')
def profile(request): # pylint: disable=missing-function-docstring
    if request.method == "POST":
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            #userreg = UserReg.objects.get(admin_id=request.user.id)
            customuser.first_name = request.POST.get('first_name', customuser.first_name)
            customuser.last_name = request.POST.get('last_name', customuser.last_name)
            if 'profile_pic' in request.FILES:
                customuser.profile_pic = request.FILES['profile_pic']
            customuser.save()
            messages.success(request, "Your profile has been updated successfully")
            return redirect('profile')
        except ObjectDoesNotExist:
            messages.error(request, "User not found.")
        except ValueError:
            messages.error(request, "Invalid data provided.")
        except IOError:
            messages.error(request, "Error accessing file.")
        return redirect('profile')
    try:
        user = CustomUser.objects.get(id=request.user.id)
        nsuser = UserReg.objects.get(admin_id=request.user.id) # pylint: disable=no-member
    except CustomUser.DoesNotExist: # pylint: disable=no-member
        user = None
    except UserReg.DoesNotExist: # pylint: disable=no-member
        nsuser = None
    context = {
        "user": user,
        "nsuser": nsuser,
    }
    return render(request, 'profile.html', context)

def change_password(request): # pylint: disable=missing-function-docstring
    context = {}
    ch = User.objects.filter(id = request.user.id)
    if len(ch)>0:
        data = User.objects.get(id = request.user.id)
        context["data"]:data
    if request.method == "POST":
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id = request.user.id)
        un = user.username
        check = user.check_password(current)
        if check is True:
            user.set_password(new_pas)
            user.save()
            messages.success(request,'Password Change  Succeesfully!!!')
            user = User.objects.get(username=un)
            login(request,user)
        messages.success(request,'Current Password wrong!!!')
        return redirect("change_password")
    return render(request,'change-password.html')


def add_notes(request): # pylint: disable=missing-function-docstring
    if request.method == "POST":
        title = request.POST.get('notestitle')
        subject = request.POST.get('subject')
        description = request.POST.get('notesdesc')
        file1 = request.FILES.get('file1')
        file2 = request.FILES.get('file2')
        file3 = request.FILES.get('file3')
        file4 = request.FILES.get('file4')

        userreg = UserReg.objects.get(admin_id=request.user.id) # pylint: disable=no-member

        notes = Notes(
            notestitle=title,
            subject = subject,
            notesdesc = description,
            file1 = file1,
            file2 = file2,
            file3 = file3,
            file4 = file4,
            nsuser = userreg,
        )
        notes.save()
        messages.success(request, 'Notes Added Successfully')
        return redirect("add_notes")
    return render(request, 'add-notes.html')

login_required(login_url='/')
def manage_notes(request): # pylint: disable=missing-function-docstring
    userreg = UserReg.objects.get(admin_id=request.user.id) # pylint: disable=no-member
    data_list = Notes.objects.filter(nsuser = userreg) # pylint: disable=no-member
    paginator = Paginator(data_list, 10)  # Show 10 data per page

    page_number = request.GET.get('page')
    try:
        data_list = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        data_list = paginator.page(paginator.num_pages)

    context = {'data_list': data_list,
   }
    return render(request, 'manage-notes.html', context)

login_required(login_url='/')
def delete_notes(request,note_id): # pylint: disable=missing-function-docstring
    del_data = Notes.objects.get(id = note_id) # pylint: disable=no-member
    del_data.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    return redirect('manage_notes')


login_required(login_url='/')
def view_notes(request,note_id): # pylint: disable=missing-function-docstring
    data_notes = Notes.objects.get(id = note_id) # pylint: disable=no-member
    context = {
        "data_notes":data_notes,
    }
    return render(request,'update_notes.html',context)

@login_required(login_url='/')
def edit_notes(request): # pylint: disable=missing-function-docstring
    if request.method == "POST":
        data_id = request.POST.get('notes_id')
        try:
            data_edit = Notes.objects.get(id=data_id) # pylint: disable=no-member
        except Notes.DoesNotExist: # pylint: disable=no-member
            messages.error(request, "Data does not exist")
            return redirect('manage_data')

        # Create a dictionary with updated data
        updated_data = {
            'notestitle': request.POST.get('notestitle'),
            'subject': request.POST.get('subject'),
            'notesdesc': request.POST.get('notesdesc'),
        }

        # Update the data_edit object with the updated data
        for field, value in updated_data.items():
            if value:
                setattr(data_edit, field, value)

        # Handle file uploads separately
        for i in range(1, 5):
            file_field = f'file{i}'
            if file_field in request.FILES:
                setattr(data_edit, file_field, request.FILES[file_field])

        data_edit.save()
        messages.success(request, "Data has been updated successfully")
        return redirect('manage_notes')

    return render(request, 'manage-notes.html')


def search_notes(request): # pylint: disable=missing-function-docstring
    if request.method == "GET":
        # Clear existing messages
        storage = messages.get_messages(request)
        list(storage)  # Access the messages to clear them
        userreg = UserReg.objects.get(admin_id=request.user.id) # pylint: disable=no-member
        query = request.GET.get('query', '')

        if query:
            searchdata = Notes.objects.filter( # pylint: disable=no-member
                Q(notestitle__icontains=query) |
                Q(subject__icontains=query),
                nsuser=userreg
            )

            if searchdata.exists():
                messages.info(request, f"Search results for '{query}'")
            else:
                messages.info(request, f"No results found for '{query}'")

            return render(request, 'search.html', {'searchdata': searchdata, 'query': query})
    return render(request, 'search.html', {'searchdata': [], 'query': ''})

login_required(login_url='/')
def notes_details(request): # pylint: disable=missing-function-docstring
    data_list = Notes.objects.all() # pylint: disable=no-member
    paginator = Paginator(data_list, 10)
    page_number = request.GET.get('page')
    try:
        data_list = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        data_list = paginator.page(paginator.num_pages)
    context = {
        "data_list":data_list,
    }
    return render(request,'notes.html',context)
