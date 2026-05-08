# Reporte de mantenimiento (Word)

Aplicación web en Flask para capturar comentarios y fotos por cada punto del mantenimiento, y generar un archivo Word usando **la plantilla del cliente**.

## Requisitos

- Python 3.10+

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar

```bash
python app.py
```

Abra `http://localhost:8000`.

## Cómo preparar la plantilla del cliente

La plantilla debe ser un `.docx` con etiquetas Jinja2 para que `docxtpl` pueda inyectar datos.

Variables disponibles en la plantilla:

- `{{ fecha }}`
- `{{ area }}`
- `{{ tecnico }}`
- `{{ items }}`: lista de preguntas con estructura:
  - `numero`
  - `pregunta`
  - `comentario`
  - `fotos` (lista de imágenes)
- `{{ lecturas }}` con campos:
  - `amperaje`, `voltaje`, `temp_inyeccion_agua`, `temp_retorno_agua`, `temp_inyeccion_aire`, `temp_retorno_aire`, `temp_area`

### Ejemplo de bloque Jinja2

```
{% for item in items %}
{{ item.numero }}.- {{ item.pregunta }}
Comentario: {{ item.comentario }}
{% if item.fotos %}
Fotos:
{% for foto in item.fotos %}
{{ foto }}
{% endfor %}
{% endif %}
{% endfor %}
```

## Notas

- Puedes subir varias fotos por pregunta.
- El archivo generado se descarga como `reporte.docx`.
