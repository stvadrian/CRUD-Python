from django.shortcuts import redirect, render
from django.db import connection
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect


def login_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if 'user' not in request.session:
            return HttpResponseRedirect('/')
        return view_func(request, *args, **kwargs)
    return wrapped_view

def logined_user(view_func):
    def wrapped_view(request, *args, **kwargs):
        if 'user' in request.session:
            return HttpResponseRedirect('/dashboard')
        return view_func(request, *args, **kwargs)
    return wrapped_view

def get_user_by_id(userid):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", [userid])
        first_row = cursor.fetchone()
        columns = [col[0] for col in cursor.description]
 
        if first_row:
            user_data = {column: value.isoformat() if isinstance(value, datetime) else value for column, value in zip(columns, first_row)}
            return user_data
        else:
            return False


# Create your views here.

@logined_user
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE user_username = %s", [username])
            first_row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
 
        if first_row:
            datacol = {col: value for col, value in zip(columns, first_row)}

            password_matched = check_password(password, datacol.get('user_password'))
            if (password_matched):
                user_data = {column: value.isoformat() if isinstance(value, datetime) else value for column, value in zip(columns, first_row)}
                request.session['user'] = user_data
                return redirect('/dashboard')
            else:
                messages.error(request, "Invalid Credentials!")
                return redirect('/')
        else:      
            messages.error(request, "Invalid Credentials!")
            return redirect('/')
        
    return render(request, "authentication/auth/index.html")

@logined_user
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        fullname = request.POST['fullname']
        password = request.POST['password']
        password = make_password(password)

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE user_username = %s", [username])
            row_count = cursor.rowcount

            if row_count > 0:
                messages.error(request, "Username already exists! Try different username.")
                return redirect('/register')
            else:
                created_at = timezone.localtime(timezone.now())
                created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
                created_by = "Python"
                cursor.execute("INSERT INTO users (user_fullname, user_username, user_password, created_at, created_by) VALUES (%s, %s, %s, %s, %s)", [fullname, username, password, created_at, created_by])
                connection.commit()
    
                if cursor.rowcount > 0:
                    messages.success(request, "Registered successfully!")
                    return redirect('/')
                else:
                    messages.error(request, "Registration failed! Please try again.")
                    return redirect('/register')
    
    return render(request, "authentication/auth/register.html")

@login_required
def dashboard_view(request):
    if request.method == 'POST':
        userID = request.POST['user_id']
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE user_id = %s", [userID])
 
            num_deleted_rows = cursor.rowcount
            if num_deleted_rows > 0:
                messages.success(request, "Success Delete Data!")
            else:
                messages.error(request, "Failed to Delete Data!")
        
        return redirect('/dashboard')
        
    request.session['active'] = 'dashboard'
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    users = []
    for row in rows:
        user = dict(zip(columns, row))
        users.append(user)

    data = {
        'users': users,
    }
    return render(request, "authentication/pages/dashboard.html", data)

@login_required
def logout_view(request):
    if 'user' in request.session:
        del request.session['user']
    return HttpResponseRedirect('/')

@login_required
def profile_view(request):
    if request.method == 'POST':
        userID = request.session['user']['user_id']

        if 'fullname' in request.POST:
            fullname = request.POST['fullname']
            with connection.cursor() as cursor:
                cursor.execute("UPDATE users SET user_fullname = %s WHERE user_id = %s", [fullname, userID])
    
                affected_rows = cursor.rowcount
                if affected_rows > 0:
                    messages.success(request, "Success Update Data!")
                else:
                    messages.error(request, "Failed to Update Data!")

        if 'new_password' in request.POST:
            current_password = request.POST['current_password']
            new_password = request.POST['new_password']

            password_matched = check_password(current_password, request.session['user']['user_password'])
            if (password_matched):
                password = make_password(new_password)
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE users SET user_password = %s WHERE user_id = %s", [password, userID])
        
                    affected_rows = cursor.rowcount
                    if affected_rows > 0:
                        messages.success(request, "Success Update Password!")
                    else:
                        messages.error(request, "Failed to Update Password!") 
            else:
                messages.error(request, "Current password does not matched!") 

        request.session['user'] = get_user_by_id(request.session['user']['user_id'])
        return redirect('/profile')
    
    request.session['active'] = 'profile'
    return render(request, "authentication/pages/profile.html")


