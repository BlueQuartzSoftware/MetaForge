from PySide2.QtWidgets import QLabel

def notify_error_message(error_label: QLabel, msg: str) -> None:
    error_label.setStyleSheet("QLabel { color: #b43431; }")
    error_label.setText(msg)

def notify_no_errors(error_label: QLabel) -> None:
    error_label.setStyleSheet("")
    error_label.setText("No errors.")
