"""Popula o banco com eventos de teste realistas para apresentação do TCC.

Idempotente: se já existem >= 15 eventos com GPS e classe, não faz nada.
Limpa eventos vazios (sem classe_detectada) antes de popular.
"""

import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from diagnostico.models import DiagnosticoEvento

User = get_user_model()

# Coordenadas de fazendas reais na região de Sorriso-MT e Cuiabá-MT
LOCAIS = [
    # Sorriso-MT — polo de produção agrícola
    (-12.5427, -55.7114, 'Fazenda Sta. Clara'),
    (-12.5602, -55.7283, 'Fazenda Esperança'),
    (-12.5185, -55.6941, 'Talhão Norte'),
    (-12.5750, -55.7450, 'Pivô Central'),
    (-12.5320, -55.7020, 'Lote 12'),
    # Cuiabá-MT — IFMT Campus Cuiabá
    (-15.5761, -56.0840, 'IFMT Horta Experimental'),
    (-15.5785, -56.0870, 'Estufa A'),
    (-15.5810, -56.0815, 'Estufa B'),
    (-15.5730, -56.0900, 'Campo Aberto IFMT'),
    (-15.5695, -56.0770, 'Canteiro Demonstração'),
    # Várzea Grande / região metropolitana
    (-15.6100, -56.1320, 'Sítio São José'),
    (-15.6250, -56.0950, 'Chácara Alvorada'),
    # Lucas do Rio Verde — outro polo agrícola
    (-13.0497, -55.9094, 'Fazenda Progresso'),
    (-13.0650, -55.9200, 'Pivô LRV-3'),
]

# Distribuição realista de classes (doença vs saudável)
CLASSES = [
    ('D01_requeima',            0.82, 0.92),
    ('D01_requeima',            0.75, 0.88),
    ('D02_septoriose',          0.78, 0.90),
    ('D03_pinta_preta',         0.80, 0.91),
    ('D03b_mancha_alvo',        0.70, 0.85),
    ('D05_mofo_foliar',         0.83, 0.93),
    ('D06_vira_cabeca',         0.76, 0.89),
    ('D06b_mosaico',            0.72, 0.87),
    ('D07_acaro_bronzeamento',  0.68, 0.84),
    ('D09_mancha_bacteriana',   0.81, 0.91),
    ('D09_mancha_bacteriana',   0.77, 0.90),
    ('saudavel',                0.88, 0.96),
    ('saudavel',                0.85, 0.95),
    ('saudavel',                0.90, 0.97),
    ('D01_requeima',            0.79, 0.91),
    ('D03_pinta_preta',         0.74, 0.88),
    ('D05_mofo_foliar',         0.80, 0.92),
    ('saudavel',                0.87, 0.95),
    ('D02_septoriose',          0.73, 0.86),
    ('D06_vira_cabeca',         0.78, 0.90),
]


class Command(BaseCommand):
    help = 'Limpa eventos vazios e popula banco com dados realistas para apresentação.'

    def handle(self, *args, **options):
        # 1. Limpar eventos sem classe_detectada
        vazios = DiagnosticoEvento.objects.filter(
            Q(classe_detectada__isnull=True) | Q(classe_detectada='')
        )
        n_vazios = vazios.count()
        if n_vazios:
            vazios.delete()
            self.stdout.write(f'{n_vazios} eventos vazios removidos.')

        # 2. Verificar se já tem dados suficientes
        com_gps = DiagnosticoEvento.objects.filter(
            latitude__isnull=False,
            classe_detectada__isnull=False,
        ).exclude(classe_detectada='').count()

        if com_gps >= 15:
            self.stdout.write(f'Banco já tem {com_gps} eventos com GPS — pulando seed.')
            return

        # 3. Buscar usuário test (ou None)
        try:
            user = User.objects.get(username='test@test.com')
        except User.DoesNotExist:
            user = None
            self.stdout.write('Usuário test@test.com não encontrado — eventos sem dono.')

        # 4. Criar eventos
        agora = timezone.now()
        random.seed(42)
        criados = 0

        for i, (classe, conf_min, conf_max) in enumerate(CLASSES):
            local = LOCAIS[i % len(LOCAIS)]
            lat, lon, nome_local = local

            # Adicionar leve jitter ao GPS (±50m)
            lat += random.uniform(-0.0005, 0.0005)
            lon += random.uniform(-0.0005, 0.0005)

            confianca = round(random.uniform(conf_min, conf_max), 4)

            # Timestamps espalhados nos últimos 7 dias
            delta = timedelta(
                days=random.randint(0, 6),
                hours=random.randint(6, 17),
                minutes=random.randint(0, 59),
            )
            ts = agora - delta

            # Sensores simulados (condições de Mato Grosso)
            temp = round(random.uniform(28.0, 38.0), 1)
            umid_ar = round(random.uniform(45.0, 85.0), 1)
            umid_solo = round(random.uniform(30.0, 70.0), 1)

            DiagnosticoEvento.objects.create(
                device_id=f'app_test@test.com',
                classe_detectada=classe,
                confianca=confianca,
                latitude=round(lat, 6),
                longitude=round(lon, 6),
                timestamp=ts,
                temperatura=temp,
                umidade_ar=umid_ar,
                umidade_solo=umid_solo,
                usuario=user,
            )
            criados += 1

        self.stdout.write(f'{criados} eventos de teste criados com sucesso.')
        self.stdout.write(
            f'Locais: Sorriso-MT, IFMT Cuiabá, Várzea Grande, Lucas do Rio Verde.'
        )
