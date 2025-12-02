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


def agregar_recomendacion(request):
    """
    Formulario para añadir una nueva película/serie al CSV.
    """
    context = {}

    if request.method == "POST":
        titulo = request.POST.get("titulo")
        tipo = request.POST.get("tipo")
        genero = request.POST.get("genero")
        duracion = request.POST.get("duracion")
        estado_animo = request.POST.get("estado_animo")
        clima = request.POST.get("clima")
        tiempo_disponible = request.POST.get("tiempo_disponible")

        ok, msg = motor.agregar_pelicula(titulo, tipo, genero, duracion, estado_animo, clima, tiempo_disponible)
        context["mensaje"] = msg
        context["exito"] = ok

    # Obtener lista actualizada de películas para mostrar en la tabla
    if motor.datos is not None:
        # Ordenamos por ID descendente para ver las últimas agregadas primero
        if 'id' in motor.datos.columns:
            context["lista_peliculas"] = motor.datos.sort_values(by='id', ascending=False).to_dict('records')
        else:
            context["lista_peliculas"] = motor.datos.to_dict('records')
    else:
        context["lista_peliculas"] = []

    return render(request, "agregar.html", context)