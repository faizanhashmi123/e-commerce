from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from twilio.rest import Client
import threading


def get_domain_protocol(request):
    current_site = get_current_site(request)
    domain = current_site.domain
    return domain, 'http'


def send_email(request, to, template, context={}, subject='Welcome'):
    context['domain'], context['protocol'] = get_domain_protocol(request)
    subject, from_email, to = subject, None, to

    html_content = render_to_string(template, context)  # render with dynamic value
    text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_email_background(request, to, template, context={}, subject='Welcome'):
    context['domain'], context['protocol'] = get_domain_protocol(request)
    EmailThread(to, template, context, subject).start()


class EmailThread(threading.Thread):
    def __init__(self, to, template, context, subject):
        self.to = to
        self.template = template
        self.context = context
        self.subject = subject
        threading.Thread.__init__(self)

    def run(self):
        from_email = None

        html_content = render_to_string(self.template, self.context)  # render with dynamic value
        text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(self.subject, text_content, from_email, [self.to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
