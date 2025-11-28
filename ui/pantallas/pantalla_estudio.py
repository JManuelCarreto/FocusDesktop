from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QHBoxLayout
from PySide6.QtCore import Qt, QTimer, QElapsedTimer
from PySide6.QtGui import QImage, QPixmap
import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

class PantallaEstudio(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.time_left = 15 * 60
        self.session_running = False

        # Timers
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.update_camera)

        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)

        # Cooldown gestos
        self.gesture_cooldown_ms = 1200
        self.gesture_timer = QElapsedTimer()
        self.gesture_timer.start()

        # Overlay para gestos
        self.overlay_label = QLabel("", self)
        self.overlay_label.setStyleSheet(
            "font-size: 32px; font-weight: bold; color: white; "
            "background-color: rgba(0,0,0,180); border-radius: 10px; padding: 20px;"
        )
        self.overlay_label.setAlignment(Qt.AlignCenter)
        self.overlay_label.hide()

        # Estado de pausa
        self.pause_active = False

        # Timer para ocultar mensajes temporales
        self.overlay_timer = QTimer()
        self.overlay_timer.setSingleShot(True)
        self.overlay_timer.timeout.connect(self.overlay_label.hide)

        # Layout principal
        main_layout = QVBoxLayout()

        title = QLabel("SESIÓN DE ESTUDIO")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #003366")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        content_layout = QHBoxLayout()

        # Lista de tareas
        self.study_tasks = [
            "1. Preparar",
            "   - Abrir materiales",
            "   - Escribir objetivo del bloque",
            "   - Cerrar distracciones",
            "2. Lectura rápida / Escaneo",
            "   - Dar una primera pasada al tema",
            "   - Identificar subtítulos, palabras clave, fórmulas o pasos importantes",
            "3. Estudio profundo / Comprensión",
            "   - Leer a detalle",
            "   - Subrayar",
            "   - Hacer mini-resumen mental",
            "   - Analizar ejemplos",
            "4. Práctica / Aplicación",
            "   - Hacer ejercicios",
            "   - Resolver preguntas rápidas",
            "   - Explicar en voz alta el concepto",
            "   - Construir una tabla/resumen corto",
            "5. Cierre / Microevaluación",
            "   - Escribir qué entendiste y qué quedó pendiente",
            "   - Preparar el objetivo para el siguiente bloque"
        ]

        self.task_list = QListWidget()
        self.task_list.setStyleSheet("QListWidget {color: black; background-color: white; font-size: 14px; font-family: Arial;}")
        self.task_list.setFixedHeight(240)
        self.task_list.addItems(self.study_tasks)
        content_layout.addWidget(self.task_list)

        self.total_tasks = sum(1 for t in self.study_tasks if t.strip().startswith("-"))
        self.tasks_completed = 0

        # Cámara
        self.camera_label = QLabel()
        self.camera_label.setFixedSize(300, 200)
        self.camera_label.setStyleSheet("background-color: black;")
        content_layout.addWidget(self.camera_label)

        main_layout.addLayout(content_layout)

        # Cronómetro
        self.timer_label = QLabel("15:00")
        self.timer_label.setStyleSheet("font-size: 28px; color: #007BFF; font-weight: bold;")
        self.timer_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.timer_label)

        # Botones
        btn_pause = QPushButton("🤚🏼 Pausa")
        btn_next = QPushButton("👍🏼 Siguiente Tarea")
        main_layout.addWidget(btn_pause, alignment=Qt.AlignCenter)
        main_layout.addWidget(btn_next, alignment=Qt.AlignCenter)

        btn_back = QPushButton("👍🏼👍🏼 Terminar Sesión")
        main_layout.addWidget(btn_back, alignment=Qt.AlignCenter)

        # Cuenta regresiva inicial
        self.countdown_time = 5
        self.countdown_label = QLabel("Comenzando en 5...")
        self.countdown_label.setStyleSheet("font-size: 20px; color: red;")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        main_layout.insertWidget(2, self.countdown_label)

        self.setLayout(main_layout)

        # Cámara
        self.cap = None

        # MediaPipe Hands
        self.hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

        # Contadores gestos
        self.thumb_up_counter = 0
        self.palm_open_counter = 0
        self.two_thumbs_counter = 0
        self.pause_count = 0


    # --- Control de pantalla ---
    def showEvent(self, event):
        super().showEvent(event)
        self.time_left = 25 * 60
        self.timer_label.setText("25:00")
        self.session_running = False

        self.task_list.clear()
        self.task_list.addItems(self.study_tasks)
        self.task_list.setCurrentRow(0)
        self.task_list.setFixedHeight(240)

        self.tasks_completed = 0
        self.total_tasks = sum(1 for t in self.study_tasks if t.strip().startswith("-"))

        self.countdown_time = 5
        self.countdown_label.setText("Comenzando en 5...")
        self.countdown_label.show()

        self.gesture_timer.restart()

        self.cap = cv2.VideoCapture(0)
        if self.cap.isOpened():
            self.camera_timer.start(33)
        self.countdown_timer.start(1000)

        current_item = self.task_list.currentItem()
        if current_item:
            text = current_item.text().strip()
            if text[0].isdigit():
                self.motivation_task(text)

    def hideEvent(self, event):
        if self.camera_timer.isActive():
            self.camera_timer.stop()
        if self.countdown_timer.isActive():
            self.countdown_timer.stop()
        if self.timer.isActive():
            self.timer.stop()
        if self.cap and self.cap.isOpened():
            self.cap.release()
        event.accept()

    def closeEvent(self, event):
        if self.cap and self.cap.isOpened():
            self.cap.release()
        event.accept()

    # --- Cuenta regresiva ---
    def update_countdown(self):
        self.countdown_time -= 1
        if self.countdown_time > 0:
            self.countdown_label.setText(f"Comenzando en {self.countdown_time}...")
        else:
            self.countdown_timer.stop()
            self.countdown_label.hide()
            self.start_timer()

    def start_timer(self):
        self.timer.start(1000)
        self.session_running = True

    def update_timer(self):
        if self.time_left > 0:
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")
            self.time_left -= 1
        else:
            self.timer.stop()
            self.end_session()

    # --- Cámara ---
    def update_camera(self):
        if not self.cap or not self.cap.isOpened():
            return
        ret, frame = self.cap.read()
        if not ret:
            return
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if results.multi_hand_landmarks:
            all_hands = list(results.multi_hand_landmarks)
            handedness_list = results.multi_handedness

            for hand_landmarks in all_hands:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            self.detect_gesture(all_hands, handedness_list)

        display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = display.shape
        img = QImage(display.data, w, h, ch * w, QImage.Format_RGB888)
        pix = QPixmap.fromImage(img).scaled(
            self.camera_label.width(), self.camera_label.height(),
            Qt.KeepAspectRatio
        )
        self.camera_label.setPixmap(pix)

    # --- Gestos ---
    def is_palm_open(self, hand):
        idx_tip = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        idx_mcp = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
        mid_tip = hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        mid_mcp = hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
        ring_tip = hand.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
        ring_mcp = hand.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
        pink_tip = hand.landmark[mp_hands.HandLandmark.PINKY_TIP]
        pink_mcp = hand.landmark[mp_hands.HandLandmark.PINKY_MCP]
        thumb_tip = hand.landmark[mp_hands.HandLandmark.THUMB_TIP]
        thumb_mcp = hand.landmark[mp_hands.HandLandmark.THUMB_MCP]

        fingers_extended = (
            idx_tip.y < idx_mcp.y and
            mid_tip.y < mid_mcp.y and
            ring_tip.y < ring_mcp.y and
            pink_tip.y < pink_mcp.y
        )
        thumb_extended = abs(thumb_tip.x - thumb_mcp.x) > 0.05
        return fingers_extended and thumb_extended

    def is_thumb_up(self, hand):
        thumb_tip = hand.landmark[mp_hands.HandLandmark.THUMB_TIP]
        thumb_ip = hand.landmark[mp_hands.HandLandmark.THUMB_IP]
        index_tip = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        wrist = hand.landmark[mp_hands.HandLandmark.WRIST]

        return (thumb_tip.y < thumb_ip.y and
                thumb_tip.y < index_tip.y and
                thumb_tip.y < middle_tip.y and
                thumb_tip.y < wrist.y - 0.02)

    def detect_gesture(self, all_hands, handedness_list):
        if self.gesture_timer.elapsed() < self.gesture_cooldown_ms:
            return

        # Pausa con palma abierta
        any_palm_open = any(self.is_palm_open(hand) for hand in all_hands)
        if any_palm_open:
            self.palm_open_counter += 1
            if self.palm_open_counter >= 5:
                self.pause_active = not self.pause_active
                self.toggle_session()
                self.overlay_label.setText("⏸ Pausa" if self.pause_active else "▶ Reanudar")
                self.overlay_label.show()
                self.overlay_label.raise_()
                self.overlay_timer.start(1500)
                self.gesture_timer.restart()
                self.palm_open_counter = 0
                return
        else:
            self.palm_open_counter = 0

        # Contar pulgares arriba
        thumbs_up_count = 0
        seen_hands = set()
        for hand, handedness in zip(all_hands, handedness_list):
            label = handedness.classification[0].label
            if label not in seen_hands:
                seen_hands.add(label)
                if self.is_thumb_up(hand):
                    thumbs_up_count += 1

        if thumbs_up_count == 2:
            self.two_thumbs_counter += 1
            self.thumb_up_counter = 0
            if self.two_thumbs_counter >= 5:
                self.end_session()
                self.overlay_timer.start(1500)
                self.gesture_timer.restart()
                self.two_thumbs_counter = 0
                return

        elif thumbs_up_count == 1:
            self.thumb_up_counter += 1
            self.two_thumbs_counter = 0
            if self.thumb_up_counter >= 5:
                self.mark_task_done()
                self.overlay_label.setText("✅Tarea terminada")
                self.overlay_label.show()
                self.overlay_label.raise_()
                self.overlay_timer.start(2000)
                self.gesture_timer.restart()
                self.thumb_up_counter = 0
                return

        else:
            self.thumb_up_counter = 0
            self.two_thumbs_counter = 0

    # --- Acciones de sesión y tareas ---
    def toggle_session(self):
        if self.session_running:
            self.timer.stop()
            self.session_running = False
            self.pause_count += 1
        else:
            self.timer.start(1000)
            self.session_running = True

    def next_task(self):
        current = self.task_list.currentRow()
        if current < self.task_list.count() - 1:
            self.task_list.setCurrentRow(current + 1)

    def mark_task_done(self):
        while True:
            current = self.task_list.currentRow()
            if current < 0 or current >= self.task_list.count():
                return

            item = self.task_list.item(current)
            text = item.text().strip()

            if text.startswith("-"):
                break
            else:
                if current < self.task_list.count() - 1:
                    self.task_list.setCurrentRow(current + 1)
                else:
                    return

        if not text.endswith("✅"):
            item.setText(text + "✅")
            self.tasks_completed += 1

        completed = 0
        total = 0
        for i in range(self.task_list.count()):
            t = self.task_list.item(i).text().strip()
            if t.startswith("-"):
                total += 1
                if t.endswith("✅"):
                    completed += 1

        if completed == total:
            self.end_session()
            return

        if current < self.task_list.count() - 1:
            self.task_list.setCurrentRow(current + 1)

    def end_session(self):
        # Parar cronómetro
        if self.timer.isActive():
            self.timer.stop()

        # Calcular tiempo transcurrido y guardarlo en app
        elapsed = (25 * 60) - self.time_left
        minutes = elapsed // 60
        seconds = elapsed % 60
        self.app.session_time = f"{minutes}:{seconds:02d} min"

        #Guardar tareas y pausas
        self.app.tasks_completed = self.tasks_completed
        self.app.session_tasks_summary = f"Tareas completadas: {self.tasks_completed} /15"
        self.app.pause_count = self.pause_count

        #Guardar nivel de concentración
        self.app.pause_count = self.pause_count

        # Cambiar a pantalla de fin
        self.app.change_screen("end")

    # --- Overlay centrado ---
    def resizeEvent(self, event):
        super().resizeEvent(event)
        w, h = 300, 120
        x = (self.width() - w) // 2
        y = (self.height() - h) // 2
        self.overlay_label.setGeometry(x, y, w, h)
