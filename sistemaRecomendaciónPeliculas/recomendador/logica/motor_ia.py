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
            # 1. Convertir los inputs del usuario a números usando los encoders correspondientes
            # Nota: duracion_input (del form) se compara con tiempo_disponible (del excel)
            mood_cod = self.encoders['estado_animo'].transform([mood_input])[0]
            clima_cod = self.encoders['clima'].transform([clima_input])[0]
            duracion_cod = self.encoders['tiempo_disponible'].transform([duracion_input])[0]

            # 2. Predicción
            genero_predicho_cod = self.modelo.predict([[mood_cod, clima_cod, duracion_cod]])[0]
            genero_predicho = self.encoders['genero'].inverse_transform([genero_predicho_cod])[0]

            print(f"IA Predicción: Para {mood_input}/{clima_input}/{duracion_input} recomienda género: {genero_predicho}")

            # 3. Filtrar resultados
            # Buscamos películas que sean del género predicho Y tengan el tiempo disponible solicitado
            recomendaciones = self.datos[
                (self.datos['genero'] == genero_predicho) & 
                (self.datos['tiempo_disponible'] == duracion_input)
            ]
            
            return recomendaciones.to_dict('records')

        except Exception as e:
            print(f"Error en predicción (posiblemente valor no visto en entrenamiento): {e}")
            return []

    def obtener_recomendacion_relax(self, mood_input):
        # Fallback basado solo en estado_animo
        try:
            recomendaciones = self.datos[self.datos['estado_animo'] == mood_input].sample(frac=1).head(5)
            return recomendaciones.to_dict('records')
        except:
            return []

# Instancia global
motor = RecomendadorIA()