# 🏗️ ARCON - Sistema de Registro y Certificación de Arquitectos

![Django](https://img.shields.io/badge/Django-5.2.8-green)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-cyan)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange)

## 📋 Tabla de Contenidos
- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Funcionalidades Principales](#-funcionalidades-principales)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Modelos de Datos](#-modelos-de-datos)
- [Flujo de Usuario](#-flujo-de-usuario)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Guía de Uso](#-guía-de-uso)
- [Características Técnicas](#-características-técnicas)

---

## 🎯 Descripción del Proyecto

**ARCON** es un sistema web integral para la **certificación profesional de arquitectos** desarrollado con Django. El sistema automatiza todo el proceso desde el registro inicial hasta la emisión del certificado profesional, pasando por la revisión administrativa y el procesamiento de pagos.

### Objetivo Principal
Digitalizar y automatizar el proceso de certificación profesional de arquitectos, eliminando trámites burocráticos y proporcionando una experiencia de usuario moderna y eficiente.

---

## 🏛️ Arquitectura del Sistema

El sistema sigue el patrón **MTV (Model-Template-View)** de Django y está organizado en aplicaciones modulares:

```
┌─────────────────────────────────────────────┐
│                FRONTEND                     │
│  ┌─────────────┐ ┌─────────────┐ ┌────────┐ │
│  │   Login/    │ │  Dashboard  │ │ Admin  │ │
│  │  Register   │ │             │ │ Panel  │ │
│  └─────────────┘ └─────────────┘ └────────┘ │
└─────────────────────────────────────────────┘
                     │
┌─────────────────────────────────────────────┐
│                BACKEND                      │
│  ┌─────────────┐ ┌─────────────┐ ┌────────┐ │
│  │  Accounts   │ │ Architects  │ │Payments│ │
│  │    App      │ │     App     │ │  App   │ │
│  └─────────────┘ └─────────────┘ └────────┘ │
│  ┌─────────────┐ ┌─────────────┐           │
│  │Notifications│ │  Dashboard  │           │
│  │    App      │ │     App     │           │
│  └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────┘
                     │
┌─────────────────────────────────────────────┐
│               DATABASE                      │
│        SQLite (Desarrollo)                  │
└─────────────────────────────────────────────┘
```

---

## ⚡ Funcionalidades Principales

### 🔐 1. Sistema de Autenticación
- **Registro de usuarios** con validación de email único
- **Login seguro** con manejo de sesiones
- **Logout** con limpieza de sesión
- **Redirección inteligente** post-autenticación

### 👥 2. Gestión de Perfiles de Arquitecto
- **Registro profesional** con datos académicos y laborales
- **Carga de documentos** en formato PDF
- **Edición de perfil** para actualizar información
- **Validaciones** de datos y archivos

### 🔍 3. Sistema de Revisión Administrativa
- **Panel de administración** para revisores
- **Lista de solicitudes pendientes** ordenadas por fecha
- **Proceso de revisión** con estados:
  - ✏️ **Pendiente** - Solicitud recién enviada
  - ✅ **Aprobada** - Solicitud aceptada
  - ❌ **Rechazada** - Solicitud denegada con comentarios
- **Comentarios administrativos** para justificar decisiones

### 💳 4. Sistema de Pagos Simulado
- **Generación automática** de pagos al aprobar solicitudes
- **Formulario completo** de datos de tarjeta de crédito
- **Validaciones de campos** (número de tarjeta, CVV, fecha)
- **Procesamiento simulado** de transacciones
- **Estados de pago**: Pendiente, Procesando, Completado, Fallido

### 📜 5. Generación de Certificados
- **Certificados PDF profesionales** con diseño corporativo
- **Información completa** del arquitecto certificado
- **Números únicos** de certificación
- **Descarga inmediata** tras completar el pago
- **Firmas digitales simuladas** de autoridades

### 🔔 6. Sistema de Notificaciones
- **Notificaciones automáticas** por cambio de estado
- **Mensajes personalizados** según el tipo de evento
- **Estado de lectura** con contador de no leídas
- **Timeline** de actividad del usuario

### 📊 7. Dashboard Interactivo
- **Resumen del estado** de la solicitud
- **Métricas visuales** de evaluación
- **Accesos rápidos** a funciones principales
- **Historial de actividad** del usuario

---

## 📁 Estructura del Proyecto

```
Proyecto_final/
├── 📁 architect_system/           # Configuración principal
│   ├── settings.py               # Configuración Django
│   ├── urls.py                   # URLs principales
│   ├── wsgi.py                   # Configuración WSGI
│   └── asgi.py                   # Configuración ASGI
│
├── 📁 app/                       # Aplicaciones del proyecto
│   ├── 📁 accounts/              # Autenticación de usuarios
│   │   ├── models.py             # (Usa User de Django)
│   │   ├── views.py              # Login, registro, logout
│   │   ├── forms.py              # Formularios de auth
│   │   ├── urls.py               # Rutas de autenticación
│   │   └── 📁 templates/         # Templates de auth
│   │       ├── login.html
│   │       └── register.html
│   │
│   ├── 📁 architects/            # Gestión de arquitectos
│   │   ├── models.py             # Architect, ApplicationReview
│   │   ├── views.py              # CRUD de perfiles
│   │   ├── forms.py              # Formularios de registro
│   │   ├── urls.py               # Rutas de arquitectos
│   │   └── 📁 templates/
│   │       ├── review_applications.html
│   │       └── process_review.html
│   │
│   ├── 📁 payments/              # Sistema de pagos
│   │   ├── models.py             # Payment
│   │   ├── views.py              # Procesamiento de pagos
│   │   ├── forms.py              # Formulario de pago
│   │   ├── urls.py               # Rutas de pagos
│   │   └── 📁 templates/
│   │       ├── payment_list.html
│   │       ├── payment_detail.html
│   │       └── payment_process.html
│   │
│   ├── 📁 notifications/         # Sistema de notificaciones
│   │   ├── models.py             # Notification
│   │   ├── views.py              # Lista y marcado
│   │   ├── urls.py               # Rutas de notificaciones
│   │   └── 📁 templates/
│   │       └── notification_list.html
│   │
│   └── 📁 dashboard/             # Panel principal
│       ├── models.py             # (Sin modelos propios)
│       ├── views.py              # Vista del dashboard
│       ├── urls.py               # Ruta del dashboard
│       └── 📁 templates/
│           └── dashboard.html
│
├── 📁 templates/                 # Templates globales
│   ├── base.html                 # Template base principal
│   ├── auth_base.html            # Template base para auth
│   ├── dashboard.html            # Dashboard principal
│   ├── register_architect.html   # Registro de arquitecto
│   └── 📁 partials/              # Componentes reutilizables
│       ├── header.html
│       └── sidebar.html
│
├── 📁 static/                    # Archivos estáticos
│   ├── 📁 css/
│   │   └── styles.css
│   └── 📁 js/
│
├── 📁 media/                     # Archivos subidos
│   └── 📁 documents/             # PDFs de arquitectos
│
├── manage.py                     # Comando Django
├── db.sqlite3                    # Base de datos
└── requirements.txt              # Dependencias Python
```

---

## 💾 Modelos de Datos

### 👤 User (Django Built-in)
```python
# Modelo de usuario estándar de Django
- id: AutoField
- username: CharField
- email: EmailField  
- password: CharField
- first_name: CharField
- last_name: CharField
- date_joined: DateTimeField
```

### 🏗️ Architect
```python
# Perfil profesional del arquitecto
class Architect(models.Model):
    user = OneToOneField(User)              # Relación 1:1 con User
    full_name = CharField(max_length=255)   # Nombre completo
    registration_number = CharField()       # Número de colegiado
    qualification = CharField()             # Título profesional
    institution = CharField()               # Universidad de egreso
    graduation_year = PositiveIntegerField  # Año de graduación
    document = FileField()                  # PDF de títulos
    status = CharField(choices=STATUS_CHOICES) # Estado actual
    created_at = DateTimeField(auto_now_add=True)
    
    # Campos de certificación
    is_certified = BooleanField(default=False)
    certificate_number = CharField()
    certification_date = DateField()
    renewal_date = DateField()

# Estados posibles:
STATUS_CHOICES = [
    ('review', 'En revisión'),
    ('approved', 'Aprobado'),
    ('rejected', 'Rechazado'), 
    ('pending_payment', 'Pendiente de pago'),
    ('certified', 'Certificado')
]
```

### 📋 ApplicationReview
```python
# Proceso de revisión administrativa
class ApplicationReview(models.Model):
    architect = OneToOneField(Architect)    # Relación 1:1
    status = CharField(choices=STATUS_CHOICES)
    comments = TextField()                  # Observaciones del revisor
    reviewed_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

# Estados de revisión:
STATUS_CHOICES = [
    ('pending', 'Pendiente'),
    ('approved', 'Aprobado'),
    ('rejected', 'Rechazado')
]
```

### 💳 Payment
```python
# Registro de transacciones de pago
class Payment(models.Model):
    architect = ForeignKey(Architect)       # Relación N:1
    amount = DecimalField(max_digits=10, decimal_places=2)
    description = CharField()               # Concepto del pago
    status = CharField(choices=STATUS_CHOICES)
    transaction_id = CharField()            # ID único de transacción
    paid_at = DateTimeField()              # Fecha de pago
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

# Estados de pago:
STATUS_CHOICES = [
    ('pending', 'Pendiente'),
    ('processing', 'Procesando'),
    ('completed', 'Completado'),
    ('failed', 'Fallido')
]
```

### 🔔 Notification
```python
# Sistema de notificaciones
class Notification(models.Model):
    user = ForeignKey(User)                 # Relación N:1
    title = CharField()                     # Título de la notificación
    message = TextField()                   # Contenido del mensaje
    is_read = BooleanField(default=False)   # Estado de lectura
    created_at = DateTimeField(auto_now_add=True)
```

---

## 🔄 Flujo de Usuario

### 📝 1. Registro e Inicio de Sesión
```
Usuario nuevo → Registro → Confirmación → Login → Dashboard
                    ↓
              Validación email único
              Validación contraseña
```

### 🏗️ 2. Solicitud de Certificación
```
Dashboard → Registro Profesional → Subir Documentos → Enviar Solicitud
    ↓              ↓                    ↓               ↓
Formulario → Validación datos → Validación PDF → Estado: "En revisión"
                                                        ↓
                                                  Notificación automática
```

### 👨‍💼 3. Proceso Administrativo
```
Admin Panel → Lista de Solicitudes → Revisar Documentos → Decisión
     ↓               ↓                     ↓               ↓
Vista admin → Filtros por estado → Download PDF → Aprobar/Rechazar
                                                        ↓
                                                  Notificación al usuario
                                                        ↓
                                              Si aprobada: Generar pago
```

### 💳 4. Procesamiento de Pago
```
Notificación → Sección Pagos → Formulario Pago → Confirmar → Certificado
     ↓             ↓              ↓              ↓          ↓
Estado update → Lista pagos → Datos tarjeta → Simular → Generate PDF
```

### 📜 5. Descarga de Certificado
```
Pago completado → Estado: "Certificado" → Botón descarga → PDF generado
       ↓                    ↓                  ↓            ↓
Notificación → Update perfil → Certificate link → ReportLab PDF
```

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **🐍 Python 3.12** - Lenguaje de programación
- **🎸 Django 5.2.8** - Framework web
- **📁 SQLite** - Base de datos (desarrollo)
- **📄 ReportLab 4.2.5** - Generación de PDFs
- **🖼️ Pillow 10.3.0** - Procesamiento de imágenes

### Frontend
- **🎨 TailwindCSS 3.0** - Framework CSS
- **📱 HTML5** - Estructura semántica
- **⚡ JavaScript (Vanilla)** - Interactividad
- **🧩 Django Templates** - Sistema de plantillas

### Funcionalidades Adicionales
- **📧 Sistema de mensajes de Django** - Notificaciones flash
- **📂 Manejo de archivos** - Upload y validación de PDFs
- **🔐 Autenticación integrada** - Sistema de usuarios de Django
- **🌐 Internacionalización** - Interfaz en español

---

## 🚀 Instalación y Configuración

### Prerrequisitos
```bash
# Python 3.12 o superior
python --version

# pip actualizado
python -m pip install --upgrade pip
```

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd Proyecto_final
```

### 2. Crear Entorno Virtual
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

### 5. Crear Superusuario (Administrador)
```bash
python manage.py createsuperuser
```

### 6. Recolectar Archivos Estáticos
```bash
python manage.py collectstatic
```

### 7. Ejecutar Servidor de Desarrollo
```bash
python manage.py runserver
```

### 8. Acceder a la Aplicación
- **Aplicación principal**: http://localhost:8000
- **Panel de administración**: http://localhost:8000/admin/

---

## 📚 Guía de Uso

### 👤 Para Arquitectos

1. **Registro**:
   - Ir a http://localhost:8000
   - Hacer clic en "Regístrate aquí"
   - Completar email y contraseña
   - Confirmar registro

2. **Completar Perfil**:
   - Ir a "Registro de Arquitecto" en el sidebar
   - Completar todos los campos obligatorios
   - Subir documento PDF (títulos, cédula profesional)
   - Enviar solicitud

3. **Seguimiento**:
   - Revisar notificaciones regularmente
   - Monitorear estado en el dashboard
   - Procesar pago cuando sea aprobado

4. **Certificación**:
   - Completar formulario de pago
   - Descargar certificado una vez procesado

### 👨‍💼 Para Administradores

1. **Acceso Administrativo**:
   - Ir a http://localhost:8000/admin/
   - Login con cuenta de superusuario

2. **Revisión de Solicitudes**:
   - Ir a "Revisión de Solicitudes"
   - Revisar documentos subidos
   - Aprobar o rechazar con comentarios

3. **Gestión de Estados**:
   - Monitorear el flujo de certificación
   - Resolver consultas de usuarios

---

## 🔧 Características Técnicas

### Seguridad
- ✅ **Validación CSRF** en todos los formularios
- ✅ **Validación de archivos** (tipo, tamaño)
- ✅ **Sanitización de inputs** automática por Django
- ✅ **Manejo seguro de archivos** con paths relativos

### Performance
- ✅ **Lazy loading** de relaciones en querysets
- ✅ **Archivos estáticos** optimizados con TailwindCSS
- ✅ **Consultas optimizadas** con select_related
- ✅ **Cache de templates** en producción

### Escalabilidad
- ✅ **Arquitectura modular** por aplicaciones
- ✅ **Modelos relacionales** bien diseñados
- ✅ **Separación de responsabilidades** (MTV)
- ✅ **Fácil migración** a PostgreSQL

### UX/UI
- ✅ **Diseño responsive** con TailwindCSS
- ✅ **Interfaz intuitiva** con navegación clara
- ✅ **Feedback visual** con mensajes flash
- ✅ **Estados de carga** y confirmaciones

### Mantenibilidad
- ✅ **Código bien documentado** con docstrings
- ✅ **Convenciones Django** estándar
- ✅ **Estructura clara** de archivos
- ✅ **Tests preparados** para implementar

---

## 📈 Métricas del Proyecto

| Métrica | Valor |
|---------|-------|
| **Líneas de código Python** | ~1,200 líneas |
| **Templates HTML** | 15 archivos |
| **Modelos de datos** | 4 principales |
| **Vistas implementadas** | 20+ vistas |
| **Formularios** | 6 formularios |
| **URLs definidas** | 25+ rutas |
| **Aplicaciones Django** | 5 apps |
| **Tiempo de desarrollo** | ~40 horas |

---

## 🎓 Aspectos Educativos

Este proyecto demuestra el dominio de:

### Conceptos Fundamentales de Django
- 🎯 **Patrón MTV** (Model-Template-View)
- 🗄️ **ORM de Django** para bases de datos
- 🔄 **Migraciones** automáticas de esquemas
- 🎨 **Sistema de templates** con herencia
- 📝 **Formularios de Django** con validaciones

### Desarrollo Web Fullstack
- 🖥️ **Backend robusto** con Django
- 🎨 **Frontend moderno** con TailwindCSS
- 🗃️ **Modelado de datos** relacional
- 🔐 **Autenticación y autorización**
- 📁 **Manejo de archivos** y uploads

### Buenas Prácticas
- 📚 **Código limpio** y bien documentado
- 🏗️ **Arquitectura modular** y escalable
- 🔒 **Seguridad web** implementada
- 🎯 **UX centrada en el usuario**
- 🧪 **Preparado para testing**

### Integración de Tecnologías
- 🐍 **Python avanzado** con librerías especializadas
- 🎨 **CSS moderno** con framework utility-first
- 📄 **Generación de PDFs** con ReportLab
- 📱 **Diseño responsive** para múltiples dispositivos
- 🔔 **Sistemas de notificaciones** en tiempo real

---

## 🚀 Posibles Mejoras y Extensiones

### Funcionalidades Adicionales
- 🔄 **Sistema de renovación** automática de certificados
- 📊 **Dashboard analítico** para administradores
- 📧 **Notificaciones por email** automáticas
- 🔍 **Búsqueda avanzada** de arquitectos certificados
- 📱 **API REST** para integración móvil

### Mejoras Técnicas
- 🐘 **Migración a PostgreSQL** para producción
- 🚀 **Implementación de cache** con Redis
- 🧪 **Suite de tests completa** (unit, integration)
- 📊 **Logging avanzado** para monitoreo
- 🔐 **Autenticación 2FA** para mayor seguridad

### DevOps y Deployment
- 🐳 **Containerización** con Docker
- ☁️ **Deployment en la nube** (AWS, DigitalOcean)
- 🔄 **CI/CD pipeline** automatizado
- 📈 **Monitoreo de performance** con APM
- 🔒 **HTTPS y certificados SSL** automáticos

---

## 📞 Soporte y Contacto

Para preguntas sobre el proyecto o la implementación:

- 📧 **Email**: [tu-email@ejemplo.com]
- 🐙 **GitHub**: [tu-usuario-github]
- 💼 **LinkedIn**: [tu-perfil-linkedin]

---

## 📄 Licencia

Este proyecto fue desarrollado con fines educativos como parte del programa de Desarrollo Web. 

---

**🎯 Proyecto desarrollado como demostración de competencias en desarrollo web fullstack con Django.**