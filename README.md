# PruebaTecnica
Prueba técnica Sistema de Votaciones
Informe de Evidencias – Sistema de Votaciones con FastAPI

1. Arquitectura General del Proyecto
El sistema desarrollado es una API RESTful para gestionar un proceso de votaciones. Está construido sobre FastAPI y utiliza SQLAlchemy como ORM para interactuar con una base de datos SQL Server.

Componentes principales:
FastAPI: framework para construir la API de manera rápida, con documentación automática en Swagger.

SQLAlchemy: ORM que permite mapear las tablas de la base de datos a modelos de Python.

PyODBC: driver para la conexión con SQL Server.

Pydantic: validación de datos de entrada y salida mediante modelos.

Python-dotenv: manejo de variables de entorno para la configuración segura de la base de datos.

2. Estructura del Proyecto
El proyecto se organizó en módulos para mantener un código limpio y escalable:

app.py → Punto de entrada de la aplicación. Registra los routers de candidatos, votantes y votos.

db.py → Configuración de la conexión a la base de datos y creación de la sesión.

models/ → Contiene los modelos de SQLAlchemy:

candidate.py

voter.py

vote.py

schemas/ → Contiene los modelos de Pydantic para validación:

candidate.py

voter.py

vote.py

routers/ → Define los endpoints de la API:

candidates.py

voters.py

votes.py

3. Funcionalidades Implementadas
3.1. Gestión de Candidatos
POST /candidates → Registrar un nuevo candidato.

GET /candidates → Listar todos los candidatos.

GET /candidates/{id} → Obtener un candidato por ID.

DELETE /candidates/{id} → Eliminar un candidato.

Validaciones implementadas:

No se permite registrar dos candidatos con el mismo nombre.

No se permite registrar un candidato cuyo nombre ya exista en la tabla de votantes.

3.2. Gestión de Votantes
POST /voters → Registrar un nuevo votante.

GET /voters → Listar todos los votantes.

GET /voters/{id} → Obtener un votante por ID.

DELETE /voters/{id} → Eliminar un votante.

Validaciones implementadas:

No se permite registrar dos votantes con el mismo correo electrónico.

No se permite registrar un votante cuyo nombre ya exista en la tabla de candidatos.

3.3. Emisión de Votos
POST /votes → Emitir un voto.

GET /votes → Listar todos los votos.

GET /votes/statistics → Estadísticas generales de votación.

Validaciones implementadas:

Un votante solo puede votar una vez (has_voted).

Un votante no puede votarse a sí mismo si también es candidato.

Se actualiza automáticamente el contador de votos del candidato.

3.4. Reportes Avanzados
Se implementaron endpoints adicionales para enriquecer el análisis de resultados:

GET /votes/top3 → Top 3 candidatos más votados.

GET /votes/participation → Porcentaje de participación de votantes.

GET /votes/winner → Candidato ganador actual.

GET /votes/by_party → Distribución de votos por partido político.

4. Consultas SQL de Verificación
Además de los endpoints, se realizaron consultas SQL directas para validar la integridad de los datos:

Votante y candidato al que votó

SELECT v.name AS VoterName, c.name AS CandidateName
FROM Votes vt
JOIN Voters v ON vt.voter_id = v.id
JOIN Candidates c ON vt.candidate_id = c.id;
Conteo de votos por candidato

SELECT c.name, COUNT(vt.id) AS TotalVotes
FROM Candidates c
LEFT JOIN Votes vt ON c.id = vt.candidate_id
GROUP BY c.name;
Participación de votantes

SELECT name, has_voted FROM Voters;
Distribución de votos por partido

SELECT c.party, COUNT(vt.id) AS VotesByParty
FROM Candidates c
LEFT JOIN Votes vt ON c.id = vt.candidate_id
GROUP BY c.party;
Totales acumulados por candidato

SELECT v.name AS VoterName, c.name AS CandidateName,
       (SELECT COUNT(*) FROM Votes vt2 WHERE vt2.candidate_id = c.id) AS CandidateTotalVotes
FROM Votes vt
JOIN Voters v ON vt.voter_id = v.id
JOIN Candidates c ON vt.candidate_id = c.id;
5. Herramientas Utilizadas
Lenguaje: Python 3.13

Framework: FastAPI

ORM: SQLAlchemy

Base de datos: SQL Server (conexión vía PyODBC)

Validación de datos: Pydantic (con EmailStr y validaciones cruzadas)

Configuración: Python-dotenv para manejo de variables de entorno

Servidor de desarrollo: Uvicorn

6. Conclusiones
El sistema de votaciones desarrollado cumple con los siguientes objetivos:

Garantiza la integridad de los datos mediante validaciones cruzadas.

Permite registrar, consultar y eliminar candidatos y votantes.

Asegura que cada votante emita un único voto y no pueda votarse a sí mismo.

Proporciona reportes avanzados de resultados y participación.

Se conecta de manera confiable a SQL Server y persiste la información correctamente.

En conjunto, se logró un sistema robusto, escalable y seguro, que refleja buenas prácticas de desarrollo backend y diseño de APIs.

