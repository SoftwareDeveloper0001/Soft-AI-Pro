from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal
import sys
from pathlib import Path

ProjectWizard = None


class ProjectPage(QWidget):
    wizard_requested = Signal()

    def __init__(self):
        super().__init__()
        self.wizard_window = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(28, 28, 28, 28)

        header = QLabel("Buat & Kelola Project")
        header.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: 800;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1d4ed8, stop:1 #14b8a6);
                padding: 18px 22px;
                border-radius: 16px;
            }
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        body = QHBoxLayout()
        body.setSpacing(16)

        left_panel = QFrame()
        left_panel.setStyleSheet("background: rgba(255,255,255,0.09); border-radius: 16px; padding: 8px; border: 1px solid rgba(255,255,255,0.14);")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(12)

        left_title = QLabel("Form Project Baru")
        left_title.setStyleSheet("color: white; font-size: 16px; font-weight: 700;")
        left_layout.addWidget(left_title)

        form_layout = QFormLayout()
        form_layout.setSpacing(12)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Contoh: Dashboard Admin AI")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Web Application", "Mobile App", "Desktop Software", "AI/ML Project", "Database System"])
        self.desc_text = QTextEdit()
        self.desc_text.setPlaceholderText("Jelaskan tujuan, target pengguna, dan fitur utama project...")
        self.desc_text.setMinimumHeight(110)

        input_style = """
            QLineEdit, QComboBox, QTextEdit {
                padding: 11px;
                background: rgba(255,255,255,0.14);
                border: 1px solid rgba(255,255,255,0.22);
                border-radius: 10px;
                color: white;
                font-size: 13.5px;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 1px solid #38bdf8;
                background: rgba(255,255,255,0.2);
            }
        """
        self.name_input.setStyleSheet(input_style)
        self.type_combo.setStyleSheet(input_style)
        self.desc_text.setStyleSheet(input_style)

        form_layout.addRow("Nama Project:", self.name_input)
        form_layout.addRow("Tipe Project:", self.type_combo)
        form_layout.addRow("Deskripsi:", self.desc_text)
        left_layout.addLayout(form_layout)

        create_btn = QPushButton("Buat Project Baru")
        create_btn.setCursor(Qt.PointingHandCursor)
        create_btn.setMinimumHeight(48)
        create_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #059669);
                color: white; border: none; border-radius: 10px; font-size: 14px; font-weight: 700;
            }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #34d399, stop:1 #10b981); }
        """)
        create_btn.clicked.connect(self.open_wizard)
        left_layout.addWidget(create_btn, alignment=Qt.AlignCenter)

        right_panel = QFrame()
        right_panel.setStyleSheet("background: rgba(255,255,255,0.09); border-radius: 16px; padding: 8px; border: 1px solid rgba(255,255,255,0.14);")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(10)

        right_title = QLabel("Panduan Cepat")
        right_title.setStyleSheet("color: white; font-size: 16px; font-weight: 700;")
        right_layout.addWidget(right_title)

        tips = [
            "• Tentukan scope project dengan jelas.",
            "• Pilih tipe project sesuai kebutuhan tim.",
            "• Tambahkan deskripsi agar AI memahami konteks.",
            "• Simpan progres secara berkala untuk tracking.",
        ]
        for text in tips:
            label = QLabel(text)
            label.setStyleSheet("color: #DDEEFF; font-size: 12px;")
            label.setWordWrap(True)
            right_layout.addWidget(label)

        recent_title = QLabel("Project Terbaru")
        recent_title.setStyleSheet("color: white; font-size: 15px; font-weight: 700;")
        right_layout.addWidget(recent_title)
        recent_list = QListWidget()
        recent_list.setStyleSheet("""
            QListWidget { background: rgba(0,0,0,0.18); border-radius: 10px; color: white; }
            QListWidget::item { padding: 8px; }
        """)
        recent_list.addItems(["AI Assistant Dashboard", "Inventory Control", "Learning Platform"])
        right_layout.addWidget(recent_list)

        body.addWidget(left_panel, 2)
        body.addWidget(right_panel, 1)
        layout.addLayout(body)

    def open_wizard(self):
        global ProjectWizard
        if ProjectWizard is None:
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from project_page import ProjectWizard as PW
            ProjectWizard = PW

        if self.wizard_window is None or not self.wizard_window.isVisible():
            self.wizard_window = ProjectWizard()
            self.wizard_window.setWindowTitle("Project Wizard - Buat Project Baru")
            self.wizard_window.setMinimumSize(1000, 700)
            self.wizard_window.show()
        else:
            self.wizard_window.raise_()
            self.wizard_window.activateWindow()
