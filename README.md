# EjsMqtt

·Ejercicio 2: 
Dado el topic numbers, leemos los números creados y separamos en enteros y relaes, calculando la frecuencia de cada número.

·Ejercicio 3: 
Dado el topic de temperaturas vamos recogiendo los datos de distintos sensores, calculando la emp max, minima y media de cada sensor; y luego la max, min y media en general.

·Ejercicio 4: 
Código que va tomando temperaturas de temperaturet1, si esas superan cierto valor k0 (en el código 30) se subscriben a humedad, si sisminuyen de este valor o los valores de humidity son mayores al limite k1 (en el código 60) se desubscriben del humidity.

·Ejercicio 5: 
Utilizando el topic 'numbers' del ej 2, usaremos sus mensajes coo temporizador.

·Ejercicio 6: 
Se diseña un esquema de diferentes clientes mqtt, encadenen su comportamiento. Un cliente escucha números y si recibe un entero multiplo de 5, pone una alarma en el temporizador, durante ese tiempo, se pone a escuchar en el topic temp1 para calcular el maximo valor, si es mayor que 40 se subscribe a humidity hasta que baje de 20.
