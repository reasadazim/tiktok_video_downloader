from django.shortcuts import render
from .forms import FormWithCaptcha
import json
import shutil
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import FormWithCaptcha
import os
import secrets
import string
import requests
import re
import uuid


# Homepage
def home(request):

    # Define alert messages
    success = ''
    warning = ''
    error = ''

    # Define download url variables
    download_url_nowatermerk = ''
    download_url_watermerk = ''
    download_url_cover = ''

    # Generate Random charecter
    random_char = (''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(24)))

    # Generate unique ID
    uid = uuid.uuid4()

    # Redirect to homepage if request type is GET
    if request.method == "GET":

        form = FormWithCaptcha()

        return render(request, 'index.html', context={'form': form})

    else:

        form = FormWithCaptcha(request.POST)

        if form.is_valid():

            try:

                # Get post url
                video_url = request.POST.get('url')

                # Check the url is instagram url not other url (e.g. youtube, ticktok)
                tiktok_url_is_vaild = re.search("tiktok.com", video_url)

                if tiktok_url_is_vaild:

                    # Download video code

                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

                    response = requests.get(video_url, headers=headers)

                    # user_data = re.findall(r'(@[a-zA-z0-9]*)\/.*\/([\d]*)?', response.url)
                    user_data = re.findall(r'(@[a-zA-z0-9-.]*)\/.*\/([\d]*)?', response.url)

                    username = user_data[0][0][1:]
                    videoid = user_data[0][1]

                    api_url = f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={videoid}'

                    api_response = requests.get(api_url, headers=headers).json()

                    if str(username) == str(api_response['aweme_list'][0]['author']['unique_id']):

                        download_url_nowatermerk = api_response['aweme_list'][0]['video']['play_addr']['url_list'][0]
                        download_url_watermerk = api_response['aweme_list'][0]['video']['download_addr']['url_list'][0]
                        download_url_cover = api_response['aweme_list'][0]['video']['dynamic_cover']['url_list'][0]

                        download_directory = 'public/static/downloads/'
                        filename_watermark = f"{download_directory}videos/{random_char}_watermark.mp4"
                        filename_nowatermark = f"{download_directory}videos/{random_char}_nowatermark.mp4"

                        with open(filename_watermark, 'wb') as out_file:
                            content = requests.get(download_url_watermerk, stream=True).content
                            out_file.write(content)
                        with open(filename_nowatermark, 'wb') as out_file:
                            content = requests.get(download_url_nowatermerk, stream=True).content
                            out_file.write(content)

                        # Store record into database so that we can flush the stored content after a certain delay
                        Files.objects.create(
                            uid=uid,
                            path_watermark=f"media/downloads/videos/{random_char}_watermark.mp4",
                            path_nowatermark=f"media/downloads/videos/{random_char}_nowatermark.mp4",
                            type='Video',
                            deleted=False
                        )

                        files = Files.objects.filter(uid=uid)

                        success = "Content downloaded successfully."

                        context = {
                            'files': files,
                            'download_url_nowatermerk': download_url_nowatermerk,
                            'download_url_watermerk': download_url_watermerk,
                            'download_url_cover': download_url_cover,
                            'form': form,
                            'success': success,
                            'error': error,
                            'warning': warning,
                        }

                        return render(request, 'index.html', context)
                    else:
                        # Call Rapid API since video is a story or not downloadable from TikTok APP
                        # Rapid API is expensive so we use it only for the videos which are private
                        # Get post url
                        video_url = request.POST.get('url')

                        url = "RAPID_API_URL"

                        querystring = {"url": video_url, "hd": "1"}

                        headers = {
                            "X-RapidAPI-Key": "YOUR_RAPID_API_KEY",
                            "X-RapidAPI-Host": "YOUR_RAPID_API_HOST"
                        }

                        response = requests.get(url, headers=headers, params=querystring)

                        data = response.json()

                        # print(data)

                        download_url_watermerk = (data['data']['wmplay'])
                        download_url_nowatermerk = (data['data']['hdplay'])
                        download_url_cover = (data['data']['cover'])

                        # END - Download video code

                        download_directory = 'public/static/downloads/'
                        filename_watermark = f"{download_directory}videos/{random_char}_watermark.mp4"
                        filename_nowatermark = f"{download_directory}videos/{random_char}_nowatermark.mp4"

                        with open(filename_watermark, 'wb') as out_file:
                            content = requests.get(download_url_watermerk, stream=True).content
                            out_file.write(content)
                        with open(filename_nowatermark, 'wb') as out_file:
                            content = requests.get(download_url_nowatermerk, stream=True).content
                            out_file.write(content)

                        # Store record into database so that we can flush the stored content after a certain delay
                        Files.objects.create(
                            uid=uid,
                            path_watermark=f"media/downloads/videos/{random_char}_watermark.mp4",
                            path_nowatermark=f"media/downloads/videos/{random_char}_nowatermark.mp4",
                            type='Video',
                            deleted=False
                        )

                        files = Files.objects.filter(uid=uid)

                        success = "Content downloaded successfully."

                        context = {
                            'files': files,
                            'download_url_nowatermerk': download_url_nowatermerk,
                            'download_url_watermerk': download_url_watermerk,
                            'download_url_cover': download_url_cover,
                            'form': form,
                            'success': success,
                            'error': error,
                            'warning': warning,
                        }

                        return render(request, 'index.html', context)
                else:
                    error = 'Not a tiktok url'
                    context = {
                        'download_url_nowatermerk': download_url_nowatermerk,
                        'download_url_watermerk': download_url_watermerk,
                        'download_url_cover': download_url_cover,
                        'form': form,
                        'success': success,
                        'error': error,
                        'warning': warning,
                    }

                return render(request, 'index.html', context)

            except Exception as e:
                error = f"Error: {e}"
                context = {
                    'download_url_nowatermerk': download_url_nowatermerk,
                    'download_url_watermerk': download_url_watermerk,
                    'download_url_cover': download_url_cover,
                    'form': form,
                    'success': success,
                    'error': error,
                    'warning': warning,
                }
                return render(request, 'index.html', context)
        else:

            form = FormWithCaptcha()
            error = "Recaptcha validation failed."
            context = {'error': error, 'form': form}
            return render(request, 'index.html', context)


# Terms page
def terms(request):
    return render(request, 'terms.html')


# Privacy page
def privacy(request):
    return render(request, 'privacy.html')


# Contact page
def contact(request):
    form = FormWithCaptcha()
    if request.method == "GET":
        return render(request, 'contact.html', context={'form': form})
    else:
        success = ''
        error = ''
        form = FormWithCaptcha()
        try:
            form = FormWithCaptcha(request.POST)
            if form.is_valid():
                name = request.POST.get('name')
                subject = request.POST.get('subject')
                message = request.POST.get('message')
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST.get('email'), ]

                context = {
                    'name': name,
                    'subject': subject,
                    'message': message,
                }

                message = get_template("email.html").render(context)
                mail = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email=email_from,
                    to=['riasadazim@gmail.com'],
                    reply_to=recipient_list,
                )
                mail.content_subtype = "html"
                mail.send()
                success = "Email sent successfully. We will get in touch with you soon."
                context = {'success': success, 'form': form}
            else:
                form = FormWithCaptcha()
                error = "Recaptcha validation failed."
                context = {'error': error, 'form': form}
                return render(request, 'contact.html', context)
        except Exception as e:
            error = f"Error: {e}"
            context = {'error': error, 'form': form}

        return render(request, 'contact.html', context)


# Sitemap
def sitemap(request):
    return render(request, 'sitemap.html', content_type="text/xml")
