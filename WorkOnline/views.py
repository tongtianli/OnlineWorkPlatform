from datetime import datetime, timedelta

from django.shortcuts import render
from django.views import View

from agenda.models import Agenda, Participant


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            # 下面一句不加tzinfo会导致出现两种datetime，不能比较
            day1 = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
            day2 = day1 + timedelta(days=1)
            day3 = day1 + timedelta(days=2)
            day4 = day1 + timedelta(days=3)
            personal_agenda = Agenda.objects.filter(start_time__gte=day1, start_time__lt=day4, userID=request.user.id,
                                                    groupID=-1)
            group_agenda = [each.agenda for each in
                            Participant.objects.filter(user_id=request.user.id, agenda__start_time__gte=day1,
                                                       agenda__start_time__lt=day4)]

            day1_agenda = list(personal_agenda.filter(start_time__lt=day2))
            day2_agenda = list(personal_agenda.filter(start_time__gte=day2, start_time__lt=day3))
            day3_agenda = list(personal_agenda.filter(start_time__gte=day3, start_time__lt=day4))
            for each in group_agenda:
                time = each.start_time.replace(tzinfo=None)
                if day1 <= time < day2:
                    day1_agenda.append(each)
                elif day2 <= time < day3:
                    day2_agenda.append(each)
                elif day3 <= time < day4:
                    day3_agenda.append(each)
        return render(request, 'index.html', locals())
