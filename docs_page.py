from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTreeWidget,
    QTreeWidgetItem, QSplitter, QTextBrowser
)
from PySide6.QtCore import Qt


class DocsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(14)

        header = QLabel("Dokumentasi & Panduan")
        header.setStyleSheet("""
            QLabel {
                color: white; font-size: 32px; font-weight: 800;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0f766e, stop:1 #2563eb);
                padding: 18px 20px; border-radius: 16px;
            }
        """)
        layout.addWidget(header)

        splitter = QSplitter()
        splitter.setOrientation(Qt.Orientation.Horizontal)

        tree = QTreeWidget()
        tree.setHeaderLabel("Dokumentasi")
        tree.setStyleSheet("""
            QTreeWidget { background: rgba(255,255,255,0.08); border-radius: 14px; color: white; font-size: 12pt; }
            QTreeWidget::item:hover { background: rgba(255,255,255,0.14); }
        """)

        sections = {
            "Getting Started": ["Installation", "Quick Start", "Basic Concepts"],
            "Features": ["AI Integration", "Code Generation", "Project Management"],
            "Tutorials": ["Creating New Project", "Using AI Assistant", "Cloud Sync"],
            "API Reference": ["Core API", "AI Models", "Cloud Services"],
            "Advanced Topics": ["Custom AI Models", "Performance Tuning"],
        }

        self.docs = {
            "Installation": "<h2>Installation</h2><p>Unduh aplikasi, aktifkan environment, lalu jalankan untuk memulai.",
            "Quick Start": "<h2>Quick Start</h2><p>Buat project baru, isi form, lalu gunakan AI assistant untuk memulai workflow.</p>",
            "Basic Concepts": "<h2>Basic Concepts</h2><p>Project, arsip, dokumentasi, dan cloud terintegrasi untuk membantu pengembangan.</p>",
            "AI Integration": "<h2>AI Integration</h2><p>Gunakan AI untuk menilai ide, menghasilkan struktur project, dan membantu dokumentasi.</p>",
            "Code Generation": "<h2>Code Generation</h2><p>Fitur ini membantu mengubah kebutuhan bisnis menjadi kerangka kerja teknis.</p>",
            "Project Management": "<h2>Project Management</h2><p>Kelola timeline, tugas, dan file project di satu tempat yang terpadu.</p>",
            "Creating New Project": "<h2>Creating New Project</h2><p>Buka halaman Project Baru, isi detail, lalu lanjutkan ke wizard untuk setup lengkap.</p>",
            "Using AI Assistant": "<h2>Using AI Assistant</h2><p>AI dapat membantu mengurai kebutuhan, memberi saran, dan mempercepat keputusan desain.</p>",
            "Cloud Sync": "<h2>Cloud Sync</h2><p>Sinkronkan proyek dan file ke layanan cloud agar bisa diakses dengan mudah.</p>",
            "Core API": "<h2>Core API</h2><p>API utama menghubungkan UI, proyek, dan integrasi cloud secara aman dan terstruktur.</p>",
            "AI Models": "<h2>AI Models</h2><p>Model AI dapat disesuaikan berdasarkan kebutuhan aplikasi dan performa yang diinginkan.</p>",
            "Cloud Services": "<h2>Cloud Services</h2><p>Gunakan layanan cloud untuk backup, berbagi, dan kolaborasi tim.</p>",
            "Custom AI Models": "<h2>Custom AI Models</h2><p>Anda dapat menyesuaikan model AI sesuai domain bisnis dan kebutuhan pengguna.</p>",
            "Performance Tuning": "<h2>Performance Tuning</h2><p>Optimalkan performa dengan pengaturan cache, efisiensi UI, dan workflow yang lebih cepat.</p>",
        }

        for section, topics in sections.items():
            parent = QTreeWidgetItem([section])
            for topic in topics:
                child = QTreeWidgetItem([topic])
                parent.addChild(child)
            tree.addTopLevelItem(parent)
        tree.itemClicked.connect(self.on_doc_item_clicked)
        tree.expandAll()

        self.content = QTextBrowser()
        self.content.setStyleSheet("""
            QTextBrowser { background: rgba(255,255,255,0.08); border-radius: 14px; color: white; font-size: 12pt; padding: 16px; }
        """)
        self.content.setOpenExternalLinks(True)
        self.show_doc("Installation")

        splitter.addWidget(tree)
        splitter.addWidget(self.content)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        layout.addWidget(splitter)

    def show_doc(self, topic: str) -> None:
        self.content.setHtml(self.docs.get(topic, "<h2>Dokumentasi</h2><p>Pilih topik untuk melihat isi.</p>"))

    def on_doc_item_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        self.show_doc(item.text(0))
