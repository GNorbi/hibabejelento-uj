from django.shortcuts import render
from .models import Hiba, Visszajelzes, AllapotValtozas
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """
    View function for home page of site.
    """
    # Generate count of some of the main objects
    hibak_szama_f=Hiba.objects.count()
    hibak_szama_g=Hiba.objects.filter(statusz='g').count() + Hiba.objects.filter(statusz='h').count() + Hiba.objects.filter(statusz='i').count()
    hibak_szama_j=Hiba.objects.filter(statusz='j').count()

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'hibak_szama_f':hibak_szama_f,'hibak_szama_g':hibak_szama_g,'hibak_szama_j':hibak_szama_j},
    )

@login_required
def get_fogadott(request):
    fogadott_hibak = Hiba.objects.filter(statusz='f')
    fogadott_hibak_szama = Hiba.objects.filter(statusz='f').count()

    visszajelzesek = Visszajelzes.objects.all()
    allapotvaltozasok = AllapotValtozas.objects.all()

    return render(
        request,
        'hibak/fogadott_hibak.html',
        context={'fogadott_hibak':fogadott_hibak, 'fogadott_hibak_szama':fogadott_hibak_szama, 'visszajelzesek':visszajelzesek, 'allapotvaltozasok':allapotvaltozasok},
    )

@login_required
def get_folyamatba_helyezve(request):
    folyamatba_helyezett_hibak_g = Hiba.objects.filter(statusz='g')
    folyamatba_helyezett_hibak_h = Hiba.objects.filter(statusz='h')
    folyamatba_helyezett_hibak_i = Hiba.objects.filter(statusz='i')
    folyamatba_helyezett_hibak_szama = Hiba.objects.filter(statusz='g').count() + Hiba.objects.filter(statusz='h').count() + Hiba.objects.filter(statusz='i').count()
    folyamatba_helyezett_hibak = folyamatba_helyezett_hibak_g | folyamatba_helyezett_hibak_h | folyamatba_helyezett_hibak_i

    visszajelzesek = Visszajelzes.objects.all()
    allapotvaltozasok = AllapotValtozas.objects.all()

    return render(
        request,
        'hibak/folyamatba_helyezett_hibak.html',
        context={'folyamatba_helyezett_hibak':folyamatba_helyezett_hibak, 'folyamatba_helyezett_hibak_szama':folyamatba_helyezett_hibak_szama, 'visszajelzesek':visszajelzesek, 'allapotvaltozasok':allapotvaltozasok},
    )

@login_required
def get_elkeszult(request):
    elkeszult_hibak = Hiba.objects.filter(statusz='j')
    elkeszult_hibak_szama = Hiba.objects.filter(statusz='j').count()

    visszajelzesek = Visszajelzes.objects.all()
    allapotvaltozasok = AllapotValtozas.objects.all()

    return render(
        request,
        'hibak/elkeszult_hibak.html',
        context={'elkeszult_hibak':elkeszult_hibak, 'elkeszult_hibak_szama':elkeszult_hibak_szama, 'visszajelzesek':visszajelzesek, 'allapotvaltozasok':allapotvaltozasok},
    )


from django.views import generic

class HibaReszleteiView(generic.DetailView):
    model = Hiba


class HibaListaView(generic.ListView):
    model = Hiba

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            list = Hiba.objects.filter(id=query)
            if list.count()==1:
                return list
            else:
                return Hiba.objects.all()
        else:
            return Hiba.objects.all()

    def get_context_data(self, **kwargs):
        context = super(HibaListaView, self).get_context_data(**kwargs)
        context['visszajelzesek'] = Visszajelzes.objects.all()
        context['allapotvaltozasok'] = AllapotValtozas.objects.all()
        return context


	

from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime

from .forms import HibaBejelentoForm
from django.core.mail import send_mail

