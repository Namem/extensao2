from django.db import models

class Diagnostico(models.Model):
    """ Representa as folhas da árvore: O resultado final da triagem """
    nome = models.CharField(max_length=200, verbose_name="Nome da Praga/Doença")
    descricao = models.TextField(verbose_name="Descrição Técnica")
    recomendacao_manejo = models.TextField(
        verbose_name="Recomendação de Manejo (Embrapa)",
        help_text="O que o produtor deve fazer ao identificar este problema."
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Pergunta(models.Model):
    """ Representa os nós da árvore: As perguntas feitas ao produtor """
    texto = models.CharField(
        max_length=255, 
        verbose_name="Texto da Pergunta",
        help_text="Ex: Em qual parte da planta está o problema?"
    )
    # No futuro, podemos adicionar um campo de imagem aqui para ilustrar a pergunta

    def __str__(self):
        return self.texto


class Opcao(models.Model):
    """ Representa os caminhos (arestas): As respostas que levam a outra pergunta ou a um diagnóstico """
    pergunta_origem = models.ForeignKey(
        Pergunta, 
        on_delete=models.CASCADE, 
        related_name='opcoes',
        verbose_name="Pergunta de Origem"
    )
    texto = models.CharField(
        max_length=200, 
        verbose_name="Texto da Opção",
        help_text="Ex: Na folha"
    )
    
    # A MÁGICA DA ÁRVORE ACONTECE AQUI:
    # Uma opção pode levar a uma nova pergunta OU encerrar no diagnóstico final.
    proxima_pergunta = models.ForeignKey(
        Pergunta, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='opcoes_que_trazem_aqui',
        verbose_name="Próxima Pergunta (Se houver)"
    )
    diagnostico_final = models.ForeignKey(
        Diagnostico, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Diagnóstico Final (Se encerrar a triagem)"
    )

    def __str__(self):
        destino = f"Pergunta: {self.proxima_pergunta.texto}" if self.proxima_pergunta else f"Diagnóstico: {self.diagnostico_final.nome}"
        return f"[{self.pergunta_origem.texto}] -> ({self.texto}) -> {destino}"