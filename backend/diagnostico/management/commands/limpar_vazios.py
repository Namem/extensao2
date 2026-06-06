"""Apaga eventos DiagnosticoEvento sem classe_detectada (lixo de testes)."""

from django.core.management.base import BaseCommand
from diagnostico.models import DiagnosticoEvento


class Command(BaseCommand):
    help = 'Remove eventos sem classe_detectada (gerados por testes incompletos).'

    def handle(self, *args, **options):
        qs = DiagnosticoEvento.objects.filter(classe_detectada__isnull=True)
        total = qs.count()
        if total == 0:
            self.stdout.write('Nenhum evento vazio encontrado.')
            return
        qs.delete()
        self.stdout.write(f'{total} eventos vazios removidos.')
