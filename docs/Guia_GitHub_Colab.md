# Cómo usar este repositorio con Google Colab

> **Colab es donde trabajamos; GitHub es donde guardamos y compartimos.**

## 1. Crear el repositorio del equipo (una sola vez)

1. Un integrante entra a github.com y pulsa **New repository** (pueden copiar la estructura de este ejemplo).
2. Le pone el nombre del proyecto (por ejemplo, `desercion-unaj`) y pulsa **Create repository**.
3. Va a **Settings → Collaborators → Add people** y agrega a sus compañeros.

## 2. Guardar un notebook de Colab en GitHub

1. En Colab: **Archivo → Guardar una copia en GitHub**.
2. La primera vez, pulsen **Authorize**. Si el repositorio es privado, marquen *Incluir repositorios privados*.
3. Elijan:
   - **Repositorio:** el del equipo
   - **Ruta:** por ejemplo `notebooks/02_modelos.ipynb`
   - **Mensaje:** qué cambiaron, por ejemplo "agrego Random Forest y LightGBM"
4. **Aceptar.**

Si guardan con el mismo nombre, GitHub **actualiza** el archivo y conserva la versión anterior en la historia.

## 3. Abrir en Colab un notebook del repositorio

**Archivo → Abrir cuaderno → pestaña GitHub** → escriban su usuario → elijan el notebook.

## 4. Subir otros archivos (datos, PDF, README)

En la página del repositorio: **Add file → Upload files** → arrastren el archivo → **Commit changes**.

Para editar el README: ábranlo en GitHub y pulsen el ícono del **lápiz** ✏️.

## Reglas del equipo

- ✅ **Cada integrante trabaja en su propio notebook.** Si dos editan el mismo a la vez, el último que guarda borra los cambios del otro.
- ✅ Escriban mensajes claros al guardar: así se sabe quién hizo qué.
- ❌ No suban contraseñas ni datos personales identificables.
- ⚠️ GitHub no acepta archivos de más de 100 MB. Si sus datos pesan más, pongan el enlace a la fuente en `data/README.md`.
