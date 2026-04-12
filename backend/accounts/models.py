from django.db import models
from django.contrib.auth.models import AbstractUser

class Tenant(models.Model):
    """
    Modelo para suportar diferentes cooperativas, associações ou grupos de produtores.
    Isso garante que os dados de uma associação não se misturem com os de outra.
    """
    nome = models.CharField(max_length=255, verbose_name="Nome da Associação/Cooperativa")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class CustomUser(AbstractUser):
    """
    Usuário customizado que estende o padrão do Django, adicionando
    a relação com o Tenant e preparando o terreno para permissões específicas.
    """
    tenant = models.ForeignKey(
        Tenant, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='usuarios',
        verbose_name="Associação/Cooperativa"
    )

    def __str__(self):
        return self.username