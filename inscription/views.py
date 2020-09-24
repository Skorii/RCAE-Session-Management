from django.shortcuts import render, HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.html import format_html
from .models import *
from datetime import datetime, timedelta

message = ''


def selection_sport(request):
    list_sessions = Session.objects.filter(date_time__gte=datetime.now(), date_time__lt=datetime.now() + timedelta(days=7))
    list_session_id, list_sections = [], []
    for session in list_sessions:
        if session.section_id not in list_session_id:
            temp = Section.objects.get(code=session.section_id)
            if temp.active:
                list_session_id.append(session.section_id)
                list_sections.append(temp)
    if list_sections:
        return render(request, 'inscription/sections.html', {
            'sections': list_sections,
        })
    else:
        return render(request, 'inscription/result.html', {
            'message': format_html(f"Désolé, les inscriptions ne sont disponibles pour aucunes sections.<br />Réessayez plus tard.")
        })


def inscription(request):
    try:
        sessions = Session.objects.filter(section=request.POST['section'], date_time__gte=datetime.now(), date_time__lt=datetime.now() + timedelta(days=7))
        if sessions:
            for session in sessions:
                session.max_members -= Member.objects.filter(session=session.id).count()
            return render(request, 'inscription/form.html', {
                'current_section': Section.objects.filter(code=request.POST['section'])[0],
                'sessions': sessions,
            })
        else:
            return render(request, 'inscription/result.html', {
                'message': f"Désolé, les inscriptions ne sont pas encore disponible pour la section : {Section.objects.filter(code=request.POST['section'])[0].name}."
            })
    except MultiValueDictKeyError:
        raise Http404


def validation(request):
    global message
    try:

        if slots_available(request.POST['session']):
            # Enough place in the session
            try:
                sub_num = request.POST['subscription_number']
            except MultiValueDictKeyError:
                sub_num = ''
            new_member = Member(first_name=request.POST['first_name'],
                                last_name=request.POST['last_name'],
                                rcae_number=request.POST['rcae_code'] + request.POST['rcae_number'],
                                e_mail=request.POST['email'],
                                subscription_number=sub_num,
                                session=Session.objects.get(id=request.POST['session'])
                                )
            if member_already_registered(request, new_member):
                message = "Vous êtes déja inscrit pour cette séance!"
            else:
                new_member.save()
                sess = Session.objects.filter(id=request.POST['session'])[0]
                message = f"Votre inscription a été validée pour le cours : {sess.section} du {sess.date_time.date()} à {sess.date_time.time()}"
        else:
            message = "Désolé, ce cours est complet..."
        return HttpResponseRedirect(reverse('inscription:result'))
    except MultiValueDictKeyError:
        raise Http404


def registration_result(request):
    return render(request, 'inscription/result.html', {'message': message})


def slots_available(session_id):
    return Member.objects.filter(session=session_id).count() < Session.objects.get(id=session_id).max_members


def member_already_registered(request, new_member):
    members_list = Member.objects.filter(session=request.POST['session'])
    for member in members_list:
        if member.last_name.lower() == new_member.last_name.lower() and member.first_name.lower() == new_member.first_name.lower() or member.rcae_number.lower() == new_member.rcae_number.lower() or member.subscription_number == new_member.subscription_number:
            return True
    return False
