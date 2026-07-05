# Manual do Usuário — Ceres Diagnóstico

**Atividade de Extensão II — IFMT Cuiabá**
**Autor:** Namem Rachid Jaudy Neto

Guia de uso do aplicativo **Ceres Diagnóstico** — diagnóstico de doenças do
tomateiro por foto, com IA embarcada no celular e monitoramento de sensores IoT.

---

## 1. Instalação do aplicativo

1. Copie o arquivo `ceres_diagnostico.apk` para o celular Android.
2. Toque no arquivo e permita "instalar de fonte desconhecida".
3. Abra o app **Ceres Diagnóstico**.

> Também é possível usar a versão web/desktop conectada à API em produção
> (`https://ceres.up.railway.app`).

---

## 2. Primeiro acesso

Ao abrir, o app mostra a **tela de abertura** (splash) e vai para o **Login**.

- **Entrar:** informe e-mail e senha e toque em *Entrar*.
- **Criar conta:** toque em *Criar conta* → escolha **Produtor** ou **Agrônomo**
  (o agrônomo informa o CREA), preencha nome, e-mail e senha (mín. 6 caracteres).
- **Esqueci a senha:** redefine a senha informando o e-mail cadastrado.
- **Continuar sem conta:** usa o app sem login (diagnóstico funciona; o histórico
  na nuvem fica indisponível).

---

## 3. Telas principais

O app tem **5 abas** na barra inferior: **Diagnóstico · Mapa · IoT · Enciclopédia · Perfil**.

### 3.1 Diagnóstico (foto da folha)

Tela principal. Fluxo de uso:

1. Toque em **Tirar foto** (câmera) ou **Galeria** para escolher uma imagem da folha.
2. O app classifica a imagem e mostra:
   - **Nome da doença** (ou *Saudável*);
   - **Confiança** (%) com barra graduada;
   - **Scores** das principais classes;
   - **Recomendação de manejo** (base Embrapa).
3. O resultado é **salvo automaticamente** (aparece "Salvo localmente").

**Modo Cloud x Offline** (alternável nesta tela e no Perfil):
- **Cloud:** envia a foto ao servidor (Railway) — resultado sincronizado, entra no mapa.
- **Offline:** a IA roda **no próprio celular** (TFLite, ~60 ms) — funciona sem internet.
  Nenhuma imagem sai do aparelho.

### 3.2 Mapa

Mostra as **ocorrências georreferenciadas** dos diagnósticos em um mapa
(OpenStreetMap). Cada marcador tem cor por urgência. Toque em um marcador para ver
doença, data, confiança e coordenadas.

### 3.3 IoT (sensores)

Exibe as leituras do **ESP32-S3** em tempo real:
- **Temperatura** e **umidade do ar** (sensor DHT22);
- **Umidade do solo** (sensor capacitivo);
- **Histórico** de eventos e status da conexão MQTT.

*(Screenshot: card de status do sensor — ver `assets/screenshots/iot_sensor_card.jpg`.)*

### 3.4 Enciclopédia

Fichas das **10 categorias** reconhecidas (9 doenças + saudável), com sintomas,
agente causal e ação recomendada. Há **busca** por nome, agente ou sintoma.

### 3.5 Perfil

- Nome, e-mail e **estatísticas** (total de diagnósticos, doenças, saudáveis);
- **Modo de inferência** (Cloud/Offline);
- **Exportar CSV** dos diagnósticos;
- **Sair** (logout).

---

## 4. As 10 categorias diagnosticadas

| Código | Doença | Código | Doença |
|---|---|---|---|
| D01 | Requeima | D06 | Vira-cabeça (TYLCV) |
| D02 | Septoriose | D06b | Mosaico |
| D03 | Pinta-preta | D07 | Ácaro-do-bronzeamento |
| D03b | Mancha-alvo | D09 | Mancha-bacteriana |
| D05 | Mofo-foliar | — | Saudável |

---

## 5. Uso offline e sincronização

- Sem internet, use o **modo Offline** — o diagnóstico roda no celular normalmente.
- Os diagnósticos feitos offline ficam salvos com a marca "não sincronizado".
- Ao **voltar a ter internet**, o app envia automaticamente os pendentes para a
  nuvem (aparecem no mapa e no histórico).

---

## 6. Dicas e observações

- **Foto da folha:** fotografe a folha bem iluminada, preenchendo o quadro. Fotos de
  campo (fundo natural, sombra) reduzem a confiança — é uma limitação conhecida
  (o modelo foi treinado com imagens de laboratório).
- **A confiança é uma estimativa.** Em caso de dúvida, consulte um agrônomo — o app
  é uma ferramenta de **triagem**, não substitui o diagnóstico profissional.
- **Privacidade:** no modo Offline nenhuma imagem sai do celular.

---

## 7. Suporte

- Repositório: https://github.com/Namem/extensao2
- API/produção: https://ceres.up.railway.app
- Autor: Namem Rachid Jaudy Neto — IFMT Cuiabá
