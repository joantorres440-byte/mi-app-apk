import tkinter as tk
from tkinter import messagebox
import winsound
import math
import pyttsx3

class AppFitnessAvanzada:
    def __init__(self, root):
        self.root = root
        self.root.title("Mi App de Fitness")
        self.root.geometry("500x780")
        self.root.config(bg="#121212")
        
        # --- MOTOR DE VOZ (TTS) ---
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150) # Velocidad de voz
        except:
            self.tts_engine = None

        # --- ESTADOS ---
        self.agua_count = 0
        self.creatina_count = 0
        self.onda_fase = 0.0
        
        self.frases_agua = [
            "¡Buen inicio, cada bote cuenta! 💧",
            "¡Excelente ritmo, sigue hidratándote! 💪",
            "¡Vas a mitad de camino, campeón! 🚀",
            "¡Casi lo logras, excelente trabajo! 🔥",
            "¡Meta de agua cumplida al 100%! 🏆"
        ]
        
        # Desglose de Nutrición por comida
        self.comidas_data = {
            "Desayuno": {"carbs": 0.0, "grasas": 0.0, "protes": 0.0, "cals": 0.0},
            "Comida": {"carbs": 0.0, "grasas": 0.0, "protes": 0.0, "cals": 0.0},
            "Cena": {"carbs": 0.0, "grasas": 0.0, "protes": 0.0, "cals": 0.0}
        }

        self.animacion_agua_id = None

        # Hablar al iniciar la app
        self.root.after(500, self.decir_recordatorio_creatina)

        self.mostrar_inicio()

    def decir_recordatorio_creatina(self):
        texto = "Recuerda tomar tu creatina de la más alta calidad."
        if self.tts_engine:
            try:
                self.tts_engine.say(texto)
                self.tts_engine.runAndWait()
            except:
                pass

    def reproducir_sonido(self):
        try:
            winsound.Beep(1200, 80)
        except:
            pass

    def limpiar_pantalla(self):
        if self.animacion_agua_id:
            self.root.after_cancel(self.animacion_agua_id)
            self.animacion_agua_id = None
        for widget in self.root.winfo_children():
            widget.destroy()

    # ================= PANEL PRINCIPAL =================
    def mostrar_inicio(self):
        self.limpiar_pantalla()
        self.reproducir_sonido()
        
        tk.Label(self.root, text="MI APP DE FITNESS", font=("Arial", 22, "bold"), fg="#bb86fc", bg="#121212").pack(pady=15)
        
        # Tarjeta Creatina
        card_creatina = tk.Frame(self.root, bg="#1e1e1e", bd=2, relief="groove")
        card_creatina.pack(fill="x", padx=30, pady=8)
        tk.Label(card_creatina, text="⚡ Suplementación de Creatina", font=("Arial", 13, "bold"), fg="white", bg="#1e1e1e").pack(anchor="w", padx=15, pady=4)
        tk.Button(card_creatina, text="Ver Bote de Creatina", font=("Arial", 10, "bold"), bg="#bb86fc", fg="black", command=self.mostrar_creatina).pack(anchor="e", padx=15, pady=6)

        # Tarjeta Agua
        card_agua = tk.Frame(self.root, bg="#1e1e1e", bd=2, relief="groove")
        card_agua.pack(fill="x", padx=30, pady=8)
        tk.Label(card_agua, text="💧 Hidratación Diaria", font=("Arial", 13, "bold"), fg="white", bg="#1e1e1e").pack(anchor="w", padx=15, pady=4)
        tk.Button(card_agua, text="Iniciar hidratación", font=("Arial", 10, "bold"), bg="#8a2be2", fg="white", command=self.mostrar_agua).pack(anchor="e", padx=15, pady=6)

        # Tarjeta Ejercicios
        card_ej = tk.Frame(self.root, bg="#1e1e1e", bd=2, relief="groove")
        card_ej.pack(fill="x", padx=30, pady=8)
        tk.Label(card_ej, text="🏋️ Rutina Semanal (Lunes a Sábado)", font=("Arial", 13, "bold"), fg="white", bg="#1e1e1e").pack(anchor="w", padx=15, pady=4)
        tk.Button(card_ej, text="Ver Días de Entrenamiento", font=("Arial", 10), bg="#8a2be2", fg="white", command=self.mostrar_dias_semana).pack(anchor="e", padx=15, pady=6)

        # Tarjeta Comidas
        card_comida = tk.Frame(self.root, bg="#1e1e1e", bd=2, relief="groove")
        card_comida.pack(fill="x", padx=30, pady=8)
        tk.Label(card_comida, text="🥗 Nutrición (Desayuno, Comida, Cena)", font=("Arial", 13, "bold"), fg="white", bg="#1e1e1e").pack(anchor="w", padx=15, pady=4)
        tk.Button(card_comida, text="Registrar Comidas", font=("Arial", 10), bg="#8a2be2", fg="white", command=self.mostrar_menu_comidas).pack(anchor="e", padx=15, pady=6)

    # ================= SECCIÓN CREATINA =================
    def mostrar_creatina(self):
        self.limpiar_pantalla()
        self.reproducir_sonido()
        self.decir_recordatorio_creatina()
        
        tk.Label(self.root, text="⚡ Registro de Creatina", font=("Arial", 16, "bold"), fg="white", bg="#121212").pack(pady=10)
        
        self.canvas_creatina = tk.Canvas(self.root, width=140, height=180, bg="#121212", highlightthickness=0)
        self.canvas_creatina.pack(pady=5)
        self.dibujar_bote_creatina()
        
        self.lbl_creatina_estado = tk.Label(self.root, text=f"Dosis registradas: {self.creatina_count} / 1", font=("Arial", 13, "bold"), fg="#bb86fc", bg="#121212")
        self.lbl_creatina_estado.pack(pady=5)
        
        tk.Button(self.root, text="TOMAR CREATINA", font=("Arial", 11, "bold"), bg="#bb86fc", fg="black", width=22, height=2, command=self.tomar_creatina).pack(pady=10)
        tk.Button(self.root, text="← Volver al inicio", font=("Arial", 10), bg="#333333", fg="white", width=18, command=self.mostrar_inicio).pack(pady=15)

    def dibujar_bote_creatina(self):
        self.canvas_creatina.delete("all")
        # Bote de suplemento
        self.canvas_creatina.create_rectangle(40, 10, 100, 30, fill="#bb86fc", outline="white") # Tapa
        self.canvas_creatina.create_rectangle(30, 30, 110, 160, outline="#bb86fc", width=3) # Envase
        self.canvas_creatina.create_text(70, 70, text="CREATINA", fill="white", font=("Arial", 9, "bold"))
        
        if self.creatina_count > 0:
            # Dibujar nivel del suplemento
            self.canvas_creatina.create_rectangle(32, 90, 108, 158, fill="#03dac6", outline="")

    def tomar_creatina(self):
        self.reproducir_sonido()
        if self.creatina_count == 0:
            self.creatina_count = 1
            self.lbl_creatina_estado.config(text="Dosis registradas: 1 / 1 (¡Completado!)")
            self.dibujar_bote_creatina()
            messagebox.showinfo("Creatina Registrada", "¡Dosis diaria de creatina registrada con éxito!")
        else:
            messagebox.showinfo("Información", "Ya tomaste tu dosis diaria de creatina de hoy.")

    # ================= SECCIÓN AGUA DINÁMICA =================
    def mostrar_agua(self):
        self.limpiar_pantalla()
        self.reproducir_sonido()
        
        tk.Label(self.root, text="💧 Galón de Agua Dinámico", font=("Arial", 16, "bold"), fg="white", bg="#121212").pack(pady=10)
        
        self.canvas = tk.Canvas(self.root, width=150, height=190, bg="#121212", highlightthickness=0)
        self.canvas.pack(pady=5)
        
        self.animar_agua()
        
        self.lbl_agua_estado = tk.Label(self.root, text=f"Botes tomados: {self.agua_count} / 5", font=("Arial", 14, "bold"), fg="#bb86fc", bg="#121212")
        self.lbl_agua_estado.pack(pady=5)
        
        self.lbl_frase = tk.Label(self.root, text="¡Mantente hidratado con agua en movimiento!", font=("Arial", 10, "italic"), fg="#03dac6", bg="#121212", wraplength=400)
        self.lbl_frase.pack(pady=5)
        
        tk.Button(self.root, text="TOMAR UN BOTE (+1)", font=("Arial", 11, "bold"), bg="#8a2be2", fg="white", width=22, height=2, command=self.sumar_agua).pack(pady=10)
        tk.Button(self.root, text="Reiniciar Galón", font=("Arial", 10), bg="#4a154b", fg="white", width=18, command=self.reiniciar_agua).pack(pady=5)
        tk.Button(self.root, text="← Volver al inicio", font=("Arial", 10), bg="#333333", fg="white", width=18, command=self.mostrar_inicio).pack(pady=10)

    def animar_agua(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(60, 10, 90, 25, outline="#8a2be2", width=2)
        self.canvas.create_rectangle(30, 25, 120, 180, outline="#8a2be2", width=3)
        
        if self.agua_count > 0:
            nivel_base = 180 - (self.agua_count * 30)
            puntos = [30, 180]
            for x in range(30, 121, 5):
                y = nivel_base + math.sin(x * 0.08 + self.onda_fase) * 4
                puntos.append(x)
                puntos.append(y)
            puntos.extend([120, 180])
            self.canvas.create_polygon(puntos, fill="#03dac6", outline="")
            
        self.onda_fase += 0.15
        self.animacion_agua_id = self.root.after(80, self.animar_agua)

    def sumar_agua(self):
        self.reproducir_sonido()
        if self.agua_count < 5:
            self.agua_count += 1
            self.lbl_agua_estado.config(text=f"Botes tomados: {self.agua_count} / 5")
            self.lbl_frase.config(text=self.frases_agua[self.agua_count - 1])
        else:
            messagebox.showinfo("¡Meta Completa!", "¡Ya completaste tus 5 botes de agua de hoy!")

    def reiniciar_agua(self):
        self.reproducir_sonido()
        self.agua_count = 0
        self.lbl_agua_estado.config(text=f"Botes tomados: 0 / 5")
        self.lbl_frase.config(text="Galón reiniciado.")

    # ================= SECCIÓN RUTINAS LUNES A SÁBADO =================
    def mostrar_dias_semana(self):
        self.limpiar_pantalla()
        self.reproducir_sonido()
        
        tk.Label(self.root, text="🏋️ Selecciona el Día de la Semana", font=("Arial", 16, "bold"), fg="white", bg="#121212").pack(pady=15)
        
        dias = [
            ("Lunes (Empuje)", "Empuje"),
            ("Martes (Piernas)", "Piernas"),
            ("Miércoles (Tracción & Abdomen)", "Traccion"),
            ("Jueves (Empuje)", "Empuje"),
            ("Viernes (Piernas)", "Piernas"),
            ("Sábado (Tracción & Abdomen)", "Traccion")
        ]
        
        for nombre_dia, tipo in dias:
            tk.Button(self.root, text=nombre_dia, font=("Arial", 10, "bold"), bg="#8a2be2", fg="white", width=36, height=1, command=lambda t=tipo, d=nombre_dia: self.mostrar_ejercicios_dia(d, t)).pack(pady=4)

        tk.Button(self.root, text="← Volver al inicio", font=("Arial", 10), bg="#333333", fg="white", width=18, command=self.mostrar_inicio).pack(pady=15)

    def mostrar_ejercicios_dia(self, dia_texto, tipo):
        self.limpiar_pantalla()
        self.reproducir_sonido()
        
        tk.Label(self.root, text=f"Rutina para: {dia_texto}", font=("Arial", 14, "bold"), fg="#bb86fc", bg="#121212").pack(pady=10)
        tk.Label(self.root, text="Selecciona un ejercicio para registrar sus 3 Sets:", font=("Arial", 9, "italic"), fg="white", bg="#121212").pack(pady=2)

        if tipo == "Empuje":
            ejercicios = ["Press plano banco", "Press inclinado banco", "Press militar máquina", "Aperturas máquina/polea", "Elevaciones laterales", "Jalón tríceps cuerda"]
        elif tipo == "Piernas":
            ejercicios = ["Sentadilla en máquina", "Press de pierna", "Curl piernas (Isquios)", "Extensión piernas", "Elevación pantorrillas"]
        else:
            ejercicios = ["Dominadas", "Jalón al pecho", "Remo sentado cable", "Remo unilateral polea", "Curl barra", "Curl predicador", "Abdomen crunch"]

        for ej in ejercicios:
            tk.Button(self.root, text=f"• {ej}", font=("Arial", 10), bg="#2b093f", fg="white", width=36, anchor="w", command=lambda e=ej: self.mostrar_sets_ejercicio(e, dia_texto, tipo)).pack(pady=3)

        tk.Button(self.root, text="← Volver a los días", font=("Arial", 10), bg="#333333", fg="white", width=18, command=self.mostrar_dias_semana).pack(pady=15)

    def mostrar_sets_ejercicio(self, ejercicio_nombre, dia_texto, tipo):
        self.limpiar_pantalla()
        self.reproducir_sonido()
        
        tk.Label(self.root, text=f"Ejercicio: {ejercicio_nombre}", font=("Arial", 13, "bold"), fg="#bb86fc", bg="#121212").pack(pady=10)
        tk.Label(self.root, text="Ingresa las repeticiones hechas en tus 3 sets:", font=("Arial", 10), fg="white", bg="#121212").pack(pady=5)

        f_sets = tk.Frame(self.root, bg="#121212")
        f_sets.pack(pady=10)
        
        tk.Label(f_sets, text="Set 1 (Reps):", fg="white", bg="#121212").grid(row=0, column=0, padx=5, pady=3)
        self.e_s1 = tk.Entry(f_sets, width=8); self.e_s1.grid(row=0, column=1, padx=5, pady=3); self.e_s1.insert(0, "10")
        
        tk.Label(f_sets, text="Set 2 (Reps):", fg="white", bg="#121212").grid(row=1, column=0, padx=5, pady=3)
        self.e_s2 = tk.Entry(f_sets, width=8); self.e_s2.grid(row=1, column=1, padx=5, pady=3); self.e_s2.insert(0, "10")
        
        tk.Label(f_sets, text="Set 3 (Reps):", fg="white", bg="#121212").grid(row=2, column=0, padx=5, pady=3)
        self.e_s3 = tk.Entry(f_sets, width=8); self.e_s3.grid(row=2, column=1, padx=5, pady=3); self.e_s3.insert(0, "8")

        tk.Button(self.root, text="Guardar Sets y Ver Total", font=("Arial", 10, "bold"), bg="#8a2be2", fg="white", command=self.calcular_total_sets).pack(pady=10)
        
        self.lbl_total_reps = tk.Label(self.root, text="Total acumulado: --", font=("Arial", 11, "bold"), fg="#03dac6", bg="#121212")
        self.lbl_total_reps.pack(pady=5)

        tk.Button(self.root, text="← Volver al día", font=("Arial", 10), bg="#333333", fg="white", width=18, command=lambda: self.mostrar_ejercicios_dia(dia_texto, tipo)).pack(pady=15)

    def calcular_total_sets(self):
        self.reproducir_sonido()
        try:
            r1 = int(self.e_s1.get()); r2 = int(self.e_s2.get()); r3 = int(self.e_s3.get())
            total = r1 + r2 + r3
            self.lbl_total_reps.config(text=f"Total acumulado: {total} repeticiones")
            messagebox.showinfo("Sets Guardados", f"¡Sets registrados! Total: {total} reps.")
        except ValueError:
            messagebox.showerror("Error", "Ingresa números válidos.")

    # ================= SECCIÓN COMIDAS DESGLOSADAS =================
    def mostrar_menu_comidas(self):
        self.limpiar_pantalla()
        self.reproducir_sonido()
        
        tk.Label(self.root, text="🥗 Registro de Nutrición", font=("Arial", 16, "bold"), fg="white", bg="#121212").pack(pady=10)
        
        tk.Button(self.root, text="🍳 1. Registro de Desayuno", font=("Arial", 11, "bold"), bg="#8a2be2", fg="white", width=30, height=2, command=lambda: self.form_comida_especifica("Desayuno")).pack(pady=6)
        tk.Button(self.root, text="🍲 2. Registro de Comida", font=("Arial", 11, "bold"), bg="#8a2be2", fg="white", width=30, height=2, command=lambda: self.form_comida_especifica("Comida")).pack(pady=6)
        tk.Button(self.root, text="🌙 3. Registro de Cena", font=("Arial", 11, "bold"), bg="#8a2be2", fg="white", width=30, height=2, command=lambda: self.form_comida_especifica("Cena")).pack(pady=6)

        # Totales generales acumulados del día
        tot_c = sum(v["carbs"] for v in self.comidas_data.values())
        tot_g = sum(v["grasas"] for v in self.comidas_data.values())
        tot_p = sum(v["protes"] for v in self.comidas_data.values())
        tot_cal = sum(v["cals"] for v in self.comidas_data.values())

        resumen_texto = (
            f"--- TOTAL GENERAL DEL DÍA ---\n"
            f"Carbohidratos: {tot_c} g | Grasas: {tot_g} g\n"
            f"Proteínas: {tot_p} g | Calorías: {tot_cal} kcal"
        )
        tk.Label(self.root, text=resumen_texto, font=("Arial", 10, "bold"), fg="#03dac6", bg="#121212", justify="center").pack(pady=10)

        tk.Button(self.root, text="← Volver al inicio", font=("Arial", 10), bg="#333333", fg="white", width=18, command=self.mostrar_inicio).pack(pady=10)

    def form_comida_especifica(self, nombre_comida):
        self.limpiar_pantalla()
        self.reproducir_sonido()
        
        tk.Label(self.root, text=f"Registro de: {nombre_comida}", font=("Arial", 14, "bold"), fg="#bb86fc", bg="#121212").pack(pady=10)
        
        frame_inputs = tk.Frame(self.root, bg="#121212")
        frame_inputs.pack(pady=5)
        
        datos_actuales = self.comidas_data[nombre_comida]

        tk.Label(frame_inputs, text="Carbohidratos (g):", fg="white", bg="#121212").grid(row=0, column=0, sticky="w", pady=3)
        self.e_c = tk.Entry(frame_inputs, width=10); self.e_c.grid(row=0, column=1, pady=3); self.e_c.insert(0, str(datos_actuales["carbs"]))
        
        tk.Label(frame_inputs, text="Grasas (g):", fg="white", bg="#121212").grid(row=1, column=0, sticky="w", pady=3)
        self.e_g = tk.Entry(frame_inputs, width=10); self.e_g.grid(row=1, column=1, pady=3); self.e_g.insert(0, str(datos_actuales["grasas"]))
        
        tk.Label(frame_inputs, text="Proteínas (g):", fg="white", bg="#121212").grid(row=2, column=0, sticky="w", pady=3)
        self.e_p = tk.Entry(frame_inputs, width=10); self.e_p.grid(row=2, column=1, pady=3); self.e_p.insert(0, str(datos_actuales["protes"]))
        
        tk.Label(frame_inputs, text="Calorías (kcal):", fg="white", bg="#121212").grid(row=3, column=0, sticky="w", pady=3)
        self.e_cal = tk.Entry(frame_inputs, width=10); self.e_cal.grid(row=3, column=1, pady=3); self.e_cal.insert(0, str(datos_actuales["cals"]))
        
        tk.Button(self.root, text=f"Guardar {nombre_comida}", font=("Arial", 10, "bold"), bg="#8a2be2", fg="white", width=22, command=lambda: self.guardar_comida(nombre_comida)).pack(pady=10)
        
        tk.Button(self.root, text="← Volver a Comidas", font=("Arial", 10), bg="#333333", fg="white", width=18, command=self.mostrar_menu_comidas).pack(pady=10)

    def guardar_comida(self, nombre_comida):
        self.reproducir_sonido()
        try:
            c = float(self.e_c.get())
            g = float(self.e_g.get())
            p = float(self.e_p.get())
            cal = float(self.e_cal.get())
            
            self.comidas_data[nombre_comida] = {"carbs": c, "grasas": g, "protes": p, "cals": cal}
            
            messagebox.showinfo("Éxito", f"¡{nombre_comida} registrada correctamente!")
            self.mostrar_menu_comidas()
        except ValueError:
            messagebox.showerror("Error", "Ingresa valores numéricos válidos.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppFitnessAvanzada(root)
    root.mainloop()