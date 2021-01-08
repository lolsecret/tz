from datetime import datetime, date

import requests
from .models import Application, Blacklist, Program, StatusTypes


class CheckApplication:
    msg_error_sum = "Заявка не подходит по сумме"
    msg_error_year = "Заемщик не подходит по возрасту"
    status = StatusTypes.approved
    rejection_reason = ''

    apps = Application.objects.all()

    def __init__(self, iin, summa):
        self.summa = summa
        self.iin = iin
        self.programs = Program.objects.all()
        self.year = date.today().year - datetime.strptime(str(iin)[:6], '%y%m%d').date().year
    def check_sum(self):
        self.programs = self.programs.filter(min_sum__lte=self.summa, max_sum__gte=self.summa)
        print(self.programs)
        if not self.programs.exists():
            self.rejection_reason = self.msg_error_sum
            self.status = StatusTypes.denied

        return [self.status, self.rejection_reason]

    def check_year(self):
        self.programs = self.programs.filter(min_year__lte=self.year, max_year__gte=self.year)
        if not self.programs.exists():
            self.status = StatusTypes.denied
            self.rejection_reason = self.msg_error_year

        return [self.status, self.rejection_reason]


class CheckIP:
    msg_error = "иин является ИП"
    status = StatusTypes.approved
    rejection_reason = ''

    def __init__(self, iin):
        self.iin = iin

    def ip_or_not(self):
        url = requests.get('https://stat.gov.kz/api/juridical/gov/?bin={0}&lang=ru'.format(self.iin))
        if url.json().get('success'):
            self.status = StatusTypes.denied
            self.rejection_reason = self.msg_error

        return [self.status, self.rejection_reason]


class CheckBlackList:
    msg_error = "Заемщик в черном списке"
    status = StatusTypes.approved
    rejection_reason = ''

    def __init__(self, iin):
        self.iin = iin

    def blacklist(self):
        if Blacklist.objects.filter(iin=self.iin.iin).exists():
            self.status = StatusTypes.denied
            self.rejection_reason = self.msg_error
        return [self.status, self.rejection_reason]


class IinGeneration:
    status = StatusTypes.approved

    def __init__(self, iin):
        self.iin = iin

    def date_of_birth(self):
        try:
            if datetime.strptime(str(self.iin)[:6], '%y%m%d').date():
                return [self.status, datetime.strptime(str(self.iin)[:6], '%y%m%d').date()]
        except:
            self.status = StatusTypes.denied
        return [self.status, 'Неверный ИИН']

    def century_and_gender(self):
        if int(self.iin[6]) > 7:
            self.status = StatusTypes.denied
        return StatusTypes.approved

    def twelve_num(self):
        try:
            iin = str(self.iin)
            tw_num = (1*iin[0] + 2*iin[1] + 3*iin[2] + 4*iin[3] + 5*iin[4] + 6*iin[5] +
                      7*iin[6] + 8*iin[7] + 9*iin[8] + 10*iin[9] + 11*iin[10])
            tw_num = int(tw_num) % 11

            if not str(self.iin)[11] == str(tw_num)[0]:
                self.status = StatusTypes.denied
        except:
            self.status = StatusTypes.denied
        return self.status


def check_iin_generation(iin):
    status = StatusTypes.approved
    msg_error = 'Неверный иин'
    date_of_birth = IinGeneration(iin).date_of_birth()
    century_and_gender = IinGeneration(iin).century_and_gender()
    twelve_num = IinGeneration(iin).twelve_num()
    if date_of_birth[0] == status or century_and_gender == status or twelve_num == status:
        return status
    return msg_error


def checkapp(borrower, summa):
    status = StatusTypes.denied
    app = CheckApplication(borrower.iin, summa)
    rejection_reason = ''

    check_sum = app.check_sum()
    year = app.check_year()
    if app.programs:
        program = app.programs.first()
    else:
        program = None

    ip = CheckIP(borrower).ip_or_not()
    blacklist = CheckBlackList(borrower).blacklist()
    if check_sum[0] != status and year[0] != status and ip[0] != status and blacklist[0] != status:
        status = StatusTypes.approved
    if check_sum[1]: rejection_reason = check_sum[1]
    elif year[1]: rejection_reason = year[1]
    elif ip[1]: rejection_reason = ip[1]
    elif blacklist[1]: rejection_reason = blacklist[1]

    Application.objects.create(summa=summa, status=status, program=program, borrower=borrower, rejection_reason=rejection_reason)

    return [status, rejection_reason]