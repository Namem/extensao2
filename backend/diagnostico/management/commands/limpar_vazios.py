"""Apaga eventos DiagnosticoEvento sem classe_detectada (lixo de testes)."""

from django.core.management.base import BaseCommand
from diagnostico.models import DiagnosticoEvento


class Command(BaseCommand):
    help = 'Remove eventos sem classe_detectada (gerados por testes incompletos).'

    def handle(self, *args, **options):
        from django.db.models import Q
        # Apaga apenas eventos sem classe E sem dados de sensor.
        # Eventos MQTT do ESP32 têm temperatura mas podem não ter classe
        # (sensor puro sem IA) — esses são PRESERVADOS.
        qs = DiagnosticoEvento.objects.filter(
            Q(classe_detectada__isnull=True) | Q(classe_detectada='')
        ).filter(
            temperatura__isnull=True,
        )
        total = qs.count()
        if total == 0:
            self.stdout.write('Nenhum evento vazio encontrado.')
            return
        qs.delete()
        self.stdout.write(f'{total} eventos vazios removidos.')
