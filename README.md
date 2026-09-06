# SecretVault-KMS: Simulador Local de Gestión de Claves con AES-256-GCM

Este proyecto consiste en un simulador local de un Servicio de Administración de Claves (KMS) que implementa estándares criptográficos avanzados y políticas automatizadas de rotación de secretos, todo empaquetado de forma segura dentro de un contenedor aislado.

## Características de Seguridad Implementadas

- **Cifrado Simétrico Militar:** Uso del estándar AES-256 para la máxima protección de datos.
- **Cifrado Autenticado (GCM):** Implementación del modo _Galois/Counter Mode_ que genera etiquetas de autenticación (_Auth Tags_) para asegurar la integridad de la información y prevenir ataques de manipulación de datos en tránsito.
- **Vectores de Inicialización Únicos (Nonce):** Uso de valores aleatorios de 12 bytes por cada operación para evitar patrones criptográficos.
- **Rotación Automática Temporal:** Mecanismo activo que expira las claves maestras cada 30 segundos, generando una nueva clave de forma automática.
- **Retrocompatibilidad Criptográfica:** El almacén mantiene un historial de llaves permitiendo descifrar paquetes antiguos aunque la clave maestra activa ya haya rotado.

## Arquitectura y Contenedorización

Para garantizar el aislamiento y la portabilidad del sistema, el entorno criptográfico fue contenedorizado utilizando **Docker** basándose en una imagen segura y minimalista (`python:3.11-alpine`), reduciendo la superficie de ataque del sistema operativo.
