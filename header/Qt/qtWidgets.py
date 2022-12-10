from header.versions import PYQT_VERSIONS

if PYQT_VERSIONS == "PyQt5":
    from PyQt5.QtWidgets import (
        QApplication,
        QWidget,
        QFrame,
        QStackedWidget,
        QLabel,
        QPushButton,
        QLineEdit,
        QTextBrowser,
        QGroupBox,
        QGridLayout,
        QVBoxLayout,
        QHBoxLayout,
        QCheckBox,
        QInputDialog,
        QComboBox,
        QMenu,
        QTableWidget,
        QScrollArea,
        QWidgetItem,
        QSplitter
    )

if PYQT_VERSIONS == "PyQt6":
    from PyQt6.QtWidgets import (
        QApplication,
        QWidget,
        QFrame,
        QStackedWidget,
        QLabel,
        QPushButton,
        QLineEdit,
        QTextBrowser,
        QGroupBox,
        QGridLayout,
        QVBoxLayout,
        QHBoxLayout,
        QCheckBox,
        QInputDialog,
        QComboBox,
        QMenu,
        QTableWidget,
        QScrollArea,
        QWidgetItem,
        QSplitter
    )

if PYQT_VERSIONS == "PySide2":
    from PySide2.QtWidgets import (
        QApplication,
        QWidget,
        QFrame,
        QStackedWidget,
        QLabel,
        QPushButton,
        QLineEdit,
        QTextBrowser,
        QGroupBox,
        QGridLayout,
        QVBoxLayout,
        QHBoxLayout,
        QCheckBox,
        QInputDialog,
        QComboBox,
        QMenu,
        QTableWidget,
        QScrollArea,
        QWidgetItem,
        QSplitter
    )

if PYQT_VERSIONS == "PySide6":
    from PySide6.QtWidgets import (
        QApplication,
        QWidget,
        QFrame,
        QStackedWidget,
        QLabel,
        QPushButton,
        QLineEdit,
        QTextBrowser,
        QGroupBox,
        QGridLayout,
        QVBoxLayout,
        QHBoxLayout,
        QCheckBox,
        QInputDialog,
        QComboBox,
        QMenu,
        QTableWidget,
        QScrollArea,
        QWidgetItem,
        QSplitter
    )