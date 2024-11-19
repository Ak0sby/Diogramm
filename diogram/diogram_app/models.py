from django.db import models
from django.contrib.auth.models import User


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")  # Ар бир отчет колдонуучуга байланыштырылат
    spravki = models.IntegerField(verbose_name="Справки", blank=True, null=True)  # Ар бир талаа сандык мааниге ээ болот
    post_cpgu = models.IntegerField(verbose_name="ПОСТ  ЦПГУ", blank=True, null=True)
    treb_mil = models.IntegerField(verbose_name="ТРЕБ МИЛ", blank=True, null=True)
    vlitiya_kart = models.IntegerField(verbose_name="ВЛИТИЯ КАРТ", blank=True, null=True)
    aktual = models.IntegerField(verbose_name="АКТУАЛ", blank=True, null=True)
    post_prekr = models.IntegerField(verbose_name="ПОСТ ПРЕКР", blank=True, null=True)
    post_objavl = models.IntegerField(verbose_name="ПОСТ ОБЬЯВЛ", blank=True, null=True)
    istreb = models.IntegerField(verbose_name= "ИСТРЕБОВАНИЕ", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Отчет пользователя {self.user.username} (ID: {self.user.id}) - {self.created_at}"