from django.contrib import admin
from .models import Diagnostico, Pergunta, Opcao

# Configuração para criar as opções diretamente na mesma tela da pergunta
class OpcaoInline(admin.TabularInline):
    model = Opcao
    extra = 2
    fk_name = 'pergunta_origem'

class PerguntaAdmin(admin.ModelAdmin):
    inlines = [OpcaoInline]
    search_fields = ['texto']

class DiagnosticoAdmin(admin.ModelAdmin):
    search_fields = ['nome']

admin.site.register(Diagnostico, DiagnosticoAdmin)
admin.site.register(Pergunta, PerguntaAdmin)