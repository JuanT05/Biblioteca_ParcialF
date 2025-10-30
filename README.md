# 📚 Sistema de Gestión de Biblioteca

## 📝 Descripción
Este proyecto es una **API REST** desarrollada con **FastAPI** y **SQLModel** para gestionar el catálogo de **autores** y **libros** de una biblioteca.  
Permite registrar, consultar, actualizar y eliminar tanto autores como libros, manejando relaciones y validaciones.

---

## 🚀 Tecnologías utilizadas
- **Python 3.12**
- **FastAPI**
- **SQLModel**
- **Uvicorn**
- **Pydantic**
- **SQLite** (base de datos por defecto)

---

## ⚙️ Instalación y ejecución

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/Biblioteca_Parcial.git
cd Biblioteca_Parcial
```

### 2️⃣ Crear un entorno virtual
```bash
python -m venv venv
```

### 3️⃣ Activar el entorno virtual
- En **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- En **Linux/Mac**:
  ```bash
  source venv/bin/activate
  ```

### 4️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5️⃣ Ejecutar el servidor
```bash
uvicorn main:app --reload
```

### 6️⃣ Abrir la documentación interactiva
- Swagger UI: 👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: 👉 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧩 Estructura del proyecto
```
Biblioteca_Parcial/
│
├── main.py                # Punto de entrada de la aplicación
├── database.py            # Conexión y configuración de la base de datos
├── models.py              # Modelos SQLModel (Autor, Libro)
├── schemas.py             # Esquemas Pydantic (validaciones)
├── crud.py                # Funciones CRUD
├── routes/
│   ├── autores.py         # Endpoints para autores
│   └── libros.py          # Endpoints para libros
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Este archivo
```

---

## 📡 Endpoints principales

### 👨‍💼 Autores
| Método | Ruta | Descripción |
|--------|------|--------------|
| POST | `/autores/` | Crear autor |
| GET | `/autores/` | Listar autores (con filtro por país) |
| GET | `/autores/{autor_id}` | Obtener autor y sus libros |
| PUT | `/autores/{autor_id}` | Actualizar autor |
| DELETE | `/autores/{autor_id}` | Eliminar autor (y verificar qué pasa con sus libros) |

### 📘 Libros
| Método | Ruta | Descripción |
|--------|------|--------------|
| POST | `/libros/` | Crear libro (con autores) |
| GET | `/libros/` | Listar libros (con filtro por año) |
| GET | `/libros/{libro_id}` | Obtener libro y sus autores |
| PUT | `/libros/{libro_id}` | Actualizar libro |
| DELETE | `/libros/{libro_id}` | Eliminar libro |

---

## 🧠 Lógica de negocio implementada
- **ISBN único:** no pueden existir libros duplicados con el mismo ISBN.  
- **Validación de copias:** no se permiten valores negativos.  
- **Eliminación en cascada:** si se elimina un autor, se gestionan sus libros relacionados.

---

## ✅ Estado del proyecto
- CRUD funcional para autores y libros  
- Relación entre autores y libros establecida  
- Swagger operativo  
- Faltan filtros y validaciones avanzadas  

---

## 👨‍💻 Autor
**Juan Tarazona**  
Universidad Católica de Colombia  
Ingeniería de Sistemas  
