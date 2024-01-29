from django.shortcuts import redirect,render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from .models import UserData
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.urls import reverse


# Create your views here.




def register(request):
    if request.method =="POST":
        Name=request.POST.get('name')
        PhoneNumber=request.POST.get('phone')
        HouseNumber=request.POST.get('HouseNo')
        Street=request.POST.get('Street')
        City=request.POST.get('city')
        District=request.POST.get('district')
        Pincode=request.POST.get('Pincode')
        State=request.POST.get('state')
        Country=request.POST.get('Country')
        
        Email=request.POST.get('email')
        Password=request.POST.get('password')
        Password1=request.POST.get('password1')

        if Password != Password1:
            messages.error(request, "Passwords did not match! Please enter passwordS in both the fields correctly!")
            return redirect('register')
        hashed_password = make_password(Password)

        user=User.objects.create(
            username=Email,
            email=Email,
            password=hashed_password,
        )
        UserData.objects.create(
        user=user,
        full_name=Name,
        phone_number=PhoneNumber,
        house_number=HouseNumber,
        street=Street,
        state=State,
        city=City,
        district=District,
        pincode=Pincode,
        country=Country
        )
        
        messages.success(request,"Your Account Has Been Successfully Created!")

        return redirect('home')


    return render(request,"register.html")




def home(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('invoice')
        else:
            messages.error(request,'Invalid username or password!')
            return render(request,"index.html")
        
    else:
        return render(request,"index.html")





@login_required
def invoice(request):
    context = None

    if request.user.is_authenticated:
        email = request.user.email  
        data = UserData.objects.get(user=request.user)  
        context = {'email': email, 'user_data': data}

        if request.method == "POST":
            Name = request.POST.get('toName')
            PhoneNumber = request.POST.get('toPhone')
            HouseNumber = request.POST.get('toHouseNo')
            Street = request.POST.get('toStreet')
            City = request.POST.get('toCity')
            District = request.POST.get('toDistrict')
            Pincode = request.POST.get('toPincode')
            State = request.POST.get('toState')
            Country = request.POST.get('toCountry')
            barcode=request.POST.get('barcodeNo')

            printContext = {
                'Name': Name,
                'PhoneNumber': PhoneNumber,
                'HouseNumber': HouseNumber,
                'Street': Street,
                'City': City,
                'District': District,
                'Pincode': Pincode,
                'State': State,
                'Country': Country,
                'barcode':barcode,
            }
            printinv_url = reverse('printinv')
            redirect_url = f"{printinv_url}?{'&'.join([f'{key}={value}' for key, value in printContext.items()])}"

    
            return redirect(redirect_url)

    return render(request, "invoice.html", context)


@login_required
def printinv(request):
    data = UserData.objects.get(user=request.user)

    Name = request.GET.get('Name', '')
    PhoneNumber = request.GET.get('PhoneNumber', '')
    HouseNumber = request.GET.get('HouseNumber', '')
    Street = request.GET.get('Street', '')
    City = request.GET.get('City', '')
    District = request.GET.get('District', '')
    Pincode = request.GET.get('Pincode', '')
    State = request.GET.get('State', '')
    Country = request.GET.get('Country', '')
    barcode = request.GET.get('barcode', '')

    printContext = {
        'Name': Name,
        'PhoneNumber': PhoneNumber,
        'HouseNumber': HouseNumber,
        'Street': Street,
        'City': City,
        'District': District,
        'Pincode': Pincode,
        'State': State,
        'Country': Country,
        'barcode':barcode,
    }
    context = {'to_data': printContext, 'user_data': data}
    print(context)
    return render(request, "print.html", context)



@login_required
def myprofile(request):
    context=None
    if request.user.is_authenticated :
        email = request.user.email 
        user_data = UserData.objects.get(user=request.user)
        context={'email':email,'user_data':user_data} 

    if request.user.is_authenticated and request.method=="POST":
        user_data = UserData.objects.get(user=request.user)
        user_data.full_name=request.POST.get('Name')
        user_data.phone_number=request.POST.get('phone')
        user_data.house_number=request.POST.get('HouseNo')
        user_data.street=request.POST.get('Street')
        user_data.city=request.POST.get('city')
        user_data.district=request.POST.get('district')
        user_data.pincode=request.POST.get('Pincode')
        user_data.state=request.POST.get('state')
        user_data.country=request.POST.get('Country')
        user_data.save()    
        
        user_data = UserData.objects.get(user=request.user)
        context = {'email': email, 'user_data': user_data}
        
    return render(request,"profile.html",context)



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            # Generate a token for password reset
            token = default_token_generator.make_token(user)
            
            # Construct password reset URL
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                f'/reset-password/{uid}/{token}/'
            )
            
            # Send email with the reset link
            send_mail(
                'Password Reset',
                f'Click the link to reset your password: {reset_url}',
                'vardhanrawat1@gmail.com',
                [email],
                fail_silently=False,
            )
            messages.success(request,"Password Reset-Link has been sent to your Email Account!")
        else:
            messages.error(request,"This Email-id is not registered! Please enter the correct Email id!")    
    return render(request, 'forgot-password.html')



def reset_password(request, uidb64, token):
    # Decode the uid and get the user
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    
    if default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            new_password1 = request.POST.get('new_password1')

            if new_password != new_password1:
                messages.error(request, "Passwords did not match! Please enter passwords in both the fields correctly!")
            else:
                user.set_password(new_password)
                user.save()
                messages.success(request,"Your Password has been changed successfully!")
                return redirect('home')
    return render(request, 'reset_password.html')


