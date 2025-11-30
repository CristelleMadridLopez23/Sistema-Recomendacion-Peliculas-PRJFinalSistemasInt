from pyDatalog import pyDatalog

# ===========================================================
# DEFINICIÓN DE TÉRMINOS
# ===========================================================
pyDatalog.create_terms('MoodGenero, ClimaGenero, Contenido, Recomendar, RecomendarRelax')
pyDatalog.create_terms('mood, clima, preferencia_duracion, t, g, d')

# Bandera para evitar duplicación
_reglas_cargadas = False


def inicializar_reglas():
    """
    Inicializa todos los HECHOS y las REGLAS en PyDatalog.
    Esta función solo se ejecuta una vez por servidor,
    gracias a la bandera _reglas_cargadas.
    """
    global _reglas_cargadas

    if _reglas_cargadas:
        return  # evita recargar reglas
    _reglas_cargadas = True

    # ===========================================================
    # HECHOS: Mood -> Género
    # ===========================================================
    +MoodGenero('Feliz', 'Comedia')
    +MoodGenero('Feliz', 'Animación')
    +MoodGenero('Feliz', 'Aventura')

    +MoodGenero('Triste', 'Drama')
    +MoodGenero('Triste', 'Romance')

    +MoodGenero('Motivado', 'Acción')
    +MoodGenero('Motivado', 'Fantasia')

    +MoodGenero('Estresado', 'Sci-Fi')
    +MoodGenero('Estresado', 'Comedia')

    +MoodGenero('Aburrido', 'Suspenso')
    +MoodGenero('Aburrido', 'Terror')

    # ===========================================================
    # HECHOS: Clima -> Género
    # ===========================================================
    +ClimaGenero('Soleado', 'Comedia')
    +ClimaGenero('Soleado', 'Aventura')
    +ClimaGenero('Soleado', 'Animación')

    +ClimaGenero('Lluvioso', 'Romance')
    +ClimaGenero('Lluvioso', 'Drama')
    +ClimaGenero('Lluvioso', 'Suspenso')

    +ClimaGenero('Nublado', 'Sci-Fi')
    +ClimaGenero('Nublado', 'Fantasia')
    +ClimaGenero('Nublado', 'Suspenso')

    +ClimaGenero('Frio', 'Drama')
    +ClimaGenero('Frio', 'Terror')
    +ClimaGenero('Frio', 'Romance')

    +ClimaGenero('Caluroso', 'Acción')
    +ClimaGenero('Caluroso', 'Aventura')

    # ===========================================================
    # HECHOS: Contenido (10 géneros × 5 títulos)
    # ===========================================================

    # 1. Acción
    +Contenido('John Wick', 'Acción', 'Media')
    +Contenido('Mad Max: Fury Road', 'Acción', 'Media')
    +Contenido('The Dark Knight', 'Acción', 'Larga')
    +Contenido('Mission Impossible: Fallout', 'Acción', 'Media')
    +Contenido('The Bourne Ultimatum', 'Acción', 'Media')

    # 2. Comedia
    +Contenido('The Office', 'Comedia', 'Corta')
    +Contenido('Friends', 'Comedia', 'Corta')
    +Contenido('Superbad', 'Comedia', 'Media')
    +Contenido('The Hangover', 'Comedia', 'Media')
    +Contenido('Brooklyn 99', 'Comedia', 'Corta')

    # 3. Drama
    +Contenido('The Pursuit of Happyness', 'Drama', 'Media')
    +Contenido('The Shawshank Redemption', 'Drama', 'Media')
    +Contenido('Breaking Bad', 'Drama', 'Larga')
    +Contenido('The Green Mile', 'Drama', 'Larga')
    +Contenido('A Beautiful Mind', 'Drama', 'Media')

    # 4. Romance
    +Contenido('The Notebook', 'Romance', 'Media')
    +Contenido('Your Name', 'Romance', 'Media')
    +Contenido('La La Land', 'Romance', 'Media')
    +Contenido('Titanic', 'Romance', 'Larga')
    +Contenido('Pride & Prejudice', 'Romance', 'Media')

    # 5. Sci-Fi
    +Contenido('Interstellar', 'Sci-Fi', 'Larga')
    +Contenido('Dark', 'Sci-Fi', 'Larga')
    +Contenido('Blade Runner 2049', 'Sci-Fi', 'Larga')
    +Contenido('Ex Machina', 'Sci-Fi', 'Media')
    +Contenido('The Matrix', 'Sci-Fi', 'Media')

    # 6. Suspenso
    +Contenido('Gone Girl', 'Suspenso', 'Media')
    +Contenido('Shutter Island', 'Suspenso', 'Media')
    +Contenido('Seven', 'Suspenso', 'Media')
    +Contenido('Mindhunter', 'Suspenso', 'Larga')
    +Contenido('Black Swan', 'Suspenso', 'Media')

    # 7. Aventura
    +Contenido('Indiana Jones', 'Aventura', 'Media')
    +Contenido('Jumanji', 'Aventura', 'Media')
    +Contenido('Harry Potter', 'Aventura', 'Larga')
    +Contenido('Jurassic Park', 'Aventura', 'Media')
    +Contenido('Pirates of the Caribbean', 'Aventura', 'Media')

    # 8. Fantasia
    +Contenido('The Lord of the Rings', 'Fantasia', 'Larga')
    +Contenido('The Witcher', 'Fantasia', 'Larga')
    +Contenido('Narnia', 'Fantasia', 'Media')
    +Contenido('Shadow and Bone', 'Fantasia', 'Larga')
    +Contenido('The Hobbit', 'Fantasia', 'Larga')

    # 9. Terror
    +Contenido('The Conjuring', 'Terror', 'Media')
    +Contenido('Hereditary', 'Terror', 'Media')
    +Contenido('IT', 'Terror', 'Larga')
    +Contenido('A Quiet Place', 'Terror', 'Media')
    +Contenido('The Haunting of Hill House', 'Terror', 'Larga')

    # 10. Animación
    +Contenido('Coco', 'Animación', 'Media')
    +Contenido('Spider-Man: Into the Spider-Verse', 'Animación', 'Media')
    +Contenido('Toy Story', 'Animación', 'Media')
    +Contenido('Shrek', 'Animación', 'Media')
    +Contenido('Soul', 'Animación', 'Media')

    # ===========================================================
    # REGLAS LÓGICAS
    # ===========================================================

    # Recomendación exacta (match perfecto)
    Recomendar(t, g, d, mood, clima, preferencia_duracion) <= (
        MoodGenero(mood, g) &
        ClimaGenero(clima, g) &
        Contenido(t, g, d) &
        (d == preferencia_duracion)
    )

    # Recomendación relajada (solo mood)
    RecomendarRelax(t, g, d, mood) <= (
        MoodGenero(mood, g) &
        Contenido(t, g, d)
    )
