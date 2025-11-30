from django.shortcuts import render
from .logica import reglas
from pyDatalog import pyDatalog

def formulario(request):

    # Inicializa hechos + reglas (solo 1 vez)
    reglas.inicializar_reglas()

    if request.method == "POST":
        mood = request.POST.get("mood")
        clima = request.POST.get("clima")
        duracion = request.POST.get("duracion")

        print("=== DEBUG ===")
        print("Mood:", mood)
        print("Clima:", clima)
        print("Duración:", duracion)

        # Consulta EXACTA
        resultado_exacto = pyDatalog.ask(
            f"Recomendar(t, g, d, '{mood}', '{clima}', '{duracion}')"
        )

        print("Resultado Exacto:", resultado_exacto)

        # Si no hay coincidencias exactas → consultar modo relax
        if not resultado_exacto:
            resultado_relax = pyDatalog.ask(
                f"RecomendarRelax(t, g, d, '{mood}')"
            )
            print("Resultado Relax:", resultado_relax)
        else:
            resultado_relax = None

        return render(request, "recomendador/resultados.html", {
            "resultado_exacto": resultado_exacto,
            "resultado_relax": resultado_relax,
            "mood": mood,
            "clima": clima,
            "duracion": duracion,
        })

    return render(request, "recomendador/formulario.html")
