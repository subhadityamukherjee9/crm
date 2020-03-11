from django.shortcuts import render, redirect
from .models import Contacts, Company, Institute, CompanyAssociation, InsttitueAssociation, Tags
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import csv,io
import boto3
from pcontact.convert import *
from botocore.exceptions import ClientError
from django.http import JsonResponse
from django.template import loader
from haystack.query import SearchQuerySet
import requests
from datetime import datetime
import logging
logger = logging.getLogger('uploadcsv')

def user_info(request):
    if request.user.is_authenticated():
        searchKey = request.GET.get('search', None)
        if searchKey:
            user_list = SearchQuerySet().filter(content=searchKey).models(Contacts)[:15]
            visible = len(SearchQuerySet().filter(content=searchKey).models(Contacts))
            users=[]
            for user in user_list:
                users.append(user.object)
        else:
            users = Contacts.objects.all()[:15]
            visible = len(Contacts.objects.all())
        return render(request, 'main-page.html', { 'users': users, 'visible':visible, 'searchKey':searchKey})
    else:
        return redirect('log-in')

def lazy_load_posts(request):
    if request.user.is_authenticated():
        page = request.POST.get('page')
        searchKey = request.POST.get('search', None)
        if searchKey:
            ulist = SearchQuerySet().filter(content=searchKey)
            user_list=[]
            for user in ulist:
                user_list.append(user.object)
        else:
            user_list = Contacts.objects.all()

        paginator = Paginator(user_list, 15)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(2)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        posts_html = loader.render_to_string('post.html', {'users': users})
        # package output data and return it as a JSON object
        output_data = {'posts_html': posts_html, 'has_next': users.has_next()}
        return JsonResponse(output_data)
    else:
        return redirect('log-in')

def upload_csv(request):
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            count=0
            upload=0
            file=request.FILES['myfile']
            file_name = file.name
            ext = file_name.split(".")
            if ext[-1] == 'csv':
                dfile=file.read().decode('utf-8')
                io_string = io.StringIO(dfile)
                file_data =csv.reader(io_string,dialect='excel')
                connects = []
                count = 0
                enc='iso-8859-15'
                for row in file_data:
                    try:
                        count +=1
                        if count == 1:
                            continue
                        connect = Connect()
                        connect.init_from_linkedin(row, count)
                        connects.append(connect)
                        s1 = json.dumps(connect.json)
                        data = json.loads(s1)
                        try:
                            ninja = Contacts.objects.create(name=data['name'],
                                                            location = data['location'],
                                                            title = data['title'],
                                                            email=data['email'],
                                                            linkedin_url = data['profile_url'])
                            upload = upload + 1
                        except:
                            logger.error(count)
                            logger.error('Error With Contact Field!')
                            continue

                        if 'positions' in data:
                            try:
                                for i in data['positions']:
                                    w = Company.objects.create(company_name=i['company'], location=i['location'])
                                    q = CompanyAssociation.objects.create(company_id=w.id, title=i['title'], location=i['location'], year=i['dates_employed'])
                                    ninja.company.add(q)
                            except:
                                logger.error(count)
                                logger.error('Error With Company Field!')
                                continue

                        if 'education' in data:
                            try:
                                for i in data['education']:
                                    w = Institute.objects.create(institute_name=i['college_name'])
                                    if not i['field_study']:
                                        q = InsttitueAssociation.objects.create(institute_id=w.id, degree=i['degree'], year=i['dates'])
                                    else:
                                        q = InsttitueAssociation.objects.create(institute_id=w.id, degree=i['degree'] + " - " + i['field_study'], year=i['dates'])
                                    ninja.institute.add(q)
                            except:
                                logger.error(count)
                                logger.error('Error With Education Field!')
                                continue

                        if data['img_url']:
                            if 'img_url' in data:
                                try:
                                    _datetime = datetime.now()
                                    datetime_str = _datetime.strftime("%Y-%m-%d-%H-%M-%S-%f")

                                    # Uses the creds in ~/.aws/credentials
                                    s3 = boto3.resource('s3', aws_access_key_id='AKIAIRMPH5QT6TD2I5LQ',aws_secret_access_key='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')
                                    bucket_name_to_upload_image_to = 'vcfirm-contactimages-ap-south-1'
                                    s3_image_filename = 'media/photos/' + data['name'][0:3] + "-" + data['location'][0:3] + datetime_str + '.jpg'
                                    internet_image_url = data['img_url']
                                    good_to_go = True


                                    # Do this as a quick and easy check to make sure your S3 access is OK
                                    for bucket in s3.buckets.all():
                                        if bucket.name == bucket_name_to_upload_image_to:
                                            good_to_go = True

                                    if not good_to_go:
                                        pass

                                    # Given an Internet-accessible URL, download the image and upload it to S3,
                                    # without needing to persist the image to disk locally
                                    req_for_image = requests.get(internet_image_url, stream=True)
                                    file_object_from_req = req_for_image.raw
                                    req_data = file_object_from_req.read()

                                    # Do the actual upload to s3
                                    s3.Bucket(bucket_name_to_upload_image_to).put_object(Key=s3_image_filename, Body=req_data)
                                    ninja.img_url = 'https://s3.ap-south-1.amazonaws.com/vcfirm-contactimages-ap-south-1/' + s3_image_filename
                                    ninja.save()
                                except:
                                    logger.error(count)
                                    logger.error('Error With Image Field!')
                                    continue
                    except:
                        logger.error(count)
                        logger.error('Error With String Bytes.')
                        continue
                output_data = {'upload': upload}
                return JsonResponse(output_data)
            else:
                output_data = {'upload': 'Invalid File Format, No'}
                return JsonResponse(output_data)
    except:
        output_data = {'upload': upload}
        return JsonResponse(output_data)

def send(emailid, sub, conname, contact_name, log_user, sender):
    SENDER = sender
    RECIPIENT = emailid
    AWS_REGION = "us-east-1"
    SUBJECT = "Request for introduction to " + contact_name
    BODY_TEXT = ("hi")
    BODY_HTML = "<html><head></head><body>Dear " + conname + ",<p>" + sub + "</p>From,<br>" + log_user.username + "<br>"+log_user.email+ "</body></html>"
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


def email(request):
    users= request.POST['user']
    user_name=request.POST['user_name']
    log_user = User.objects.get(username=user_name)
    log_user_email = log_user.email
    role=request.POST['user_role']
    user=users.split(',')
    body=request.POST['body']
    if role=='0': #Request Intro, Mail To vcfirm Connections.
        sender = "tech@vcfirmvc.com"
        for i in user:
            contact=Contacts.objects.get(pk=i)
            contact_name = contact.name
            connect=contact.connection.all()
            for con in connect:
                conname=con.first_name
                emailid=con.email
                send(emailid, body, conname, contact_name,log_user, sender)
    if role=='1': #Send Mail, Mail To Contact.
        """
        if '@vcfirmvc.com' in log_user_email:
            sender = log_user_email
        else:
            sender = "tech@vcfirmvc.com"
        for i in user:
            contact=Contacts.objects.get(pk=i)
            emailid=contact.email
            contact_name=contact.name
            send(emailid, body, conname, contact_name, log_user, sender)
        """
    return redirect('/dashboard/')
