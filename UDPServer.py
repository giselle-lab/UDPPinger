# T2 - Giselle de Souza Pereira
from socket import *
import random
import time
import datetime


# Qual é o seu endereço IP e a porta que devemos usar?
recieveHost = 'localhost'
recievePort = 30000

codPing = 1 # recebe ping = 0; envia pong = 1


# Cria um soquete UDP Server
# Observe o uso de SOCK_DGRAM para pacotes UDP
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Atribuir endereço IP e número da porta ao soquete
serverSocket.bind((recieveHost, recievePort))

# quando há pacotes perdidos setar para True, quando não setar para False
pacotesPerdidos = True
atrasoEnvio = True  # quando há atraso no envio setar para True, quando não setar para False

# obtem o tempo em milissegundos
# def current_milli_time():
#     return round(time.time() * 1000)

while True:

  try:
    # Gera número aleatório no intervalo de 0 a 10
    rand = random.randint(0, 10)

    # Receba o pacote do cliente junto com o endereço de onde ele está vindo
    message, address = serverSocket.recvfrom(1024)

    # Capitalize a mensagem do cliente
    # message = message.upper()

    # decodifica a mensagem do cliente 
    message = message.decode()

    # estilo da msg: 000004294GiselleOi
    nMsg = message[0:5] #numero da message 000XX
    pingPong = message[5:6] #pega o byte que determina ping ou pong
    tempo = message[6:10] # pega o tempo marcado
    msgClient = message[10:40] #pega a mensagem do cliente de até 30 caracteres

    print(f'Message:   {message}')

    #para devolver a mensagem como pong altera o valor para 1
    if pingPong == '0':
      pingPong = '1'

    # Se rand for menor que 4, consideramos o pacote perdido e não respondemos
    # if rand < 4:
    #   print('PAC')
    #   continue

    # tempo que o pacote chegou
    tempoChegada = int(str(datetime.datetime.now())[20:24]) 

    difTempo = tempoChegada - int(tempo)
    print(difTempo)
    if(difTempo) < 1:
      print('Tempo excedido')
      serverSocket.sendto('aaaaaaa'.encode('utf-8'), address)
      continue
    else:
      tempo = tempoChegada

    # concatena novamente
    messageC = f'{nMsg}{pingPong}{tempo}{msgClient}'

    # Caso contrário, o servidor responde
    serverSocket.sendto(messageC.encode('utf-8'), address)
    print (f'Enviando: {messageC} ')

  except e:
    print('eroor')
