# ✉️ Daemon de Telemetría y Alertas de Mantenimiento (Gmail)

El sistema de alertas automáticas de **AutoCare Pro** es una tarea periódica en segundo plano integrada en el backend, encargada de verificar la telemetría de kilometraje de los coches de todos los usuarios y enviar notificaciones preventivas vía correo electrónico.

---

## 📂 Archivos Involucrados
* `backend/services/alert_scheduler.py` -> Lógica de comparación de kilometrajes y ciclo asíncrono.
* `backend/services/email_services.py` -> Motor de configuración y envío SMTP a través de Gmail.
* `backend/models.py` -> Contiene el modelo de base de datos `ServiceAlert`.

---

## ⚙️ Funcionamiento del Daemon Periódico

Cuando se inicia el backend de FastAPI, el archivo `main.py` dispara una tarea paralela mediante:
```python
asyncio.create_task(start_alert_scheduler())
```
Esta tarea espera **15 segundos** (dando tiempo para que el servidor de base de datos PostgreSQL se estabilice) y luego entra en un bucle infinito que se ejecuta **cada 12 horas** (`await asyncio.sleep(43200)`). En cada ciclo, realiza las siguientes evaluaciones:

```
                  ┌───────────────────────────────┐
                  │ ¿Existe un servicio registrado│
                  │   de este tipo en el coche?   │
                  └───────────────┬───────────────┘
                                  │
                  ┌───────────────┴───────────────┐
                  ▼ SÍ                            ▼ NO
 ┌─────────────────────────────────┐      ┌───────────────────────────────┐
 │ Ultimo_Km = Kilometraje servicio│      │ Ultimo_Km = 0                 │
 │ Proximo_Km = Ultimo_Km +        │      │ Proximo_Km =                  │
 │              tipo.cada_cuantos  │      │   tipo.cada_cuantos_Km        │
 └────────────────┬────────────────┘      └───────────────┬───────────────┘
                  │                                       │
                  └───────────────────┬───────────────────┘
                                      │
                                      ▼
                      ┌───────────────────────────────┐
                      │    Remanente = Proximo_Km -   │
                      │       Coche.kilometraje       │
                      └───────────────┬───────────────┘
                                      │
           ┌──────────────────────────┼──────────────────────────┐
           ▼ Remanente > 1500         ▼ 0 < Remanente <= 1500    ▼ Remanente <= 0
    ┌──────────────┐           ┌──────────────┐           ┌──────────────┐
    │   AL DÍA     │           │   PRÓXIMO    │           │   VENCIDO    │
    │  (Verde)     │           │ (Amarillo)   │           │   (Rojo)     │
    └──────┬───────┘           └──────┬───────┘           └──────┬───────┘
           │                          │                          │
   ┌───────┴──────┐           ┌───────┴──────┐           ┌───────┴──────┐
   │Borrar alerta │           │ Si no existe │           │ Notificar al │
   │previa en DB  │           │ en DB, enviar│           │ instante y   │
   └──────────────┘           │ email + crear│           │ re-notificar │
                              │    alerta    │           │  los Lunes   │
                              └──────────────┘           └──────────────┘
```

---

## 📅 Reglas de Notificación de Alertas

El sistema previene la saturación de correos utilizando la tabla `ServiceAlert` para registrar el estado de los avisos enviados:

### 1. Estado Amarillo (`PRÓXIMO`)
* Se dispara cuando quedan **1.500 km o menos** para llegar al límite de revisión.
* Si el sistema detecta que el servicio está en este rango y **no existe** ningún registro previo de alerta para ese coche y servicio, envía el primer correo electrónico de advertencia y guarda la alerta en la base de datos con el estado `PRÓXIMO`.
* No se enviarán más correos mientras se mantenga en este rango.

### 2. Estado Rojo (`VENCIDO`)
* Se dispara cuando quedan **0 km o menos** (kilometraje del coche igual o superior al límite del servicio).
* **Transición inmediata:** Si el servicio pasa de estar en amarillo (`PRÓXIMO`) a rojo (`VENCIDO`), el sistema lo detecta al instante, envía un nuevo correo de advertencia crítica y actualiza el registro en la base de datos a `VENCIDO`.
* **Notificación Semanal (Lunes):** Si el coche continúa circulando con el servicio vencido y no se registra la intervención, el sistema volverá a enviar un correo de recordatorio **todos los lunes**, siempre y cuando hayan pasado **al menos 6 días** desde el último correo enviado.

### 3. Restablecimiento a Verde (`AL DÍA`)
* En el momento en que el usuario registra en la interfaz la correspondiente intervención (lo que añade una fila a la tabla `Revision` vinculada a ese `tipo_revision_id`), el kilometraje remanente vuelve a ser superior a 1500 km.
* Al ejecutarse el planificador, detecta que el estado volvió a estar `AL DÍA` y **elimina la alerta** de la tabla `ServiceAlert` automáticamente, dejando el ciclo limpio para volver a notificarse en el futuro.

---

## 🎨 Diseño del Correo Electrónico
Los correos electrónicos se envían en formato HTML enriquecido y adoptan la estética brutalista del frontend:
* Estructura centrada con bordes negros gruesos y sombra plana.
* Botón de llamada a la acción ("VER EXPEDIENTE") que redirige de forma directa a la ficha técnica del vehículo correspondiente en la web.
* El recuadro del estado cambia de color a **magenta neón** en caso de que esté vencido (rojo) o **amarillo neón** en caso de estar próximo.
