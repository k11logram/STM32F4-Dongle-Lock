# Authors: Buqwana Xolisile and Kagiso Dube
# Version: 21/10/2025
# Project: EEE3095S Project
# Class Description: Centralized STM32CubeProgrammer inspired UI theme.

class ThemeUI:
    PRIMARY_BG = "#05244b"
    SECONDARY_BG = "#3b546c"
    ACCENT_BLUE = "#1184d5"
    HOVER_BLUE = "#1a9ee9"
    PRESSED_BLUE = "#0f6bab"
    TEXT_COLOR = "#dee4e7"
    SURFACE_BG = "#fafafa"
    BORDER_COLOR = "#687d94"
    SUCCESS_LIME = "#c2c43f"

    @staticmethod
    def get_stylesheet() -> str:
        return f"""
            QWidget {{
                background-color: {ThemeUI.PRIMARY_BG};
                color: {ThemeUI.TEXT_COLOR};
                font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
                font-size: 13px;
            }}

            QLabel#heading {{
                color: #ffffff;
                font-weight: bold;
                font-size: 22px;
                letter-spacing: 1px;
            }}

            QLabel {{
                color: {ThemeUI.TEXT_COLOR};
            }}

            QPushButton {{
                background-color: {ThemeUI.ACCENT_BLUE};
                border: none;
                border-radius: 8px;
                font-weight: 600;
                color: {ThemeUI.TEXT_COLOR};
                font-size: 12px; /* adjusted to visually match label */
                min-width: 150px;
                max-width: 150px;
                min-height: 42px;
                max-height: 42px;
            }}

            QPushButton:hover {{
                background-color: {ThemeUI.HOVER_BLUE};
            }}

            QPushButton:pressed {{
                background-color: {ThemeUI.PRESSED_BLUE};
            }}

            QPushButton:disabled {{
                background-color: {ThemeUI.SECONDARY_BG};
                color: #888888;
            }}

            QLineEdit, QTextEdit {{
                background-color: {ThemeUI.SURFACE_BG};
                border: 1px solid {ThemeUI.BORDER_COLOR};
                border-radius: 6px;
                padding: 5px;
                color: #1a1a1a;
                selection-background-color: {ThemeUI.ACCENT_BLUE};
            }}

            QTextEdit {{
                font-family: Consolas, monospace;
                font-size: 12px;
            }}

            QDialog {{
                background-color: {ThemeUI.PRIMARY_BG};
                color: {ThemeUI.TEXT_COLOR};
                border-radius: 10px;
            }}

            QMessageBox {{
                background-color: {ThemeUI.PRIMARY_BG};
                color: {ThemeUI.TEXT_COLOR};
            }}

            QScrollBar:vertical {{
                border: none;
                background: {ThemeUI.SECONDARY_BG};
                width: 10px;
                margin: 2px 0 2px 0;
                border-radius: 5px;
            }}

            QScrollBar::handle:vertical {{
                background: {ThemeUI.ACCENT_BLUE};
                min-height: 20px;
                border-radius: 5px;
            }}

            QScrollBar::handle:vertical:hover {{
                background: {ThemeUI.HOVER_BLUE};
            }}
        """
