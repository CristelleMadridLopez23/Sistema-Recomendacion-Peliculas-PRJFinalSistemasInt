from django.shortcuts import render
from .logica.motor_ia import motor  # Importamos tu nuevo Motor de IA

def formulario(request):
    if request.method == "POST":
        # 1. Obtener datos del formulario
        mood = request.POST.get("mood")
        clima = request.POST.get("clima")
        duracion = request.POST.get("duracion")

        # 2. Consultar al Motor de IA
        # El motor usará el Árbol de Decisión para predecir el género ideal
        resultado_exacto = motor.recomendar(mood, clima, duracion)

        # 3. Lógica de Fallback (Si la IA no encuentra peli exacta)
        if not resultado_exacto:
            resultado_relax = motor.obtener_recomendacion_relax(mood)
        else:
            resultado_relax = None

        # 4. Renderizar resultados
        return render(request, "resultados.html", {
            "resultado_exacto": resultado_exacto,
            "resultado_relax": resultado_relax,
            "mood": mood,
            "clima": clima,
            "duracion": duracion,
        })

    return render(request, "formulario.html")

def home(request):
    return render(request, "home.html")