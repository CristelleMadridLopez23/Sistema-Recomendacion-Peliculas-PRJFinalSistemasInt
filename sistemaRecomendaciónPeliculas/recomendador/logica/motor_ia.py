import pandas as pd
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from django.conf import settings

class RecomendadorIA:
    def __init__(self):
        self.modelo = None
        self.datos = None
        self.encoders = {}
        self.cargar_datos_y_entrenar()

    def cargar_datos_y_entrenar(self):
        # 1. Cargar el Excel
        ruta_csv = os.path.join(settings.BASE_DIR, 'recomendador/data/peliculas.csv')
        
        try:
            self.datos = pd.read_csv(ruta_csv)
        except FileNotFoundError:
            print("ERROR: No se encontró el archivo peliculas.csv en recomendador/data/")
            return

        # 2. Preprocesamiento
        # Mapeamos las columnas que usaremos para entrenar
        # estado_animo, clima, tiempo_disponible -> Predecir -> genero
        columnas_cat = ['estado_animo', 'clima', 'tiempo_disponible', 'genero']
        
        df_train = self.datos.copy()
        
        # Creamos los encoders para transformar texto a números
        for col in columnas_cat:
            le = LabelEncoder()
            # Convertimos a string por seguridad y ajustamos el encoder
            df_train[col] = le.fit_transform(df_train[col].astype(str))
            self.encoders[col] = le

        # 3. Entrenamiento del Modelo
        # X = Features (Inputs)
        X = df_train[['estado_animo', 'clima', 'tiempo_disponible']]
        # y = Target (Lo que predecimos)
        y = df_train['genero']

        # Usamos un Árbol de Decisión
        self.modelo = DecisionTreeClassifier(criterion='entropy', max_depth=5)
        self.modelo.fit(X, y)
        print("Modelo de IA entrenado exitosamente con columnas personalizadas.")

    def recomendar(self, mood_input, clima_input, duracion_input):
        if self.modelo is None:
            return []

        try:
            # --- PASO 1: PRIORIDAD A COINCIDENCIAS EXACTAS ---
            # Buscamos películas que coincidan EXACTAMENTE con Mood, Clima y Tiempo.
            # Esto garantiza que si agregaste una peli específica para ese escenario, salga primero.
            coincidencias_exactas = self.datos[
                (self.datos['estado_animo'] == mood_input) & 
                (self.datos['clima'] == clima_input) & 
                (self.datos['tiempo_disponible'] == duracion_input)
            ]

            if not coincidencias_exactas.empty:
                print(f"¡Encontradas {len(coincidencias_exactas)} coincidencias directas!")
                return coincidencias_exactas.to_dict('records')

            # --- PASO 2: PREDICCIÓN DE GÉNERO (FALLBACK) ---
            # Si no hay coincidencia exacta, usamos la IA para predecir qué GÉNERO pega mejor.
            mood_cod = self.encoders['estado_animo'].transform([mood_input])[0]
            clima_cod = self.encoders['clima'].transform([clima_input])[0]
            duracion_cod = self.encoders['tiempo_disponible'].transform([duracion_input])[0]

            # Predicción del género
            genero_predicho_cod = self.modelo.predict([[mood_cod, clima_cod, duracion_cod]])[0]
            genero_predicho = self.encoders['genero'].inverse_transform([genero_predicho_cod])[0]

            print(f"IA Predicción (Fallback): Para {mood_input}/{clima_input} recomienda género: {genero_predicho}")

            # 3. Filtrar resultados por el género predicho
            # Aquí mantenemos el filtro de tiempo, pero relajamos el clima/mood porque ya usamos la IA para "traducirlos" a un género.
            recomendaciones = self.datos[
                (self.datos['genero'] == genero_predicho) & 
                (self.datos['tiempo_disponible'] == duracion_input)
            ]
            
            return recomendaciones.to_dict('records')

        except Exception as e:
            print(f"Error en predicción: {e}")
            # Fallback final: devolver algo aleatorio del mismo mood
            return self.obtener_recomendacion_relax(mood_input)

    def obtener_recomendacion_relax(self, mood_input):
        # Fallback basado solo en estado_animo
        try:
            recomendaciones = self.datos[self.datos['estado_animo'] == mood_input].sample(frac=1).head(5)
            return recomendaciones.to_dict('records')
        except:
            return []
        
    def agregar_pelicula(self, titulo, tipo, genero, duracion, estado_animo, clima, tiempo_disponible):
        """
        Añade una nueva fila al CSV de películas y recarga/reentrena el modelo.
        Devuelve (True, mensaje) o (False, mensaje) en caso de error.
        """
        ruta_csv = os.path.join(settings.BASE_DIR, 'recomendador/data/peliculas.csv')
        # Validaciones básicas
        campos = [titulo, tipo, genero, duracion, estado_animo, clima, tiempo_disponible]
        if any(not str(c).strip() for c in campos):
            return False, "Todos los campos son obligatorios."

        # Evitar duplicados por título (case-insensitive)
        if self.datos is not None and titulo.strip().lower() in (t.lower() for t in self.datos['titulo'].astype(str).values):
            return False, "Ya existe una película/serie con ese título."

        # Escribir en CSV de forma segura
        try:
            import csv
            nueva_fila = {
                "id": (self.datos['id'].max() + 1) if (self.datos is not None and 'id' in self.datos.columns and len(self.datos)>0) else 1,
                "titulo": titulo.strip(),
                "tipo": tipo.strip(),
                "genero": genero.strip(),
                "duracion": duracion.strip(),
                "estado_animo": estado_animo.strip(),
                "clima": clima.strip(),
                "tiempo_disponible": tiempo_disponible.strip()
            }
            # Asegurar que el archivo existe y tiene cabecera
            file_exists = os.path.exists(ruta_csv)
            
            # --- CORRECCIÓN INICIO: Verificar si falta salto de línea al final ---
            if file_exists and os.path.getsize(ruta_csv) > 0:
                with open(ruta_csv, 'rb') as f:
                    f.seek(-1, 2) # Ir al último byte del archivo
                    last = f.read(1)
                
                # Si el último caracter no es un salto de línea, lo agregamos manualmente
                if last != b'\n' and last != b'\r':
                    with open(ruta_csv, 'a', encoding='utf-8') as f:
                        f.write('\n')
            # --- CORRECCIÓN FIN ---

            with open(ruta_csv, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["id","titulo","tipo","genero","duracion","estado_animo","clima","tiempo_disponible"])
                if not file_exists:
                    writer.writeheader()
                writer.writerow(nueva_fila)

            # Recargar datos y reentrenar
            self.cargar_datos_y_entrenar()
            return True, "Registro agregado y modelo recargado."
        except Exception as e:
            return False, f"Error al guardar: {e}"

# Instancia global
motor = RecomendadorIA()