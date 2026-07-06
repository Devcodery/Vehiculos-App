import asyncio
from datetime import datetime, timezone
from sqlmodel import Session, select, col
from database import engine
from models import User, Vehicle, Revision, RevisionType, ServiceAlert
from services.email_services import enviar_correo_real

async def check_vehicle_alerts():
    print("[Alert Scheduler] Iniciando comprobación de alertas de mantenimiento...")
    try:
        now = datetime.now(timezone.utc)
        is_monday = now.weekday() == 0  # 0 es Lunes
        
        with Session(engine) as session:
            # 1. Obtener todos los usuarios
            usuarios = session.exec(select(User)).all()
            for user in usuarios:
                # Obtener los vehículos del usuario
                vehiculos = session.exec(select(Vehicle).where(Vehicle.user_id == user.user_id)).all()
                if not vehiculos:
                    continue
                
                # Obtener todos los tipos de revisión
                tipos = session.exec(select(RevisionType)).all()
                if not tipos:
                    continue
                
                # Obtener todas las revisiones del usuario
                vehiculos_matriculas = [v.matricula for v in vehiculos]
                revisiones = session.exec(
                    select(Revision).where(col(Revision.vehiculo_id).in_(vehiculos_matriculas))
                ).all()
                
                for coche in vehiculos:
                    km_actual = coche.kilometraje
                    
                    for tipo in tipos:
                        # Filtrar las revisiones de este coche y este tipo
                        srvs = [r for r in revisiones if r.vehiculo_id == coche.matricula and r.tipo_revision_id == tipo.tipo_revision_id]
                        # Ordenar por kilometraje descendente
                        srvs.sort(key=lambda x: x.kilometro_servicio, reverse=True)
                        
                        ultimo_km = None
                        proximo_km = tipo.cada_cuantos_Km
                        
                        if srvs:
                            ultimo_km = srvs[0].kilometro_servicio
                            proximo_km = ultimo_km + tipo.cada_cuantos_Km
                            
                        km_restantes = proximo_km - km_actual
                        
                        # Determinar estado
                        estado_actual = "AL DÍA"
                        if km_restantes <= 0:
                            estado_actual = "VENCIDO"  # Rojo
                        elif km_restantes <= 1500:
                            estado_actual = "PRÓXIMO"  # Amarillo
                            
                        # Buscar alerta existente en la base de datos
                        alert_statement = select(ServiceAlert).where(
                            ServiceAlert.vehiculo_id == coche.matricula,
                            ServiceAlert.tipo_revision_id == tipo.tipo_revision_id
                        )
                        alert = session.exec(alert_statement).first()
                        
                        if estado_actual == "AL DÍA":
                            # Si ya está al día (por ejemplo, porque hicieron la revisión), borramos cualquier alerta previa
                            if alert:
                                session.delete(alert)
                                session.commit()
                            continue
                            
                        # Si llegamos aquí, el estado es PRÓXIMO o VENCIDO
                        enviar_email = False
                        
                        if not alert:
                            if tipo.tipo_revision_id:
                                # Primera vez que detectamos esta alerta
                                enviar_email = True
                                nueva_alerta = ServiceAlert(
                                    vehiculo_id=coche.matricula,
                                    tipo_revision_id=tipo.tipo_revision_id,
                                    estado=estado_actual,
                                    ultimo_envio=now
                                )
                                session.add(nueva_alerta)
                                session.commit()
                        else:
                            # Ya existía una alerta registrada
                            if alert.estado == "PRÓXIMO" and estado_actual == "VENCIDO":
                                # Subió de amarillo a rojo, notificamos de nuevo
                                enviar_email = True
                                alert.estado = "VENCIDO"
                                alert.ultimo_envio = now
                                session.add(alert)
                                session.commit()
                            elif alert.estado == "VENCIDO" and estado_actual == "VENCIDO":
                                # Sigue en rojo. Si hoy es lunes y ha pasado al menos una semana (6 días), volvemos a enviar
                                if is_monday and (now - alert.ultimo_envio).days >= 6:
                                    enviar_email = True
                                    alert.ultimo_envio = now
                                    session.add(alert)
                                    session.commit()
                                    
                        if enviar_email:
                            asunto = f"ALERTA: Mantenimiento de tu vehículo {coche.marca} {coche.modelo}"
                            color_alert = "#ff3366" if estado_actual == "VENCIDO" else "#ffcc00"
                            text_color = "#ffffff" if estado_actual == "VENCIDO" else "#000000"
                            
                            cuerpo = f"""
                            <html>
                            <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0c0c0c; color: #ffffff; padding: 20px; margin: 0;">
                                <div style="max-width: 600px; margin: 20px auto; background-color: #111111; padding: 30px; border: 4px solid #ff00ff; box-shadow: 12px 12px 0 #000000;">
                                    <h2 style="color: #00e5ff; font-size: 2rem; margin-top: 0; text-transform: uppercase; text-align: center; border-bottom: 2px dashed #ff00ff; padding-bottom: 10px;">
                                        Telemetría de Alerta
                                    </h2>
                                    <p style="font-size: 1.1rem;">Hola, <strong>{user.nombre}</strong></p>
                                    <p>Hemos detectado que el siguiente servicio para tu coche requiere atención inmediata:</p>
                                    
                                    <div style="background-color: {color_alert}; color: {text_color}; padding: 15px; margin: 20px 0; border: 3px solid #000000; font-size: 1.2rem; font-weight: bold; text-align: center; text-transform: uppercase;">
                                        {tipo.nombre}: Estado {estado_actual}
                                    </div>

                                    <table style="width: 100%; border-collapse: collapse; margin: 20px 0; background-color: #000000; border: 2px solid #555;">
                                        <tr>
                                            <td style="padding: 12px; border: 1px solid #333; font-weight: bold; color: #00e5ff;">VEHÍCULO:</td>
                                            <td style="padding: 12px; border: 1px solid #333; color: #fff;">{coche.marca} {coche.modelo} ({coche.matricula})</td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 12px; border: 1px solid #333; font-weight: bold; color: #00e5ff;">KILOMETRAJE ACTUAL:</td>
                                            <td style="padding: 12px; border: 1px solid #333; color: #fff;">{km_actual} km</td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 12px; border: 1px solid #333; font-weight: bold; color: #00e5ff;">LÍMITE MÁXIMO:</td>
                                            <td style="padding: 12px; border: 1px solid #333; color: #fff;">{proximo_km} km</td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 12px; border: 1px solid #333; font-weight: bold; color: #00e5ff;">REMANENTE:</td>
                                            <td style="padding: 12px; border: 1px solid #333; color: #ff3366; font-weight: bold;">{max(0, km_restantes)} km</td>
                                        </tr>
                                    </table>
                                    
                                    <p style="text-align: center; margin-top: 30px;">
                                        <a href="http://localhost:5173/vehiculo/{coche.matricula}" style="background-color: #ff00ff; color: #000000; padding: 12px 30px; font-weight: bold; text-decoration: none; border: 3px solid #000000; display: inline-block;">
                                            VER EXPEDIENTE
                                        </a>
                                    </p>
                                    
                                    <hr style="border: 1px dashed #555; margin: 30px 0;" />
                                    <p style="font-size: 0.8rem; color: #666; text-align: center; margin: 0;">
                                        * Este es un correo automatizado enviado por AutoCare Pro.
                                    </p>
                                </div>
                            </body>
                            </html>
                            """
                            await enviar_correo_real(user.email, user.nombre, asunto, cuerpo)
                            
    except Exception as e:
        print(f"[Alert Scheduler] Error en check_vehicle_alerts: {str(e)}")

async def start_alert_scheduler():
    # Esperamos 15 segundos al iniciar el backend antes de realizar el primer escaneo
    await asyncio.sleep(15)
    while True:
        await check_vehicle_alerts()
        # Repetir el escaneo de telemetría cada 12 horas
        await asyncio.sleep(43200)
