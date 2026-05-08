from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from typing import List

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
from flask import Flask, flash, redirect, render_template, request, send_file, url_for
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "reporte-secret")


@dataclass
class Question:
    numero: int
    texto: str


QUESTIONS: List[Question] = [
    Question(1, "Limpieza, colocación o sustitución de filtros de aire (colocar de tipo metálicos lavables)"),
    Question(2, "Lavado y peinado de serpentín evaporador (con productos biodegradables)"),
    Question(3, "Lavado de charolas de condensado"),
    Question(4, "Pruebas de funcionamiento de bomba de condesado (en caso de que se cuenten)"),
    Question(5, "Lavado de turbinas"),
    Question(6, "Lubricación de motores"),
    Question(7, "Lubricación de chumaceras y flechas (en caso de que se cuente)"),
    Question(8, "Pruebas de funcionamiento de válvula de dos vías, tres vías o solenoide"),
    Question(9, "Prueba funcionamiento de termostato"),
    Question(10, "Pruebas funcionamiento de cajas de volumen de aire (en caso de que se cuente)"),
    Question(11, "Revisión del correcto estado de ductos rígidos y flexibles"),
    Question(12, "Revisión de soportaría de equipo y tuberías (eléctricas, agua helada o refrigerante)"),
    Question(13, "Revisión de soportaría difusores y rejillas de aire"),
    Question(14, "Limpieza de gabinete interno y externo del equipo"),
    Question(15, "Limpieza de difusores de inyección de aire y rejillas de extracción"),
    Question(16, "Revisión de estado de forro de tubería de agua helada o refrigérate"),
    Question(17, "Reapriete de conexiones eléctricas"),
]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        template_file = request.files.get("template")
        if not template_file or template_file.filename == "":
            flash("Debes subir el archivo Word con el formato del cliente.")
            return redirect(url_for("index"))

        with tempfile.TemporaryDirectory() as tmpdir:
            template_path = os.path.join(tmpdir, secure_filename(template_file.filename))
            template_file.save(template_path)
            doc = DocxTemplate(template_path)

            items = []
            for question in QUESTIONS:
                comment = request.form.get(f"comentario_{question.numero}", "").strip()
                photos = []
                for photo in request.files.getlist(f"fotos_{question.numero}"):
                    if not photo or photo.filename == "":
                        continue
                    filename = f"{question.numero}_{secure_filename(photo.filename)}"
                    photo_path = os.path.join(tmpdir, filename)
                    photo.save(photo_path)
                    photos.append(InlineImage(doc, photo_path, width=Inches(2.5)))

                items.append(
                    {
                        "numero": question.numero,
                        "pregunta": question.texto,
                        "comentario": comment,
                        "fotos": photos,
                    }
                )

            lecturas = {
                "amperaje": request.form.get("lectura_amperaje", "").strip(),
                "voltaje": request.form.get("lectura_voltaje", "").strip(),
                "temp_inyeccion_agua": request.form.get("lectura_temp_inyeccion_agua", "").strip(),
                "temp_retorno_agua": request.form.get("lectura_temp_retorno_agua", "").strip(),
                "temp_inyeccion_aire": request.form.get("lectura_temp_inyeccion_aire", "").strip(),
                "temp_retorno_aire": request.form.get("lectura_temp_retorno_aire", "").strip(),
                "temp_area": request.form.get("lectura_temp_area", "").strip(),
            }

            context = {
                "fecha": request.form.get("fecha", "").strip(),
                "area": request.form.get("area", "").strip(),
                "tecnico": request.form.get("tecnico", "").strip(),
                "items": items,
                "lecturas": lecturas,
            }

            doc.render(context)
            output_path = os.path.join(tmpdir, "reporte.docx")
            doc.save(output_path)
            return send_file(output_path, as_attachment=True, download_name="reporte.docx")

    return render_template("index.html", questions=QUESTIONS)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
