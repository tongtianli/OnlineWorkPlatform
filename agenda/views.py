from django.shortcuts import render
from django.views import View

class AgendaView(View):
    def get(self, request):
        return render(request, 'agenda/agenda.html')
