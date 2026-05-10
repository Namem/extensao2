# Ceres Diagnóstico — Resumo Executivo
**IFMT Campus Cuiabá — Engenharia da Computação**
**Autor:** Namem Rachid Jaudy Neto | **Ano:** 2026

---

## O Problema

O tomateiro é uma das hortaliças mais importantes do Brasil. Doenças como
requeima, septoriose e mancha bacteriana podem destruir uma lavoura inteira
em poucos dias se não forem detectadas cedo.

O problema: **o diagnóstico depende de um agrônomo especializado.** Para o
pequeno produtor rural, isso significa esperar dias ou semanas, pagar por
uma visita técnica, e muitas vezes tratar a planta com o defensivo errado.

---

## A Solução

O **Ceres Diagnóstico** é um dispositivo pequeno e barato que o produtor
instala na lavoura. Ele funciona assim:

1. **O dispositivo tira uma foto** da folha do tomateiro automaticamente
2. **Uma inteligência artificial analisa a foto** em menos de 2 segundos,
   diretamente no aparelho — sem precisar de internet
3. **O resultado aparece no celular do produtor:** qual doença foi detectada,
   com que nível de confiança, e o que fazer
4. **Os dados de temperatura, umidade do ar e umidade do solo** são enviados
   junto com o diagnóstico para o histórico

Tudo isso funciona mesmo em áreas sem sinal de internet.

---

## Como foi desenvolvido

### A inteligência artificial
Foi treinada com **88.949 fotos** de folhas de tomate saudáveis e doentes,
coletadas em laboratório. O resultado: **98% de acerto** em condições
controladas.

O modelo é tão pequeno (**639 KB**) que cabe em um chip do tamanho de
uma moeda — o ESP32-S3, que custa menos de R$ 50.

### Os dois experimentos
Para garantir o melhor resultado, dois métodos de treinamento foram
comparados lado a lado:

| | Método A | Método B (escolhido) |
|---|---|---|
| Plataforma | Serviço na nuvem | Computador local com GPU |
| Resultado | 62% de acerto | **98% de acerto** |
| Tamanho | 624 KB | 639 KB |

A diferença: o Método B usou uma técnica de calibração que o Método A não
usou, o que fez toda a diferença na precisão.

### O teste no mundo real
O modelo foi testado com **1.353 fotos tiradas em lavouras reais** (dataset
PlantDoc). Resultado: **20,77%** — bem abaixo dos 98% do laboratório.

Isso é esperado e já foi documentado por pesquisadores do mundo todo:
modelos treinados em fotos de laboratório (fundo limpo, luz controlada)
têm dificuldade com fotos de campo (fundo natural, sombra, ângulos variados).

A solução já está em andamento: o sistema está sendo retreinado com fotos
que misturam folhas de laboratório com fundos naturais de lavoura.
**Meta: superar 70% de acerto no campo.**

---

## Onde está hoje

| Componente | Situação |
|---|---|
| Modelo de IA (639 KB) | ✅ Pronto |
| Backend + banco de dados | ✅ Pronto e testado |
| Comunicação MQTT (IoT) | ✅ Pronto e testado |
| Retreino para campo real | 🔄 Em andamento |
| Firmware do hardware | ⏳ Próxima etapa |
| Aplicativo celular | ⏳ Próxima etapa |

---

## O que torna este projeto diferente

- **Funciona sem internet:** a IA roda dentro do chip, não na nuvem
- **Baixo custo:** hardware alvo abaixo de R$ 200
- **10 doenças detectadas:** a maioria dos trabalhos similares detecta 4 ou 5
- **Validado em campo real:** o gap entre laboratório e campo está documentado
  e a solução está sendo implementada
- **Código aberto:** qualquer pesquisador pode replicar o projeto

---

## Próximos passos

1. Retreinar o modelo com fundos naturais → superar 70% no campo
2. Instalar o modelo no hardware ESP32-S3
3. Medir a velocidade de diagnóstico no hardware real (meta: < 300ms)
4. Desenvolver o aplicativo Flutter para celular
5. Testar com produtores reais de Sorriso-MT

---

*Para detalhes técnicos completos, consulte `docs/TCC_CERES.md`*
*Para o estado atual do projeto, consulte `docs/BACKLOG.md`*
