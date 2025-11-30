from django.shortcuts import render
from .logica import reglas

def formulario(request):

    reglas.inicializar_reglas()

    if request.method == "POST":
        mood = request.POST.get("mood")
        clima = request.POST.get("clima")
        duracion = request.POST.get("duracion")

        resultado_exacto = reglas.recomendar_exacta(mood, clima, duracion)

        if not resultado_exacto:
            resultado_relax = reglas.recomendar_relax(mood)
        else:
            resultado_relax = None

        return render(request, "resultados.html", {
            "resultado_exacto": resultado_exacto,
            "resultado_relax": resultado_relax,
            "mood": mood,
            "clima": clima,
            "duracion": duracion,
        })

    return render(request, "formulario.html")
