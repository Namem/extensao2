from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Pergunta, Opcao, Diagnostico, DiagnosticoEvento

class MotorInferenciaTests(APITestCase):

    def setUp(self):
        """
        Prepara o terreno antes de cada teste rodar.
        """
        # 1. Cria um usuário de teste e força a autenticação do cliente DRF
        User = get_user_model()
        self.user = User.objects.create_user(username='produtor_teste', password='senha_segura_123')
        self.client.force_authenticate(user=self.user)

        # 2. Cria as Folhas (Diagnóstico)
        self.diagnostico_pinta = Diagnostico.objects.create(
            nome="Pinta Preta Teste",
            descricao="Fungo genérico",
            recomendacao_manejo="Aplicar fungicida"
        )

        # 3. Cria os Nós (Perguntas)
        self.pergunta_raiz = Pergunta.objects.create(texto="Onde está a mancha?")
        self.pergunta_folha = Pergunta.objects.create(texto="Qual a cor da mancha na folha?")

        # 4. Cria as Arestas (Opções) ligando os pontos
        self.opcao_ir_pra_folha = Opcao.objects.create(
            pergunta_origem=self.pergunta_raiz,
            texto="Na folha",
            proxima_pergunta=self.pergunta_folha
        )
        self.opcao_dar_diagnostico = Opcao.objects.create(
            pergunta_origem=self.pergunta_folha,
            texto="Preta com halo amarelo",
            diagnostico_final=self.diagnostico_pinta
        )

    def test_iniciar_diagnostico_retorna_raiz(self):
        """ Testa se o endpoint /iniciar/ acha a primeira pergunta corretamente """
        url = reverse('iniciar_diagnostico')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tipo'], 'pergunta')
        self.assertEqual(response.data['dados']['texto'], "Onde está a mancha?")

    def test_responder_retorna_proxima_pergunta(self):
        """ Testa se o motor avança para a pergunta filha correta """
        url = reverse('responder_diagnostico')
        data = {'opcao_id': self.opcao_ir_pra_folha.id}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tipo'], 'pergunta')
        self.assertEqual(response.data['dados']['texto'], "Qual a cor da mancha na folha?")

    def test_responder_retorna_diagnostico_final(self):
        """ Testa se o motor encerra a árvore e devolve o diagnóstico """
        url = reverse('responder_diagnostico')
        data = {'opcao_id': self.opcao_dar_diagnostico.id}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tipo'], 'diagnostico')
        self.assertEqual(response.data['dados']['nome'], "Pinta Preta Teste")


class DiagnosticoEventoTests(APITestCase):
    """Testes para o model DiagnosticoEvento e o endpoint /historico/."""

    def setUp(self):
        """Cria usuário autenticado e um evento de exemplo."""
        User = get_user_model()
        self.user = User.objects.create_user(username='sensor_teste', password='senha_segura_123')
        self.client.force_authenticate(user=self.user)

        self.evento = DiagnosticoEvento.objects.create(
            device_id='ceres_001',
            classe_detectada='Requeima',
            confianca=0.87,
            temperatura=28.4,
            umidade_ar=82,
            umidade_solo=65,
            timestamp=timezone.now(),
        )

    def test_evento_criado_com_dados_validos(self):
        """Verifica que o evento foi salvo corretamente no banco."""
        self.assertEqual(DiagnosticoEvento.objects.count(), 1)
        evento = DiagnosticoEvento.objects.first()
        self.assertEqual(evento.device_id, 'ceres_001')
        self.assertEqual(evento.classe_detectada, 'Requeima')
        self.assertAlmostEqual(evento.confianca, 0.87)
        self.assertEqual(evento.temperatura, 28.4)
        self.assertEqual(evento.umidade_ar, 82)
        self.assertEqual(evento.umidade_solo, 65)

    def test_historico_retorna_lista_paginada(self):
        """Verifica que o endpoint /historico/ retorna JSON paginado com os eventos."""
        url = reverse('historico_eventos')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['device_id'], 'ceres_001')
