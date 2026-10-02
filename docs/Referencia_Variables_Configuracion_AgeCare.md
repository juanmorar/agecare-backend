__Referencia de Variables de Configuración por Entorno__

AgeCare App \(agecare\_app\) — complemento a la Guía de Instalación y Despliegue

La app no usa archivos \.env: toda su configuración se resuelve con \-\-dart\-define en tiempo de compilación \(ver lib/core/config/app\_config\.dart\)\. Este documento consolida, en un solo lugar, qué valor corresponde a cada entorno — distinguiendo lo que ya está documentado de lo que todavía hay que definir o conseguir\.

# Tabla de valores por entorno

__Variable__

__Demo / Mock__

__Desarrollo__

__Staging__

__Producción__

__USE\_MOCKS__

true

false

false

false

__API\_BASE\_URL__

no aplica

https://api\-dev\.agecare\.app

https://api\-staging\.agecare\.app \(propuesto\)

https://api\.agecare\.app

__SPIKE\_APP\_ID__

no aplica

pendiente de asignar

pendiente de asignar

pendiente de asignar

__USE\_WEARABLE\_SIMULATOR__

true

true \(propuesto\)

false \(propuesto\)

false \(propuesto\)

# Leyenda

__Marca__

__Significado__

Confirmado

Valor tomado literalmente del README, app\_config\.dart o la Especificación de Endpoints\.

Propuesto

Convención sugerida en este documento, siguiendo el patrón de los valores confirmados\. No está en ningún documento fuente y debe validarse con el equipo antes de usarse\.

Pendiente

No existe ningún valor, ni siquiera de ejemplo, en la documentación\. Debe obtenerse de un tercero \(p\. ej\. el panel de Spike\) o definirse por el equipo\.

No aplica

El modo demo no se conecta a servicios externos, por lo que la variable no tiene efecto en ese entorno\.

# Comandos de ejemplo por entorno

## Demo / Mock

flutter run \-\-dart\-define=USE\_MOCKS=true

## Desarrollo

flutter run \\

  \-\-dart\-define=USE\_MOCKS=false \\

  \-\-dart\-define=API\_BASE\_URL=https://api\-dev\.agecare\.app \\

  \-\-dart\-define=SPIKE\_APP\_ID=<pendiente>

## Staging \(propuesto\)

flutter run \\

  \-\-dart\-define=USE\_MOCKS=false \\

  \-\-dart\-define=API\_BASE\_URL=https://api\-staging\.agecare\.app \\

  \-\-dart\-define=SPIKE\_APP\_ID=<pendiente>

## Producción

flutter build appbundle \\

  \-\-dart\-define=USE\_MOCKS=false \\

  \-\-dart\-define=API\_BASE\_URL=https://api\.agecare\.app \\

  \-\-dart\-define=SPIKE\_APP\_ID=<pendiente>

# Qué falta para completar este documento

- Confirmar con el equipo si existirá un entorno de staging separado de desarrollo y, de ser así, su URL real \(hoy es una propuesta por convención, no un valor confirmado\)\.
- Obtener el/los SPIKE\_APP\_ID reales desde el panel de Spike \(https://dashboard\.spikeapi\.com o equivalente\) para desarrollo, staging y producción — hoy no existe ninguno documentado, solo ejemplos ilustrativos en el README \(1234\) y en el docstring de app\_config\.dart \(1000\)\.
- Confirmar si USE\_WEARABLE\_SIMULATOR debe pasar a false automáticamente en staging/producción o si conviene mantenerlo configurable por build, para poder probar sin depender de Spike\.

__Nota: __una vez el equipo confirme la URL de staging y se obtengan los SPIKE\_APP\_ID reales, basta con actualizar la tabla de este documento — no requiere cambios en el código de la app, porque ya lee estos valores por \-\-dart\-define\.
