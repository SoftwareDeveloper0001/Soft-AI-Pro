from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QGridLayout
)
from PySide6.QtCore import Qt


class CloudPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(18)
        layout.setContentsMargins(28, 28, 28, 28)

        title = QLabel("Cloud Integration")
        title.setStyleSheet("""
            QLabel {
                color: white; font-size: 32px; font-weight: 800;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2563eb, stop:1 #06b6d4);
                padding: 18px 20px; border-radius: 16px;
            }
        """)
        layout.addWidget(title)

        summary = QLabel("Integrasikan project Anda ke cloud untuk backup, kolaborasi, dan sinkronisasi yang aman.")
        summary.setStyleSheet("color: #DDEEFF; font-size: 13px;")
        summary.setWordWrap(True)
        layout.addWidget(summary)

        status_row = QHBoxLayout()
        for label, value in [("Online", "Connected"), ("Last Sync", "2 min ago"), ("Storage", "1.2 GB")]:
            card = QFrame()
            card.setStyleSheet("background: rgba(255,255,255,0.09); border-radius: 14px; padding: 10px; border: 1px solid rgba(255,255,255,0.12);")
            card_layout = QVBoxLayout(card)
            card_title = QLabel(label)
            card_title.setStyleSheet("color: #CBE8FF; font-size: 12px;")
            card_value = QLabel(value)
            card_value.setStyleSheet("color: white; font-size: 18px; font-weight: 700;")
            card_layout.addWidget(card_title)
            card_layout.addWidget(card_value)
            status_row.addWidget(card)
        layout.addLayout(status_row)

        services_grid = QGridLayout()
        services = [
            {"name": "GitHub Integration", "desc": "Sinkronisasi project dengan repository GitHub."},
            {"name": "Google Drive", "desc": "Backup dan berbagi dokumen secara real-time."},
            {"name": "Dropbox", "desc": "Kolaborasi tim dengan folder bersama."},
            {"name": "OneDrive", "desc": "Akses project dari Microsoft ecosystem."},
        ]

        for i, service in enumerate(services):
            card = self.create_service_card(service)
            services_grid.addWidget(card, i // 2, i % 2)
        layout.addLayout(services_grid)

        action_row = QHBoxLayout()
        action_row.addWidget(QPushButton("Hubungkan akun"))
        action_row.addWidget(QPushButton("Lihat riwayat sinkron"))
        layout.addLayout(action_row)
        layout.addStretch()

    def create_service_card(self, service):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.08); border-radius: 14px; padding: 16px;
            }
            QFrame:hover { background: rgba(255,255,255,0.14); }
        """)
        card_layout = QVBoxLayout(card)

        name = QLabel(service["name"])
        name.setStyleSheet("color: white; font-size: 16.5px; font-weight: 700;")
        desc = QLabel(service["desc"])
        desc.setStyleSheet("color: #EAF6FF; font-size: 12px;")
        desc.setWordWrap(True)

        card_layout.addWidget(name)
        card_layout.addWidget(desc)
        return card
