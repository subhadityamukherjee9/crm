from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import login as contrib_login
from django.contrib.auth import authenticate
from django.conf import settings
from mezzanine.blog.views import blog_post_list
from mezzanine.blog.models import BlogPost, BlogCategory
import boto3
from django.contrib.auth.models import User


from portfolio_company.models import PortfolioCompany
from team.models import CompanyTeam

def login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return contrib_login(request, **kwargs)

def index(request):
    posts = BlogPost.objects.all()
    portfolio=PortfolioCompany.objects.filter(show_on_profile=True)
    return render(request, 'index.html',{'posts': posts, 'portfolio':portfolio})


def portfolio_companies_view(request):
    portfolio=PortfolioCompany.objects.all()
    return render(request, 'portfolio.html',{ 'portfolio':portfolio})

def teams(request):
    team=CompanyTeam.objects.all()
    return render(request, 'team.html',{ 'team':team})

def portfolio_detail(request, portfolio_id):
    portfolio_details = PortfolioCompany.objects.get(id=portfolio_id)
    return render(request, 'portfolio_details.html', {'portfolio': portfolio_details})






def emailsend(email,username):
    SENDER = "tech@vcfirmvc.com"
    RECIPIENT = "tech@vcfirmvc.com"
    AWS_REGION = "us-east-1"
    SUBJECT = "User Forgot Password"
    BODY_TEXT = ("hi")
    BODY_HTML = "<html>User Forgot Password, Contact, <br/><br/>Username: " + username + "<br/>Email: " + email + "</html>"
    CHARSET = "UTF-8"
    client = boto3.client('ses',aws_access_key_id='AKIAIRMPH5QT6TD2I5LQ',aws_secret_access_key='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',region_name=AWS_REGION)
    try:
        response = client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,)
    except ClientError as e:
        print(e.response['Error']['Message'])
    return redirect('/dashboard/')

def forgot_email(request):
    try:
        email = request.POST['email']
        user = User.objects.get(email=email)
        username = user.username
        emailsend(email, username)
        return redirect('/login/')
    except:
        return redirect('forgotpassword')

from django.shortcuts import render_to_response
def forgotpassword (request):
    if request.user.is_authenticated():
        return redirect('dashboard')
    else:
        return render(request,'forgot_password.html')
