# ===========================================================
#   MOTOR LÓGICO EN PYTHON PURO (SUSTITUYE PYDATALOG)
# ===========================================================

_reglas_cargadas = False

# ---------------------------
# TABLAS / HECHOS
# ---------------------------

MoodGenero = {}         # mood -> [generos]
ClimaGenero = {}        # clima -> [generos]
Contenido = []          # lista de dicts con titulo, genero, duracion


def agregar_mood_genero(mood, genero):
    MoodGenero.setdefault(mood, []).append(genero)


def agregar_clima_genero(clima, genero):
    ClimaGenero.setdefault(clima, []).append(genero)


def agregar_contenido(titulo, genero, duracion):
    Contenido.append({
        "titulo": titulo,
        "genero": genero,
        "duracion": duracion
    })


# ===========================================================
# CARGA DE HECHOS (REEMPLAZO DIRECTO DE PyDatalog)
# ===========================================================

def inicializar_reglas():
    global _reglas_cargadas
    if _reglas_cargadas:
        return

    _reglas_cargadas = True

    # -------------------------------------------------------
    # HECHOS: Mood -> Género
    # -------------------------------------------------------
    agregar_mood_genero('Feliz', 'Comedia')
    agregar_mood_genero('Feliz', 'Animación')
    agregar_mood_genero('Feliz', 'Aventura')

    agregar_mood_genero('Triste', 'Drama')
    agregar_mood_genero('Triste', 'Romance')

    agregar_mood_genero('Motivado', 'Acción')
    agregar_mood_genero('Motivado', 'Fantasia')

    agregar_mood_genero('Estresado', 'Sci-Fi')
    agregar_mood_genero('Estresado', 'Comedia')

    agregar_mood_genero('Aburrido', 'Suspenso')
    agregar_mood_genero('Aburrido', 'Terror')

    # -------------------------------------------------------
    # HECHOS: Clima -> Género
    # -------------------------------------------------------
    agregar_clima_genero('Soleado', 'Comedia')
    agregar_clima_genero('Soleado', 'Aventura')
    agregar_clima_genero('Soleado', 'Animación')

    agregar_clima_genero('Lluvioso', 'Romance')
    agregar_clima_genero('Lluvioso', 'Drama')
    agregar_clima_genero('Lluvioso', 'Suspenso')

    agregar_clima_genero('Nublado', 'Sci-Fi')
    agregar_clima_genero('Nublado', 'Fantasia')
    agregar_clima_genero('Nublado', 'Suspenso')

    agregar_clima_genero('Frio', 'Drama')
    agregar_clima_genero('Frio', 'Terror')
    agregar_clima_genero('Frio', 'Romance')

    agregar_clima_genero('Caluroso', 'Acción')
    agregar_clima_genero('Caluroso', 'Aventura')

    # -------------------------------------------------------
    # HECHOS: Contenido (10 géneros × 5 títulos)
    # -------------------------------------------------------

    # 1. Acción
    agregar_contenido('John Wick', 'Acción', 'Media')
    agregar_contenido('Mad Max: Fury Road', 'Acción', 'Media')
    agregar_contenido('The Dark Knight', 'Acción', 'Larga')
    agregar_contenido('Mission Impossible: Fallout', 'Acción', 'Media')
    agregar_contenido('The Bourne Ultimatum', 'Acción', 'Media')

    # 2. Comedia
    agregar_contenido('The Office', 'Comedia', 'Corta')
    agregar_contenido('Friends', 'Comedia', 'Corta')
    agregar_contenido('Superbad', 'Comedia', 'Media')
    agregar_contenido('The Hangover', 'Comedia', 'Media')
    agregar_contenido('Brooklyn 99', 'Comedia', 'Corta')

    # 3. Drama
    agregar_contenido('The Pursuit of Happyness', 'Drama', 'Media')
    agregar_contenido('The Shawshank Redemption', 'Drama', 'Media')
    agregar_contenido('Breaking Bad', 'Drama', 'Larga')
    agregar_contenido('The Green Mile', 'Drama', 'Larga')
    agregar_contenido('A Beautiful Mind', 'Drama', 'Media')

    # 4. Romance
    agregar_contenido('The Notebook', 'Romance', 'Media')
    agregar_contenido('Your Name', 'Romance', 'Media')
    agregar_contenido('La La Land', 'Romance', 'Media')
    agregar_contenido('Titanic', 'Romance', 'Larga')
    agregar_contenido('Pride & Prejudice', 'Romance', 'Media')

    # 5. Sci-Fi
    agregar_contenido('Interstellar', 'Sci-Fi', 'Larga')
    agregar_contenido('Dark', 'Sci-Fi', 'Larga')
    agregar_contenido('Blade Runner 2049', 'Sci-Fi', 'Larga')
    agregar_contenido('Ex Machina', 'Sci-Fi', 'Media')
    agregar_contenido('The Matrix', 'Sci-Fi', 'Media')

    # 6. Suspenso
    agregar_contenido('Gone Girl', 'Suspenso', 'Media')
    agregar_contenido('Shutter Island', 'Suspenso', 'Media')
    agregar_contenido('Seven', 'Suspenso', 'Media')
    agregar_contenido('Mindhunter', 'Suspenso', 'Larga')
    agregar_contenido('Black Swan', 'Suspenso', 'Media')

    # 7. Aventura
    agregar_contenido('Indiana Jones', 'Aventura', 'Media')
    agregar_contenido('Jumanji', 'Aventura', 'Media')
    agregar_contenido('Harry Potter', 'Aventura', 'Larga')
    agregar_contenido('Jurassic Park', 'Aventura', 'Media')
    agregar_contenido('Pirates of the Caribbean', 'Aventura', 'Media')

    # 8. Fantasia
    agregar_contenido('The Lord of the Rings', 'Fantasia', 'Larga')
    agregar_contenido('The Witcher', 'Fantasia', 'Larga')
    agregar_contenido('Narnia', 'Fantasia', 'Media')
    agregar_contenido('Shadow and Bone', 'Fantasia', 'Larga')
    agregar_contenido('The Hobbit', 'Fantasia', 'Larga')

    # 9. Terror
    agregar_contenido('The Conjuring', 'Terror', 'Media')
    agregar_contenido('Hereditary', 'Terror', 'Media')
    agregar_contenido('IT', 'Terror', 'Larga')
    agregar_contenido('A Quiet Place', 'Terror', 'Media')
    agregar_contenido('The Haunting of Hill House', 'Terror', 'Larga')

    # 10. Animación
    agregar_contenido('Coco', 'Animación', 'Media')
    agregar_contenido('Spider-Man: Into the Spider-Verse', 'Animación', 'Media')
    agregar_contenido('Toy Story', 'Animación', 'Media')
    agregar_contenido('Shrek', 'Animación', 'Media')
    agregar_contenido('Soul', 'Animación', 'Media')


# ===========================================================
# REGLAS / Funciones de inferencia (Equivalente a PyDatalog)
# ===========================================================

def recomendar_exacta(mood, clima, duracion):
    generos_mood = MoodGenero.get(mood, [])
    generos_clima = ClimaGenero.get(clima, [])

    generos_validos = set(generos_mood) & set(generos_clima)

    recomendaciones = [
        c for c in Contenido
        if c["genero"] in generos_validos and c["duracion"] == duracion
    ]

    return recomendaciones


def recomendar_relax(mood):
    generos_mood = MoodGenero.get(mood, [])

    recomendaciones = [
        c for c in Contenido
        if c["genero"] in generos_mood
    ]

    return recomendaciones
