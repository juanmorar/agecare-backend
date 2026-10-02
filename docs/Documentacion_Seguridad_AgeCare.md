__Documentación de Seguridad__

AgeCare — Suite de cuidado de adultos mayores

*Manejo de credenciales, permisos y cifrado \(v1\)*

Fecha: 14 de agosto de 2026

Fuentes: AgeCare\_Especificacion\_Endpoints\_Backend\_v1 \(secciones 2\.2, 2\.7, 16\.2 y endpoints 3\.x\) · agecare\_app/lib/core \(storage, network\)

# 1\. Alcance y fuentes

Este documento consolida en un solo lugar todo lo que la documentación existente de AgeCare dice sobre seguridad — hoy disperso entre la Especificación de Endpoints Backend v1 \(secciones 2\.2, 2\.7 y 16\.2\) y el código de la app Flutter — y deja explícitamente marcado qué queda pendiente de definir\.

Como el backend no tiene código todavía, las secciones 2 a 5 describen la arquitectura de seguridad especificada \(lo que el backend deberá implementar\), no una implementación verificada\. La sección sobre el cliente \(app Flutter\) sí está verificada contra código real\.

__Nota: __igual que con la Guía de Instalación y Despliegue, este documento no reemplaza la Especificación de Endpoints; la reorganiza en un formato de documentación de seguridad dedicado, que es lo que pide el checklist de auditoría\.

# 2\. Autenticación y manejo de credenciales

## 2\.1 Contraseñas

Las contraseñas de los usuarios se almacenan con hash bcrypt o argon2 \(a definir cuál de los dos por el equipo BE\); en ningún caso en texto plano\. El flujo de recuperación envía un token de un solo uso por correo \(POST /auth/password/recovery\) y el restablecimiento \(POST /auth/password/reset\) revoca todas las sesiones activas del usuario, no solo la que originó la solicitud\.

## 2\.2 Tokens de sesión

La autenticación se resuelve con JSON Web Tokens firmados \(HS256/RS256\):

__Token__

__Vigencia__

__Comportamiento__

Access token

30 minutos

Se envía en cada petición como Authorization: Bearer <token>\. Incluye user\_id y los roles del usuario por paciente\.

Refresh token

30 días

Rotatorio \(se emite uno nuevo en cada uso\) y persistido en PostgreSQL, lo que permite revocarlo del lado del servidor\.

## 2\.3 Manejo de credenciales en el cliente \(app Flutter\)

Verificado contra el código de agecare\_app:

- Los tokens se guardan con flutter\_secure\_storage, que usa Keychain en iOS y Keystore en Android \(con encryptedSharedPreferences habilitado explícitamente en Android\) — no se usa SharedPreferences ni almacenamiento plano\.
- ApiClient agrega el header Authorization en cada petición autenticada, salvo en las rutas públicas\.
- Ante un 401, un interceptor intenta renovar el access token una sola vez y reintenta la petición original; si la renovación falla, limpia la sesión local y notifica al resto de la app \(onSessionExpired\)\.
- El único usuario/contraseña que aparece en el código fuente es una credencial de demostración \(demo@agecare\.app / agecare123\), usada exclusivamente por el repositorio Mock cuando USE\_MOCKS=true; no es una credencial real ni se envía a ningún backend\.

# 3\. Autorización y permisos

## 3\.1 Principio de autorización

Cada endpoint valida la autorización contra la membresía del usuario en el paciente \(tabla patient\_members\), a través de una dependencia reutilizable de FastAPI \(get\_patient\_member\(role\_required\)\)\. El principio de separación de roles es: el familiar observa, la cuidadora opera, el médico prescribe y el adulto mayor se comunica\.

## 3\.2 Matriz de permisos por rol

L = lectura, E = escritura, — = sin acceso\.

__Recurso__

__Familiar__

__Cuidadora__

__Médico__

__Adulto mayor__

Perfil del paciente

E \(owner\)

L

L

L

Invitaciones y miembros

E \(owner\)

—

L

—

Vitals \(wearable y series\)

L

L \+ E \(manuales\)

L

L \(propio\)

Umbrales de alerta

E

L

E

—

Plan de medicamentos

L

E

E

—

Registro de dosis \(adherencia\)

L

E

L

—

Observaciones e incidentes

L

E

L

E \(check\-in\)

Documentos médicos

E

E

E

—

Alertas \(ver / atender\)

L \+ E

L \+ E

L

—

Asistente IA

E

E

E

E

Chat del paciente

E

E

L

E

Galería de fotos

E \(publica\)

E \(Premium\)

—

