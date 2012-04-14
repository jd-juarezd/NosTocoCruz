# Social Djungle
* * *
## Estrategia de Branching
Existen tres ramas:
1. master: versión estable que ha superado con éxito toda una sesión de tests.
2. test: versión copia de master en la que se incluyen los tests desarrollados.
3. development: versión que une test y master con el objetivo de desarrollar hasta superar todos los tests.

### Inicialización del repositorio
1. git clone git@github.com:alessandrofg/NosTocoCruz.git
2. git checkout -b development origin/development
3. git checkout -b test origin/test

### Merges
1. Para actualizar la versión estable:
	* git checkout master
	* git merge development
2. Para actualizar la rama de tests:
	* git checkout test
	* git merge master

### Pulls
Deben realizarse `git pull` cada vez que se comience a trabajar