@login_required
def hiba_bejelentes(request):
    """
    View function for renewing a specific BookInstance by librarian
    """
    #hiba=get_object_or_404(Hiba)
    

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = HibaBejelentoForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            			    
            hiba = form.save(commit=True)
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            hiba.nev = form.cleaned_data['nev']
            hiba.cim = form.cleaned_data['cim']
            hiba.kapcsolattarto_email = form.cleaned_data['kapcsolattarto_email']
            hiba.leiras = form.cleaned_data['leiras']
            form.save()

			#elso ugyfelnek masodik szolgaltatonak
            elso = " sorszámu hiba"
            masodik = "Hibabejelentését fogadtuk,"
            harmadik = " sorszámon rögzítettük, nyomon követheti www.kincstarhibabejelento.hu webcímen üzemelő hibabejelentő felületen, a későbbiekben a változásokról e-mail értesítést fog kapni. Ez egy automatikus üzenet, kérjük erre ne válaszoljon.  Tisztelettel: Ép-Üz-Bau Kft"
            negyedik = " sorszámu hiba"
            otodik = " sorszámon hibabejelentés érkezett, megtekinthető a www.kincstarhibabejelento.hu/admin webcímen üzemelő hibabejelentő felületen"
            #email1_fejlec = "sorszámú hiba bejelentését fogadtuk"
            #email1_from = str(hiba.id).decode('utf-8') + " " + email1_fejlec.decode('utf-8') + ' <tesztemailepuzbau@gmail.com>'

            #email2_fejlec = "sorszámú hiba bejelentés érkezett"
            #email2_from = str(hiba.id).decode('utf-8') + " " + email2_fejlec.decode('utf-8') + ' <tesztemailepuzbau@gmail.com>'

            #send_mail(str(hiba.id).decode('utf-8') + elso.decode('utf-8'), masodik.decode('utf-8') + str(hiba.id).decode('utf-8') + harmadik.decode('utf-8'),email1_from,[hiba.kapcsolattarto_email],fail_silently=False,)
            #send_mail(str(hiba.id).decode('utf-8') + negyedik.decode('utf-8'), str(hiba.id) + otodik.decode('utf-8'),email2_from,['info@epuzbaukft.hu'],fail_silently=False,)
            #send_mail(str(hiba.id).decode('utf-8') + negyedik.decode('utf-8'), str(hiba.id) + otodik.decode('utf-8'),email2_from,['epuzbaukft@gmail.com'],fail_silently=False,)

			# redirect to a new URL:
            return HttpResponseRedirect(reverse('hibalista') )

    # If this is a GET (or any other method) create the default form.
    else:
        form = HibaBejelentoForm()

    return render(request, 'hibak/hibabejelentes.html', {'form': form})

import xlwt
from django.http import HttpResponse
from django.utils import timezone
import pytz
def export_hibak_csv(request):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="hibak.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Hibak')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.num_format_str = 'YYYY/MM/DD - hh:mm'
    font_style.font.bold = True

    font_style2 = xlwt.XFStyle()
    font_style2.font.bold = True

    time_zone = pytz.timezone('Europe/Budapest')


    columns = ['Azonosító','Bejelentő neve', 'Hiba címe', 'Hiba leírása', 'Bejelentő e-mail címe', 'Bejelentés időpontja']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows

    rows = Hiba.objects.all().values_list('id','nev', 'cim', 'leiras', 'kapcsolattarto_email', 'bejelentes_datuma')
    visszajel = Visszajelzes.objects.all();
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 5:
                ws.write(row_num, col_num, str(row[col_num].astimezone(time_zone).strftime('%Y-%m-%d %H:%M')), font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style2)
        db = 0
        for vissz in visszajel:
            if vissz.hiba.id == row[0]:
                row_num += 1
                db+=1
                ws.write(row_num, 1, str(vissz.hiba.id) + " / Visszajelzés " + str(db), font_style)
                ws.write(row_num, 2, vissz.uzenet, font_style)
                ws.write(row_num, 3, str(vissz.datum.astimezone(time_zone).strftime('%Y-%m-%d %H:%M')), font_style)

    wb.save(response)
    return response
