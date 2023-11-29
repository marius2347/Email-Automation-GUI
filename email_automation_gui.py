# Email Automation GUI

# importing sys for handling application termination and exit status
import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QFormLayout, QLineEdit, QPlainTextEdit, \
    QHBoxLayout, QPushButton, QFileDialog, QVBoxLayout, QMessageBox
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import Qt

# import libraries for email sending and attachments
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# creating an instance of QApplication
eApp = QApplication([])

# creating Email Automation's GUI
window = QWidget()
window.setWindowTitle("Email Automation GUI")

# set fixed window size
window.setFixedSize(700, 650)

# get primary screen
primaryScreen = QGuiApplication.primaryScreen()

# center the window on the screen
rect = primaryScreen.availableGeometry()
x = (rect.width() - window.width()) // 2
y = (rect.height() - window.height()) // 2
window.move(x, y)

# content from GUI
headText = QLabel("<h1> Email Automation GUI </h1>", parent=window)

# center the head text
headText.setAlignment(Qt.AlignmentFlag.AlignCenter)
headText.setGeometry(0, 0, 700, 50)  # Adjust the y-coordinate to move it to the top

# layout
layout = QFormLayout()

# create a horizontal layout for the "My Email" and "Password" row
emailPasswordRowLayout = QHBoxLayout()

# "My Email" label and input
emailLabel = QLabel("My Email")
emailLineEdit = QLineEdit()
emailPasswordRowLayout.addWidget(emailLabel)
emailPasswordRowLayout.addWidget(emailLineEdit)

# "Password" label and input
passwordLabel = QLabel("Password")
passwordLineEdit = QLineEdit()
emailPasswordRowLayout.addWidget(passwordLabel)
emailPasswordRowLayout.addWidget(passwordLineEdit)

# add the "My Email" and "Password" row
layout.addRow(emailPasswordRowLayout)

# create a horizontal layout for the "Send to Email" row
emailToSendRowLayout = QHBoxLayout()

# "Send to Email" label and input
emailToSendLabel = QLabel("Send to Email")
emailToSendLineEdit = QLineEdit()
emailToSendRowLayout.addWidget(emailToSendLabel)
emailToSendRowLayout.addWidget(emailToSendLineEdit)

# 'Subject' label
subjectLabel = QLabel("Subject")
subjectLineEdit = QLineEdit()
emailToSendRowLayout.addWidget(subjectLabel)
emailToSendRowLayout.addWidget(subjectLineEdit)

# "Attach File" button
attachmentButton = QPushButton("Attach File")

# function to handle attachment button clicked
file_dialog = QFileDialog()
selected_file_path = None

def attach_file_clicked():
    global selected_file_path
    selected_file_path, _ = file_dialog.getOpenFileName(window, "Attach File", "", "All Files (*)")
    if selected_file_path:
        print("Selected File:", selected_file_path)

# connect the "Attach File" button to the function
attachmentButton.clicked.connect(attach_file_clicked)
emailToSendRowLayout.addWidget(attachmentButton)

# add the "Send to Email" row
layout.addRow(emailToSendRowLayout)

# create a new label for the textPlainEdit
messageLabel = QLabel("Message")

# add the "Message" label and textPlainEdit in a horizontal layout
messageRowLayout = QHBoxLayout()
messageRowLayout.addWidget(messageLabel)
messageRowLayout.addWidget(QLabel(""))  # Spacer
layout.addRow(messageRowLayout)

# add the "Message" row
textPlainEdit = QPlainTextEdit()
layout.addRow(textPlainEdit)

# add a button
button = QPushButton("Submit")

# function to retrieve values when Submit button is clicked
def on_submit_clicked():
    enteredEmail = emailLineEdit.text()
    enteredPassword = passwordLineEdit.text()
    enteredEmailSendTo = emailToSendLineEdit.text()
    enteredSubjectText = subjectLineEdit.text()
    enteredMessage = textPlainEdit.toPlainText()

    print("Entered Email:", enteredEmail)
    print("Entered Password:", enteredPassword)
    print("Entered Email Send To:", enteredEmailSendTo)
    print("Entered Subject Text:", enteredSubjectText)
    print("Entered Message:", enteredMessage)

    # print the selected file path if available
    if selected_file_path:
        print("Selected File:", selected_file_path)

    # my informations
    smtpServer = 'smtp.gmail.com'
    smtpPort = 587
    smtpUsername = enteredEmail
    smtpPassword = enteredPassword

    msg = MIMEMultipart()
    msg['From'] = enteredEmail
    msg['To'] = enteredEmailSendTo
    msg['Subject'] = enteredSubjectText
    msg.attach(MIMEText(enteredMessage))

    with open(selected_file_path, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='pdf')
        attachment.add_header('Content-Disposition', 'attachment', filename=selected_file_path)
        msg.attach(attachment)

    with smtplib.SMTP(smtpServer, smtpPort) as smtp:
        smtp.starttls()
        smtp.login(smtpUsername, smtpPassword)
        smtp.send_message(msg)

    # show a popup to inform the user that the email has been sent
    QMessageBox.information(window, "Email Sent", "The email has been sent successfully!")

# connect the "Submit" button to the function
button.clicked.connect(on_submit_clicked)

# add the button below textPlainEdit
buttonLayout = QHBoxLayout()
buttonLayout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addRow(buttonLayout)

# wrap the layout in a QVBoxLayout for centering
centerLayout = QVBoxLayout()
centerLayout.addWidget(headText)
centerLayout.addSpacing(50)
centerLayout.addLayout(layout)
centerLayout.setContentsMargins(50, 50, 50, 50)

# set top margin to move the layout down
centerLayout.setContentsMargins(50, 70, 50, 20)

# run app
window.setLayout(centerLayout)
window.show()
sys.exit(eApp.exec())
