"""
Command Django para escutar mensagens MQTT do ESP32 e persistir no banco.

Uso:
    python manage.py mqtt_listener
    python manage.py mqtt_listener --host 192.168.1.100 --port 1883

Encerrar com Ctrl+C — shutdown limpo garantido.
"""

import json
import os
import signal
import time
import logging

import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from diagnostico.models import DiagnosticoEvento

logger = logging.getLogger(__name__)

TOPICO = 'ceres/sensor/#'

# Broker via env vars (HiveMQ Cloud ou Mosquitto local)
_MQTT_HOST     = os.getenv('MQTT_HOST', 'localhost')
_MQTT_PORT     = int(os.getenv('MQTT_PORT', '1883'))
_MQTT_USER     = os.getenv('MQTT_USER', '')
_MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', '')
_MQTT_TLS      = os.getenv('MQTT_TLS', 'false').lower() == 'true'


class Command(BaseCommand):
    """Listener MQTT — recebe dados dos dispositivos ESP32 e persiste no banco."""

    help = 'Inicia o listener MQTT que recebe dados dos dispositivos ESP32.'

    def add_arguments(self, parser):
        """Define argumentos opcionais de linha de comando."""
        parser.add_argument('--host', default=_MQTT_HOST, help='Broker MQTT host.')
        parser.add_argument('--port', type=int, default=_MQTT_PORT, help='Broker MQTT porta.')
        parser.add_argument('--user', default=_MQTT_USER, help='Usuário MQTT.')
        parser.add_argument('--password', default=_MQTT_PASSWORD, help='Senha MQTT.')
        parser.add_argument('--tls', action='store_true', default=_MQTT_TLS, help='Usar TLS.')

    def handle(self, *args, **options):
        """Ponto de entrada do command — inicializa o cliente MQTT."""
        host     = options['host']
        port     = options['port']
        user     = options['user']
        password = options['password']
        use_tls  = options['tls']

        self.stdout.write(self.style.SUCCESS(
            f'[MQTT] Iniciando listener → {host}:{port} | TLS:{use_tls} | Tópico: {TOPICO}'
        ))

        self._rodando = True
        signal.signal(signal.SIGTERM, self._encerrar)
        signal.signal(signal.SIGINT, self._encerrar)

        self._conectar_com_retry(host, port, user, password, use_tls)

    def _encerrar(self, signum, frame):
        """Callback de shutdown limpo ao receber SIGTERM ou SIGINT."""
        self.stdout.write(self.style.WARNING('\n[MQTT] Encerrando listener...'))
        self._rodando = False

    def _conectar_com_retry(self, host, port, user='', password='', use_tls=False):
        """Tenta conectar ao broker com retry exponencial (1s, 2s, 4s, 8s...)."""
        espera = 1
        while self._rodando:
            try:
                cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
                cliente.on_connect = self._ao_conectar
                cliente.on_message = self._ao_receber_mensagem
                cliente.on_disconnect = self._ao_desconectar

                if user:
                    cliente.username_pw_set(user, password)
                if use_tls:
                    cliente.tls_set()

                cliente.connect(host, port, keepalive=60)
                cliente.loop_start()

                # Mantém o processo vivo enquanto _rodando for True
                while self._rodando:
                    time.sleep(1)

                cliente.loop_stop()
                cliente.disconnect()
                break

            except Exception as erro:
                self.stdout.write(self.style.ERROR(
                    f'[MQTT] Falha na conexão ({host}:{port} TLS={use_tls} user={user}): {erro}. Tentando em {espera}s...'
                ))
                time.sleep(espera)
                espera = min(espera * 2, 60)  # Máximo de 60s entre tentativas

    def _ao_conectar(self, cliente, userdata, flags, reason_code, properties):
        """Callback chamado quando a conexão com o broker é estabelecida."""
        if reason_code == 0:
            self.stdout.write(self.style.SUCCESS('[MQTT] Conectado ao broker!'))
            cliente.subscribe(TOPICO)
            self.stdout.write(f'[MQTT] Inscrito no tópico: {TOPICO}')
        else:
            self.stdout.write(self.style.ERROR(f'[MQTT] Falha ao conectar. Código: {reason_code}'))

    def _ao_desconectar(self, cliente, userdata, flags, reason_code, properties):
        """Callback chamado quando a conexão com o broker é perdida."""
        if reason_code != 0:
            self.stdout.write(self.style.WARNING('[MQTT] Desconectado inesperadamente. Reconectando...'))

    def _ao_receber_mensagem(self, cliente, userdata, mensagem):
        """Callback chamado para cada mensagem recebida — valida e persiste no banco."""
        topico = mensagem.topic
        payload = mensagem.payload.decode('utf-8')

        self.stdout.write(f'[MQTT] Mensagem recebida em "{topico}": {payload}')

        try:
            dados = json.loads(payload)
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'[MQTT] JSON inválido: {e}'))
            return

        # Valida campos obrigatórios
        campos_obrigatorios = ['device_id', 'temperatura', 'umidade_ar', 'umidade_solo']
        for campo in campos_obrigatorios:
            if campo not in dados:
                self.stdout.write(self.style.ERROR(f'[MQTT] Campo ausente: {campo}'))
                return

        # Converte o timestamp — usa o momento atual se não fornecido
        timestamp_str = dados.get('timestamp')
        timestamp = parse_datetime(timestamp_str) if timestamp_str else timezone.now()
        if timestamp is None:
            timestamp = timezone.now()

        try:
            evento = DiagnosticoEvento.objects.create(
                device_id=dados['device_id'],
                classe_detectada=dados.get('classe_detectada'),
                confianca=dados.get('confianca'),
                temperatura=dados['temperatura'],
                umidade_ar=dados['umidade_ar'],
                umidade_solo=dados['umidade_solo'],
                timestamp=timestamp,
            )
            self.stdout.write(self.style.SUCCESS(
                f'[MQTT] Evento #{evento.id} salvo — dispositivo: {evento.device_id}'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'[MQTT] Erro ao salvar evento: {e}'))