1. Visualización del API en Swagger
En la Figura 1 se observa la interfaz de Swagger UI, donde se listan todos los endpoints implementados. Esto confirma que la API está completamente funcional y documentada automáticamente.
<img width="921" height="488" alt="image" src="https://github.com/user-attachments/assets/65e8db09-ccd3-4c08-9a59-f16aa0e0e60a" />

2. Registro de Candidatos
En la Figura 2 se muestra el uso del endpoint POST /candidates, donde se registra un nuevo candidato exitosamente. La respuesta confirma la creación del registro en la base de datos.
<img width="921" height="489" alt="image" src="https://github.com/user-attachments/assets/7eab62e3-c343-4e11-a061-f13c1ed34689" />

3. Validación de duplicados en Candidatos
En la Figura 3 se evidencia que, al intentar registrar nuevamente el mismo candidato, el sistema devuelve la alerta: “El candidato ya está registrado”. Esto demuestra la validación de unicidad implementada.

<img width="921" height="489" alt="image" src="https://github.com/user-attachments/assets/7eab62e3-c343-4e11-a061-f13c1ed34689" />

4. Tabla de Candidatos
La Figura 4 presenta la consulta directa a la tabla Candidates, donde se reflejan los registros creados desde la API. Esto confirma la persistencia de los datos en la base de datos.

<img width="921" height="486" alt="image" src="https://github.com/user-attachments/assets/4d70cc69-2c35-4562-9eb1-d98c89fa6168" />

5. Tabla de Votantes
En la Figura 5 se visualiza la tabla Voters, mostrando los registros creados mediante el endpoint correspondiente. Aquí se evidencia la correcta inserción de votantes en la base de datos.

<img width="921" height="488" alt="image" src="https://github.com/user-attachments/assets/16ae4aa2-ee89-4cb7-bb48-982a1ce27303" />

6. Registro de Votantes
La Figura 6 muestra el uso del endpoint POST /voters, donde se agrega un nuevo votante exitosamente. La respuesta confirma la creación del registro.

<img width="921" height="489" alt="image" src="https://github.com/user-attachments/assets/9267e8cd-077a-452a-b112-f48b2c729e25" />

7. Eliminación de Candidatos
En la Figura 7 se ejecuta el endpoint DELETE /candidates/{id}, mostrando el mensaje: “Candidato eliminado correctamente”. Esto valida que la eliminación funciona de manera adecuada.

<img width="921" height="489" alt="image" src="https://github.com/user-attachments/assets/9f1643d3-72f6-4a49-b420-54fa2a1a019d" />

8. Validación cruzada en Votantes
En la Figura 8 se observa que, al intentar registrar un votante con un nombre ya existente en la tabla de candidatos, el sistema devuelve la alerta: “El nombre ya está registrado como candidato”. Esto confirma la validación cruzada entre tablas.

<img width="921" height="488" alt="image" src="https://github.com/user-attachments/assets/336fc192-69a6-42f8-afda-2d8fc7429fba" />

9. Registro de Votos
La Figura 9 evidencia el funcionamiento del endpoint POST /votes, donde un votante emite su voto hacia un candidato. La respuesta confirma la inserción en la tabla de votos.

<img width="921" height="486" alt="image" src="https://github.com/user-attachments/assets/a115d540-7246-451b-b020-17896b162b78" />

10. Validación de voto único
En la Figura 10 se muestra que, al intentar que un votante emita un segundo voto, el sistema devuelve la alerta: “El votante ya emitió su voto”. Esto garantiza la integridad del proceso electoral.

<img width="921" height="487" alt="image" src="https://github.com/user-attachments/assets/4d3fecc5-f572-4a57-a340-a967c2e6719f" />

11. Tabla de Votos
La Figura 11 presenta la consulta directa a la tabla Votes, donde se reflejan los registros de votos emitidos. Esto confirma la persistencia de los votos en la base de datos.

<img width="921" height="488" alt="image" src="https://github.com/user-attachments/assets/d1ec4a89-80ac-480e-9c93-6d2c27ef04bb" />

12. Consultas SQL de verificación
En las Figuras 12 a 16 se muestran diversas consultas SQL que validan la correcta conexión y consistencia de los datos:

Listado de votantes con el candidato al que votaron.

Conteo de votos por candidato.

Participación de votantes.

Distribución de votos por partido.

Totales acumulados por candidato.

Estas consultas permiten comprobar la integridad de la información y la correcta relación entre las tablas.

<img width="921" height="488" alt="image" src="https://github.com/user-attachments/assets/e169fd0d-4f0d-4812-969c-99f9208e8395" />
<img width="921" height="620" alt="image" src="https://github.com/user-attachments/assets/c3c4fb00-399d-403d-8ef2-8d1624fe0c1a" />
<img width="921" height="617" alt="image" src="https://github.com/user-attachments/assets/5f0491c4-bf97-486c-b382-eb14186eb931" />
<img width="921" height="622" alt="image" src="https://github.com/user-attachments/assets/fbb39ba1-4883-46d4-b74f-e8822cde7483" />




