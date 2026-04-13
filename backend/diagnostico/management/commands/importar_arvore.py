import json
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from diagnostico.models import Diagnostico, Pergunta, Opcao

class Command(BaseCommand):
    help = 'Importa a árvore de decisão do tomateiro a partir de um JSON'

    def handle(self, *args, **options):
        # Caminho do arquivo
        file_path = os.path.join('diagnostico', 'data', 'arvore_diagnostico.json')

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        try:
            with transaction.atomic():
                # Limpando dados antigos para evitar duplicidade
                Opcao.objects.all().delete()
                Pergunta.objects.all().delete()
                Diagnostico.objects.all().delete()

                # 1. Criar Diagnósticos e guardar em um dicionário para mapear IDs
                diag_map = {}
                for d in data['diagnosticos']:
                    obj = Diagnostico.objects.create(
                        nome=d['nome'],
                        descricao=d['descricao'],
                        recomendacao_manejo=d['recomendacao_manejo']
                    )
                    diag_map[d['id']] = obj

                # 2. Criar Perguntas primeiro (sem opções)
                perg_map = {}
                for p in data['perguntas']:
                    obj = Pergunta.objects.create(texto=p['texto'])
                    perg_map[p['id']] = obj

                # 3. Criar as Opções e ligar os pontos
                for p_data in data['perguntas']:
                    pergunta_origem = perg_map[p_data['id']]
                    for opt in p_data['opcoes']:
                        Opcao.objects.create(
                            pergunta_origem=pergunta_origem,
                            texto=opt['texto'],
                            proxima_pergunta=perg_map.get(opt['proxima_pergunta_id']),
                            diagnostico_final=diag_map.get(opt['diagnostico_final_id'])
                        )

                self.stdout.write(self.style.SUCCESS('Árvore de decisão importada com sucesso!'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro na importação: {e}'))