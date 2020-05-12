# Simulador SIR en aútomatas celulares


## Modelo SIR
Uno de  los modelos más sencillos para representar el coportamiento de las epidemias es el modelo SIR, el cual fue introducido por Kermack-McKendrick.
El modelo considera la  
La población **N** es dividida en :
- **S** Susceptibles: Son los individuos que pueden contraer la enfermedad 
- **I** Infectados. Son los individuos que están enfermos y pueden transmitir la enfermedad a los individuos susceptibles. 
- **R** Recuperados. Son los individuos que estuvieron enfermos y se han recuperado, estos individuos generaron inmunidad por lo que no pueden volverse a enfermar. [1]

[1] [A. M. del Rey, S. H. White, and G. R. Sánchez, “A model based on cellularautomata to simulate epidemic diseases,” pp. 304–310, 2006](https://doi.org/10.1007/11861201_36) 

## Instalación

Este simulador web  esta hecho con Python y flask. 
Existen dos maneras para descargar y desplegar el simulador:
- Descargar el repositorio y correr el servidor flask
- Descargar la imagen Docker del proyect de Dockerhub

### Descargar de github
```
git clone https://github.com/Carlos-ZRM/COVID.git
cd COVID
```

#### Preparar el entorno virtual

```
virtualenv flask-venv
source flask-venv/bin/activate
pip install -r requirements.txt 

```

#### Iniciar el servidor 
El servidor utilizara el puerto 80. Si desea cambiar el puerto debe modificar las siguientes lineas  del archivo *app/run.py*
```


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("80"), debug=True)



```
Para iniciar el sevidor :

```
cd app
python run.py
```
### Descargar imagen del Dockerhub

```
docker pull carloszrm/sir-covid-mexico
docker run -d --name flask-sir -p 5000:80  carloszrm/sir-covid-mexico
```
El servidor se desplegará en el puerto 5000. Si desea cambiar el puerto debe modificar la bandera **-p \<puerto-host\>:80**


<!--stackedit_data:
eyJoaXN0b3J5IjpbODI0MDkxNzg2LDExMjQ0MzE5LDEyMDQ0MT
AwMTcsLTY1MzYxMDM2NCw5ODU5MjQ5OTZdfQ==
-->