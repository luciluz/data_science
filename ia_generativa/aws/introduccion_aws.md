# Introducción a AWS

## 🌐 ¿Qué es AWS?
Amazon Web Services (**AWS**) es una plataforma de servicios en la nube que proporciona infraestructura escalable y herramientas para el desarrollo, despliegue y gestión de aplicaciones. AWS permite a empresas y desarrolladores acceder a recursos como servidores, bases de datos, almacenamiento y redes sin necesidad de mantener hardware físico.

AWS opera bajo un modelo de **pago por uso**, lo que significa que solo se paga por los recursos consumidos, optimizando costos en comparación con infraestructuras tradicionales.

## 🌍 Regiones y Zonas de Disponibilidad (AZs)
AWS organiza su infraestructura en **Regiones**, que son áreas geográficas con múltiples centros de datos distribuidos. Dentro de cada región existen **Zonas de Disponibilidad (AZs)**, que son centros de datos físicamente separados pero interconectados.

- **Regiones**: AWS tiene múltiples regiones a nivel global (ejemplo: `us-east-1`, `eu-west-1`).
- **Zonas de Disponibilidad (AZs)**: Cada región tiene al menos dos zonas de disponibilidad para garantizar alta disponibilidad y tolerancia a fallos.

### 🚲 Edge Locations y Amazon CloudFront
AWS también cuenta con **Edge Locations**, que son nodos de distribución de contenido para mejorar la velocidad de entrega de datos mediante **Amazon CloudFront**, su red de entrega de contenido (CDN).

## 👷 IAM (Identity and Access Management)
AWS IAM es el servicio que permite gestionar usuarios, permisos y roles de acceso a los recursos de AWS. Sus principales componentes son:

- **Usuarios IAM**: Cuentas individuales con credenciales de acceso.
- **Grupos IAM**: Conjunto de usuarios con permisos compartidos.
- **Roles IAM**: Permiten otorgar permisos temporales a usuarios o servicios.
- **Políticas IAM**: Definen qué acciones pueden realizar los usuarios sobre los recursos.

> **Mejor práctica**: Usar el principio de **menor privilegio** para limitar accesos innecesarios.

## 💸 Facturación y Precios en AWS
AWS sigue un modelo de **pago por uso**, donde los costos dependen del consumo de recursos. Algunos puntos clave:

- **Facturación por segundo/minuto/hora** dependiendo del servicio.
- **Capas gratuitas**: AWS ofrece ciertos servicios gratis hasta un límite mensual.
- **Herramientas de monitoreo**: Uso de AWS Cost Explorer y AWS Budgets para controlar gastos.

## ⚡ Servicios Principales de AWS
Algunos de los servicios más utilizados en AWS incluyen:

| Categoría        | Servicio              | Descripción                          |
|-----------------|----------------------|--------------------------------------|
| Cómputo        | **EC2**               | Servidores virtuales escalables     |
| Almacenamiento | **S3**                | Almacenamiento de objetos           |
| Bases de Datos | **RDS** / **DynamoDB** | Bases de datos SQL y NoSQL          |
| Seguridad      | **IAM** / **Cognito**  | Control de acceso y autenticación   |
| Redes         | **VPC** / **CloudFront** | Redes privadas y CDN                |
| IA Generativa | **Amazon Bedrock**     | Acceso a modelos de IA generativa   |

AWS es una plataforma poderosa para el desarrollo en la nube, con una arquitectura altamente distribuida y segura. Comprender su estructura y servicios principales facilita la implementación y escalabilidad de aplicaciones.

### 📖 Recursos Adicionales
- [Documentación oficial de AWS](https://docs.aws.amazon.com/)
- [AWS Free Tier](https://aws.amazon.com/free/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
