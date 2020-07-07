import numpy as np
from scipy import stats
from scipy import signal
from scipy import integrate
import matplotlib.pyplot as plt
import csv

#Guardar datos en un list
with open('bits10k.csv', newline='') as csvfile:
  data = list(csv.reader(csvfile))

bits = [0]*len(data)
for c in range(0,10000):
  bits[c]=int(data[c][0])

# Número de bits
N = len(bits)

# Variable aleatoria binaria equiprobable
X = stats.bernoulli(0.5)

# Generar bits para "transmitir"
#bits = X.rvs(N)

'''
Punto 1

'''

# Frecuencia de operación
f = 5000 # Hz

# Duración del período de cada símbolo (onda)
T = 1/f # 1 ms

# Número de puntos de muestreo por período
p = 50

# Puntos de muestreo para cada período
tp = np.linspace(0, T, p)

# Creación de la forma de onda de la portadora
sinus = np.sin(2*np.pi * f * tp)

# Frecuencia de muestreo
fs = p/T # 50 kHz

# Creación de la línea temporal para toda la señal Tx
t = np.linspace(0, N*T, N*p)

# Inicializar el vector de la señal
senal = np.zeros(t.shape)

# Creación de la señal modulada BPSK
for k, b in enumerate(bits):
  senal[k*p:(k+1)*p] = ((2*b)-1) * sinus

# Visualización de los primeros bits modulados

pb = 10
plt.figure()
plt.plot(senal[0:pb*p]) 
plt.savefig('Tx.png')


'''
Punto 2
'''

# Potencia instantánea
Pinst = senal**2

# Potencia promedio (W)
Ps = integrate.trapz(Pinst, t) / (N * T)

# Iterar para varios valores de SNR
muestreo = 25
y = np.linspace(-10,3,muestreo)
BER = [0]*muestreo
SNR = [0]*muestreo
for l, x in enumerate(y):
  '''
  Punto 3
  '''
# Relación señal-a-ruido deseada
  SNR[l] = x

# Potencia del ruido para SNR y potencia de la señal dadas
  Pn = Ps / (10**(SNR[l] / 10))

# Desviación estándar del ruido
  sigma = np.sqrt(Pn)

# Crear ruido (Pn = sigma^2)
  ruido = np.random.normal(0, sigma, senal.shape)

# Simular "el canal": señal recibida
  Rx = senal + ruido

# Visualización de los primeros bits recibidos para SNR=0,833 dB
  if (l==20):
    pb = 10
    plt.figure()
    plt.plot(Rx[0:pb*p])
    plt.savefig('Rx.png')

  '''
  Punto 4
  '''
  if (l==20):
# Antes del canal ruidoso
    fw, PSD = signal.welch(senal, fs, nperseg=1024)
    plt.figure()
    plt.semilogy(fw, PSD)
    plt.xlabel('Frecuencia / Hz')
    plt.ylabel('Densidad espectral de potencia / V**2/Hz')
    plt.savefig('PSD.png')

# Después del canal ruidoso con SNR=0,833 dB
    fw, PSD = signal.welch(Rx, fs, nperseg=1024)
    plt.figure()
    plt.semilogy(fw, PSD)
    plt.xlabel('Frecuencia / Hz')
    plt.ylabel('Densidad espectral de potencia / V**2/Hz')
    plt.savefig('PSD_ruido.png')


  '''
  Punto 5
  '''

# Pseudo-energía de la onda original
  Es = np.sum(sinus**2)

# Inicialización del vector de bits recibidos
  bitsRx = np.zeros(len(bits))

# Decodificación de la señal por detección de energía
  for k, b in enumerate(bits):
  # Producto interno de dos funciones
    Ep = np.sum(Rx[k*p:(k+1)*p] * sinus) 
    if Ep > Es/2:
      bitsRx[k] = 1
    else:
      bitsRx[k] = 0

  err = np.sum(np.abs(bits - bitsRx))
  BER[l] = err/N


'''
Punto 6
'''

#Graficar BER versus SNR
plt.figure()
plt.plot(SNR, BER)
plt.xlabel('SNR')
plt.ylabel('BER')
plt.savefig('BERvs.SNR.png')