L \+ reacciones

Entretenimiento \(feed\)

L

—

—

L

Tareas del día

L \+ E

E

—

—

SOS

recibe

E

—

E

Marketplace

L \+ contacto

E \(su perfil\)

—

—

## 3\.3 Autorización en el cliente \(app Flutter\)

__Pendiente / brecha abierta: __el control de acceso por rol en la app hoy solo se aplica en la interfaz: MainShell decide qué pestañas mostrar según el rol de la sesión, pero el enrutador \(go\_router\) no valida el rol al hacer redirect, solo valida si hay sesión activa\. Esto significa que, técnicamente, una ruta pensada para un rol podría alcanzarse por deep link estando autenticado con otro rol\. La autorización real sigue viviendo en el backend \(sección 3\.1\), pero se recomienda no depender solo de ocultar botones en el cliente\.

# 4\. Cifrado y protección de datos

__Capa__

__Mecanismo__

En tránsito

TLS 1\.2 o superior en todas las comunicaciones con la API\.

En reposo

Cifrado nativo de Azure Database for PostgreSQL y de Azure Blob Storage\.

Secretos de la aplicación

Azure Key Vault \(claves de API de terceros, cadenas de conexión, credenciales de firma\)\.

Archivos \(documentos médicos\)

Subida y descarga vía URLs firmadas \(SAS\) de Azure Blob Storage; el cliente nunca maneja credenciales de almacenamiento directamente \(ver UploadService en el código de la app\)\.

# 5\. Auditoría y trazabilidad

La especificación exige una bitácora de acceso a datos clínicos: quién consultó qué expediente y cuándo\. Es un requisito de diseño explícito, pero — al no existir código de backend — no hay forma de verificar su implementación real; queda como un punto a confirmar cuando el backend exista\.

# 6\. Retención y eliminación de datos

- Los documentos médicos usan baja lógica al eliminarse: el registro se marca como eliminado y el archivo binario \(blob\) se depura después, según una política de retención \(no se especifica el plazo exacto en la documentación disponible\)\.
- El diseño general contempla borrado lógico y consentimiento por invitación como mecanismo que, según la propia Especificación de Endpoints, "facilita la adaptación" a distintos marcos regulatorios regionales — pero eso es una intención de diseño, no una política de retención/eliminación ya definida y documentada con plazos y alcance\.

# 7\. Brechas y pendientes

Estos puntos se listan aquí agrupados porque son, específicamente, brechas de seguridad y privacidad:

__Pendiente / brecha abierta: __consentimiento y privacidad regional de datos de salud: la Especificación de Endpoints \(16\.2\) y el documento de Funcionalidades \(sección 11, Preguntas abiertas\) coinciden en que este punto está pendiente de definición legal\. No existe hoy ningún endpoint, campo de datos ni flujo de consentimiento explícito — es la brecha de seguridad más importante del proyecto en este momento, porque bloquea el módulo de documentos médicos y el piloto\.

__Pendiente / brecha abierta: __autenticación multifactor \(MFA\): no se menciona en ningún documento\. Dado que la app maneja datos de salud, conviene que el equipo decida explícitamente si la v1 la requiere o si queda para una fase posterior, en vez de dejarlo implícito\.

__Pendiente / brecha abierta: __límites de tasa e idempotencia: no hay especificación de rate limiting ni de idempotencia para endpoints críticos como SOS \(9\.6\) o la ingesta batch de wearable \(5\.1\), donde un envío duplicado podría generar alertas o datos duplicados\.

__Pendiente / brecha abierta: __verificación de modo de build: AppConfig\.useMocks tiene defaultValue: true; si un build de tienda se compila sin pasar \-\-dart\-define=USE\_MOCKS=false explícitamente, la app publicada quedaría en modo demo\. Se recomienda una verificación automatizada en CI que bloquee ese escenario\.

# 8\. Resumen de estado

__Área__

__Estado__

Autenticación \(contraseñas, tokens\)

Especificada con buen nivel de detalle; sin código de backend que verificar todavía\.

Autorización y permisos

Especificada con matriz de permisos clara; brecha conocida en el cliente \(guard de rol solo en UI, C\-05\)\.

Cifrado en tránsito y en reposo

Especificado, apoyado en mecanismos nativos de Azure\.

Auditoría de acceso a datos clínicos

Especificada como requisito; sin implementación que verificar\.

Retención y eliminación de datos

Parcial — hay baja lógica y purga de blobs, pero sin plazos ni alcance documentados\.

Consentimiento y privacidad regional

Pendiente — es la brecha abierta más relevante del proyecto\.
