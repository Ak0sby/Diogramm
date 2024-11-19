from django.shortcuts import render, redirect
from rest_framework import viewsets

from .forms import ReportForm
from .models import Report
from .serializers import ReportSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import matplotlib
matplotlib.use('Agg')  # GUI жок графикаларды түзүү үчүн
import matplotlib.pyplot as plt
import io
import base64

# Логинден кийин колдонуучуларды багыттоо
@login_required
def login_redirect_view(request):
    if request.user.is_staff:
        return redirect('admin_reports')  # Админ баракчасы
    else:
        return redirect('create_report')  # Колдонуучунун диограмма толтуруу баракчасы

# Колдонуучунун отчетун түзүү
@login_required
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()

            labels = ['СПРАВКИ', 'ПОСТ ЦПГУ', 'ТРЕБ МИЛ', 'ВЛИТИЯ КАРТ', 'АКТУАЛ', 'ПОСТ ПРЕКР', 'ПОСТ ОБЬЯВЛ', 'ИСТРЕБОВАНИЕ']
            values = [
                report.spravki or 0,
                report.post_cpgu or 0,
                report.treb_mil or 0,
                report.vlitiya_kart or 0,
                report.aktual or 0,
                report.post_prekr or 0,
                report.post_objavl or 0,
                report.istreb or 0
            ]

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
            ax1.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
            ax1.set_title(f'Отчет - {report.user.username}')
            ax2.bar(labels, values, color='blue')
            ax2.set_title('Каличестволук Диаграмма')
            ax2.set_xticklabels(labels, rotation=45, ha='right')

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()

            graph = base64.b64encode(image_png).decode('utf-8')
            plt.close(fig)

            return render(request, 'report.html', {'form': form, 'graph': graph})

    else:
        form = ReportForm()

    return render(request, 'report.html', {'form': form})

# Жалпы жыйынтык диаграмма
def generate_summary_diagram():
    reports = Report.objects.all()
    labels = ['СПРАВКИ', 'ПОСТ ЦПГУ', 'ТРЕБ МИЛ', 'ВЛИТИЯ КАРТ', 'АКТУАЛ', 'ПОСТ ПРЕКР', 'ПОСТ ОБЬЯВЛ', 'ИСТРЕБОВАНИЕ']
    values = [0] * len(labels)

    for report in reports:
        values[0] += report.spravki or 0
        values[1] += report.post_cpgu or 0
        values[2] += report.treb_mil or 0
        values[3] += report.vlitiya_kart or 0
        values[4] += report.aktual or 0
        values[5] += report.post_prekr or 0
        values[6] += report.post_objavl or 0
        values[7] += report.istreb or 0

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
    ax1.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    ax1.set_title('Жалпы Жыйынтык Диаграмма')
    ax2.bar(labels, values, color='blue')
    ax2.set_title('Жалпы Каличестволук Диаграмма')
    ax2.set_xticklabels(labels, rotation=45, ha='right')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close(fig)

    return base64.b64encode(image_png).decode('utf-8')

# Админ үчүн бардык отчетторду көрүү
@staff_member_required
def admin_reports_view(request):
    reports = Report.objects.all()
    diagrams = []

    for report in reports:
        labels = ['СПРАВКИ', 'ПОСТ ЦПГУ', 'ТРЕБ МИЛ', 'ВЛИТИЯ КАРТ', 'АКТУАЛ', 'ПОСТ ПРЕКР', 'ПОСТ ОБЬЯВЛ', 'ИСТРЕБОВАНИЕ']
        values = [
            report.spravki or 0,
            report.post_cpgu or 0,
            report.treb_mil or 0,
            report.vlitiya_kart or 0,
            report.aktual or 0,
            report.post_prekr or 0,
            report.post_objavl or 0,
            report.istreb or 0
        ]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(25, 8))
        ax1.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        ax1.set_title(f'Отчет - {report.user.username}')
        ax2.bar(labels, values, color='blue')
        ax2.set_title('Каличестволук Диаграмма')
        ax2.set_xticklabels(labels, rotation=45, ha='right')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close(fig)

        diagrams.append((report, base64.b64encode(image_png).decode('utf-8')))

    summary_diagram = generate_summary_diagram()

    return render(request, 'admin_reports.html', {'diagrams': diagrams, 'summary_diagram': summary_diagram})

# ReportViewSet
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Колдонуучу отчетту түзүүдө аны ошол учурдагы колдонуучу менен байланыштырып сактайт
        serializer.save(user=self.request.user)
