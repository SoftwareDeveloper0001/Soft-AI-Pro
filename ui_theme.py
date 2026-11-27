from pathlib import Path
from typing import Optional
from PySide6.QtGui import QFontDatabase, QFont, QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect

# Centralized UI theme for Soft AI Pro - MODERN REDESIGN 2026
# Professional, modern design with better visual hierarchy and UX

PALETTE = {
    # Modern gradient background
    'bg_start': '#0A0E27',      # Deep dark blue
    'bg_end': '#141B3A',        # Medium dark blue
    'bg_accent': '#1A2847',     # Accent dark blue
    
    # Surface and containers
    'surface': 'rgba(255,255,255,0.04)',
    'surface_hover': 'rgba(255,255,255,0.08)',
    'surface_active': 'rgba(255,255,255,0.12)',
    
    # Brand colors - Modern gradients
    'primary': '#7C3AED',       # Vibrant purple (primary)
    'primary_light': '#A78BFA', # Light purple
    'primary_dark': '#5B21B6',  # Dark purple
    
    'accent': '#06B6D4',        # Cyan accent
    'accent_light': '#22D3EE',  # Light cyan
    'accent_dark': '#0891B2',   # Dark cyan
    
    # Status colors
    'success': '#10B981',       # Modern green
    'warning': '#F59E0B',       # Modern amber
    'error': '#EF4444',         # Modern red
    'info': '#3B82F6',          # Modern blue
    
    # Text colors
    'text': '#F0F4F8',          # Primary text
    'text_secondary': '#CBD5E1', # Secondary text
    'text_muted': '#94A3B8',    # Muted text
    
    # Special colors
    'border': 'rgba(148,163,184,0.2)',
    'border_focus': 'rgba(124,58,237,0.5)',
    'shadow': 'rgba(0,0,0,0.3)',
}


def load_fonts(font_dir: Optional[Path] = None):
    """Attempt to load bundled fonts from `font_dir` (if provided).

    This is best-effort; function will not raise on failure.
    """
    try:
        if font_dir is None:
            return
        font_dir = Path(font_dir)
        if not font_dir.exists():
            return
        for f in font_dir.glob('*.ttf'):
            QFontDatabase.addApplicationFont(str(f))
    except Exception:
        pass


