# 📌 Conceptos Claves de AWS

Este documento resume algunos de los servicios más importantes de AWS para entender su ecosistema y cómo se utilizan.

## ☁️ EC2 (Elastic Compute Cloud)
**EC2** proporciona servidores virtuales en la nube que permiten ejecutar aplicaciones sin necesidad de administrar hardware físico. Puedes elegir diferentes tipos de instancias según el rendimiento, almacenamiento y memoria que necesites.

🔹 **Casos de uso:** Hosting de aplicaciones web, ejecución de modelos de IA, servidores de bases de datos.

## 📦 S3 (Simple Storage Service)
**S3** es un servicio de almacenamiento de objetos altamente escalable y duradero. Permite almacenar y recuperar cualquier cantidad de datos en la nube.

🔹 **Casos de uso:** Almacenamiento de archivos, backups, hosting de sitios estáticos, datasets para machine learning.

## 🔑 IAM (Identity and Access Management)
**IAM** permite gestionar la autenticación y los permisos dentro de AWS. Define **usuarios, grupos, roles y políticas** para controlar el acceso a los recursos.

🔹 **Mejores prácticas:** Aplicar el principio de **menor privilegio**, usar autenticación multifactor (MFA) y revisar permisos regularmente.

## 🐳 ECS y Fargate (Ejecución de Contenedores)
**ECS (Elastic Container Service)** es un servicio para ejecutar contenedores Docker en AWS. 

**Fargate** es una opción serverless dentro de ECS que permite ejecutar contenedores sin gestionar la infraestructura subyacente.

🔹 **Casos de uso:** Microservicios, aplicaciones escalables, procesamiento de datos en contenedores.

## 🛢️ RDS y PostgreSQL en AWS
**RDS (Relational Database Service)** es un servicio de bases de datos gestionadas que simplifica la administración, escalabilidad y seguridad de bases de datos SQL.

**PostgreSQL en AWS** es una de las opciones más utilizadas dentro de RDS, ofreciendo un sistema relacional potente con soporte para extensiones avanzadas.

🔹 **Casos de uso:** Aplicaciones empresariales, almacenamiento de datos transaccionales, sistemas de reporting.

## ⚡ Lambda (Computación Serverless)
**AWS Lambda** permite ejecutar código sin necesidad de administrar servidores. Solo se paga por el tiempo de ejecución del código.

🔹 **Casos de uso:** Automatización de tareas, procesamiento de eventos, backend sin servidores.

## 🤖 Amazon Bedrock (IA Generativa en AWS)
**Amazon Bedrock** es un servicio que proporciona acceso a modelos de IA generativa de diferentes proveedores sin necesidad de configurar infraestructura compleja. Permite crear aplicaciones con modelos de lenguaje, generación de imágenes y más.

🔹 **Casos de uso:** Chatbots avanzados, generación de contenido, análisis de texto e imágenes.

---

## 📚 Recursos Adicionales
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
