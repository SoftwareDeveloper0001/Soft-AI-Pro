import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from soft_ai_code import SoftAICodeUI, load_fonts, get_global_styles

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(app.font())
    try:
        load_fonts(Path(__file__).parent / 'fonts')
    except Exception:
        pass

    try:
        app.setStyleSheet(get_global_styles())
    except Exception:
        pass

    window = SoftAICodeUI()
    window.show()
    sys.exit(app.exec())