from PySide6.QtWidgets import *
from PySide6.QtCore import Qt


class ArchivePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(18)
        layout.setContentsMargins(28, 28, 28, 28)

        header = QLabel("Arsip Project")
        header.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: 800;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7c3aed, stop:1 #2563eb);
                padding: 18px 20px;
                border-radius: 16px;
            }
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        top_bar = QHBoxLayout()
        search_box = QLineEdit()
        search_box.setPlaceholderText("Cari project arsip...")
        search_box.setMinimumHeight(44)
        search_box.setStyleSheet("""
            QLineEdit {
                padding: 10px; background: rgba(255,255,255,0.14); border: 1px solid rgba(255,255,255,0.2);
                border-radius: 10px; color: white; font-size: 13px;
            }
        """)
        top_bar.addWidget(search_box, 1)

        filter_btn = QPushButton("Filter")
        filter_btn.setStyleSheet("background: rgba(255,255,255,0.14); color: white; border-radius: 10px; padding: 8px 14px;")
        top_bar.addWidget(filter_btn)
        layout.addLayout(top_bar)

        stats_row = QHBoxLayout()
        stats_row.setSpacing(12)
        for label, value in [("Total Arsip", "18"), ("Selesai", "12"), ("Dalam Review", "6")]:
            card = QFrame()
            card.setStyleSheet("background: rgba(255,255,255,0.09); border-radius: 14px; padding: 8px; border: 1px solid rgba(255,255,255,0.12);")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(12, 10, 12, 10)
            card_title = QLabel(label)
            card_title.setStyleSheet("color: #DDEEFF; font-size: 12px;")
            card_value = QLabel(value)
            card_value.setStyleSheet("color: white; font-size: 22px; font-weight: 700;")
            card_layout.addWidget(card_title)
            card_layout.addWidget(card_value)
            stats_row.addWidget(card)
        layout.addLayout(stats_row)

        self.projects_list = QListWidget()
        self.projects_list.setStyleSheet("""
            QListWidget { background: rgba(255,255,255,0.08); border-radius: 14px; padding: 8px; color: white; }
            QListWidget::item { padding: 12px; margin: 4px; background: rgba(255,255,255,0.08); border-radius: 8px; }
            QListWidget::item:hover { background: rgba(255,255,255,0.16); }
        """)
        sample_projects = [
            "E-Commerce Website — Selesai • 2025",
            "Mobile Banking App — Review • 2025",
            "School Management System — Arsip • 2024",
            "AI Chat Bot — Selesai • 2024",
            "Inventory System — Aktif • 2024",
        ]
        self.projects_list.addItems(sample_projects)
        layout.addWidget(self.projects_list)

        detail = QLabel("Arsip membantu tim meninjau ulang hasil kerja lama dan memanfaatkan pembelajaran dari project sebelumnya.")
        detail.setStyleSheet("color: #CBE8FF; font-size: 12px;")
        detail.setWordWrap(True)
        layout.addWidget(detail)
