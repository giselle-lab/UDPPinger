from socket import *
import sys
import datetime
import time
from statistics import stdev


recieveHost = '127.0.0.1'
recievePort = 30000

nMsg = 00000
pingPong = 0 # recebe ping = 0; envia pong = 1
timeInicial= 0000 #antes de enviar
msg = "GiselleOi" # messagem do cliente - até 30 caracteres


pkgEnviados = 0
pkgRecebidos = 0
rtt=[]
timeTotal = 0

# Cria um soquete UDP Cliente
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(2)

#verifica se a mensagem tem menos que 30 caracteres
while len(msg)> 30:
    print("Escolha uma mensagem com menos que 30 caracteres:")
    #msg = input()
else:
    print("Ok! A mensagem possui menos que 30 caracteres")
    msg = str(msg).ljust(30,'\0') #ajusta msg com \0


#cria a mensagem completa
for i in range(0, 10): 
  #tempo do inicio da msg
  timeInicial = int(str(datetime.datetime.now())[20:24]) 

  number = str(i).zfill(5)
  timeInicial = str(timeInicial)
  msgF = str(msg).ljust(30,'\0')
  msgCompleta = f"{number}{pingPong}{timeInicial}{msgF}"

  # enviando um pacote
  clientSocket.sendto(msgCompleta.encode(), (recieveHost, recievePort))

  pkgEnviados += 1

  try:
    data, server = clientSocket.recvfrom(1024)

    msgRecebida = data.decode()
    

    #se receber uma mensagem de erro
    if(msgRecebida[0:4]!='0000'):
      print('Pacote inválido')
      continue

    rttIndividual = int(msgRecebida[6:10]) - int(timeInicial)

    rtt.append(rttIndividual)
    print(f'Message Recebida:   {msgRecebida}')

    pkgRecebidos +=1
    timeChegada = msgRecebida[6:10]
    # print(timeChegada)
    # print(timeTotal)

  except:
    print('Pacote perdido [tempo limite excedido]')

timeTotal = sum(rtt)

if pkgRecebidos == 0:
  print('Nenhum pacote recebido')
else:
  result = f"{pkgEnviados} packets transmitted, {pkgRecebidos} received, {100 - pkgRecebidos/pkgEnviados*100}% packet loss,  time {timeTotal:.2f}ms rtt min/avg/max/mdev = {min(rtt):.4f}/{sum(rtt)/len(rtt):.4f}/{max(rtt):.4f}/{stdev(rtt):.4f} ms"
  print(result)
