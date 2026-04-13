from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Pergunta, Opcao, Diagnostico

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