def get_global_styles() -> str:
    """Return global stylesheet string for MODERN UI - Professional Design 2026
    
    Features:
    - Modern gradient backgrounds
    - Better contrast and readability
    - Smooth transitions and hover effects
    - Professional color scheme
    - Enhanced visual hierarchy
    """
    return f"""
        /* ===== MAIN APPLICATION ===== */
        QWidget {{
            color: {PALETTE['text']};
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1, 
                        stop:0 {PALETTE['bg_start']}, 
                        stop:1 {PALETTE['bg_end']});
            font-family: 'Segoe UI', 'Poppins', 'Inter', sans-serif;
            font-size: 11pt;
        }}

        /* ===== FRAMES & CONTAINERS ===== */
        QFrame {{
            background: {PALETTE['surface']};
            border: 1px solid {PALETTE['border']};
            border-radius: 12px;
            margin: 0px;
            padding: 0px;
        }}

        QFrame:hover {{
            background: {PALETTE['surface_hover']};
            border: 1px solid {PALETTE['border_focus']};
        }}

        /* ===== BUTTONS - PRIMARY ===== */
        QPushButton {{
            color: {PALETTE['text']};
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                        stop:0 {PALETTE['primary']},
                        stop:1 {PALETTE['primary_dark']});
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 11pt;
            margin: 4px;
            transition: all 0.3s ease;
        }}

        QPushButton:hover {{
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                        stop:0 {PALETTE['primary_light']},
                        stop:1 {PALETTE['primary']});
            padding: 11px 22px;
        }}

        QPushButton:pressed {{
            background: {PALETTE['primary_dark']};
            padding: 9px 19px;
        }}

        QPushButton:disabled {{
            color: {PALETTE['text_muted']};
            background: {PALETTE['surface']};
            opacity: 0.5;
        }}

        /* ===== INPUT FIELDS ===== */
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background: {PALETTE['surface']};
            color: {PALETTE['text']};
            border: 2px solid {PALETTE['border']};
            border-radius: 8px;
            padding: 10px 12px;
            selection-background-color: {PALETTE['primary']};
            font-size: 11pt;
        }}

        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border: 2px solid {PALETTE['primary']};
            background: {PALETTE['surface_active']};
        }}

        /* ===== COMBO BOXES & DROPDOWNS ===== */
        QComboBox {{
            background: {PALETTE['surface']};
            color: {PALETTE['text']};
            border: 2px solid {PALETTE['border']};
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 11pt;
        }}

        QComboBox:focus {{
            border: 2px solid {PALETTE['primary']};
            background: {PALETTE['surface_active']};
        }}

        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}

        QComboBox::down-arrow {{
            image: none;
            width: 14px;
            height: 8px;
        }}

        /* ===== CHECKBOXES & RADIO BUTTONS ===== */
        QCheckBox, QRadioButton {{
            color: {PALETTE['text']};
            spacing: 8px;
            outline: none;
        }}

        QCheckBox::indicator, QRadioButton::indicator {{
            width: 18px;
            height: 18px;
        }}

        QCheckBox::indicator:unchecked {{
            background: {PALETTE['surface']};
            border: 2px solid {PALETTE['border']};
            border-radius: 4px;
        }}

        QCheckBox::indicator:checked {{
            background: {PALETTE['primary']};
            border: 2px solid {PALETTE['primary']};
            border-radius: 4px;
        }}

        /* ===== TABS ===== */
        QTabWidget {{
            background: transparent;
            border: none;
        }}

        QTabBar::tab {{
            background: {PALETTE['surface']};
            color: {PALETTE['text_secondary']};
            border: 1px solid {PALETTE['border']};
            border-bottom: 2px solid transparent;
            padding: 12px 20px;
            margin-right: 2px;
            border-radius: 8px 8px 0px 0px;
            font-weight: bold;
        }}

        QTabBar::tab:hover {{
            background: {PALETTE['surface_hover']};
            color: {PALETTE['text']};
        }}

        QTabBar::tab:selected {{
            background: {PALETTE['primary']};
            color: {PALETTE['text']};
            border: 1px solid {PALETTE['primary']};
            border-bottom: 3px solid {PALETTE['accent']};
        }}

        /* ===== SCROLL BARS ===== */
        QScrollBar:vertical {{
            background: transparent;
            width: 12px;
            border: none;
        }}

        QScrollBar::handle:vertical {{
            background: {PALETTE['primary']};
            border-radius: 6px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: {PALETTE['primary_light']};
        }}

        QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical {{
            border: none;
            background: none;
        }}

        /* ===== LABELS & TEXT ===== */
        QLabel {{
            color: {PALETTE['text']};
            background: transparent;
        }}

        /* ===== TOOLTIPS ===== */
        QToolTip {{
            background: {PALETTE['bg_accent']};
            color: {PALETTE['text']};
            border: 1px solid {PALETTE['border_focus']};
            border-radius: 6px;        }

        /* ===== MODERN PAGE ELEMENTS ===== */
        QFrame#sectionCard {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: 20px;
            padding: 18px;
        }

        QLabel#pageTitle {
            color: #F8FAFC;
            font-size: 26pt;
            font-weight: 800;
        }

        QLabel#pageSubtitle {
            color: #CBD5E1;
            font-size: 11pt;
            line-height: 1.6;
        }

        QPushButton#primaryButton {
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 {PALETTE['primary']}, stop:1 {PALETTE['primary_dark']});
            color: {PALETTE['text']};
            border-radius: 12px;
            padding: 12px 22px;
            font-weight: 700;
        }

        QPushButton#primaryButton:hover {
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 {PALETTE['primary_light']}, stop:1 {PALETTE['primary']});
        }

        QPushButton#secondaryButton {
            background: rgba(255,255,255,0.08);
            color: {PALETTE['text']};
            border: 1px solid rgba(255,255,255,0.16);
            border-radius: 12px;
            padding: 10px 20px;
        }

        QListWidget#highlightList {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.16);
            border-radius: 12px;
            padding: 8px;
        }

        QScrollArea {
            background: transparent;
            border: none;
        }
            padding: 8px 12px;
            font-size: 10pt;
        }}

        /* ===== MENU BARS & MENUS ===== */
        QMenuBar {{
            background: {PALETTE['surface']};
            color: {PALETTE['text']};
            border-bottom: 1px solid {PALETTE['border']};
        }}

        QMenuBar::item:selected {{
            background: {PALETTE['primary']};
            border-radius: 4px;
        }}

        QMenu {{
            background: {PALETTE['bg_accent']};
            color: {PALETTE['text']};
            border: 1px solid {PALETTE['border']};
            border-radius: 8px;
        }}

        QMenu::item:selected {{
            background: {PALETTE['primary']};
            border-radius: 4px;
        }}

        /* ===== SPIN BOXES ===== */
        QSpinBox, QDoubleSpinBox {{
            background: {PALETTE['surface']};
            color: {PALETTE['text']};
            border: 2px solid {PALETTE['border']};
            border-radius: 8px;
            padding: 8px;
        }}

        QSpinBox:focus, QDoubleSpinBox:focus {{
            border: 2px solid {PALETTE['primary']};
        }}

        QSpinBox::up-button, QDoubleSpinBox::up-button {{
            background: {PALETTE['primary']};
            border: none;
            width: 20px;
        }}

        QSpinBox::down-button, QDoubleSpinBox::down-button {{
            background: {PALETTE['primary']};
            border: none;
            width: 20px;
        }}
    """


def button_gradient(start: str = None, end: str = None, text_color: str = None) -> str:
    s = start or PALETTE['primary']
    e = end or PALETTE['accent']
    t = text_color or PALETTE['text']
    return f"background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 {s}, stop:1 {e}); color: {t};"


def apply_shadow(widget, blur: int = 20, x: int = 0, y: int = 8, color: QColor = QColor(0, 0, 0, 90)):
    try:
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(blur)
        effect.setXOffset(x)
        effect.setYOffset(y)
        effect.setColor(color)
        widget.setGraphicsEffect(effect)
    except Exception:
        pass


if __name__ == '__main__':
    print('ui_theme module - palette:')
    for k, v in PALETTE.items():
        print(f'  {k}: {v}')
