import sys
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLineEdit, QWidget, QFileDialog, QMessageBox,\
    QHBoxLayout,QGroupBox
from PyQt5.QtGui import QIcon
from pdf_processor import PDFSplitter,PDFMerger  # 确保 PDFSplitter 类在同一个文件夹中

class PDFApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.filesToMerge = []  # 初始化文件列表
        self.initUI()

    def initUI(self):
        self.setWindowTitle('D PDF')
        self.setGeometry(100, 100, 400, 300)
        self.setWindowIcon(QIcon('icon.ico'))

        mainLayout = QVBoxLayout()

        # 分割 PDF 区域
        splitGroup = QGroupBox("Split PDF")
        splitLayout = QVBoxLayout()

        # 源文件路径布局
        self.sourceFileLayout = QHBoxLayout()
        self.fileLineEdit = QLineEdit()
        self.fileLineEdit.setPlaceholderText('Input or select your PDF path')
        self.sourceFileLayout.addWidget(self.fileLineEdit)

        self.chooseFileButton = QPushButton('...')
        self.chooseFileButton.setMaximumWidth(30)
        self.chooseFileButton.clicked.connect(self.openFileDialog)
        self.sourceFileLayout.addWidget(self.chooseFileButton)

        # 保存文件路径布局
        self.saveFileLayout = QHBoxLayout()
        self.saveLineEdit = QLineEdit()
        self.saveLineEdit.setPlaceholderText('Input or select save path')
        self.saveFileLayout.addWidget(self.saveLineEdit)

        self.chooseSaveButton = QPushButton('...')
        self.chooseSaveButton.setMaximumWidth(30)
        self.chooseSaveButton.clicked.connect(self.saveFileDialog)
        self.saveFileLayout.addWidget(self.chooseSaveButton)

        # 页面范围输入框
        self.pagesLineEdit = QLineEdit()
        self.pagesLineEdit.setPlaceholderText('Input ranges, like 1-3, 5-6')

        # 分割 PDF 按钮
        self.splitButton = QPushButton('Split PDF')
        self.splitButton.clicked.connect(self.splitPDF)

        # 将分割相关控件添加到 splitLayout
        splitLayout.addLayout(self.sourceFileLayout)
        splitLayout.addLayout(self.saveFileLayout)
        splitLayout.addWidget(self.pagesLineEdit)
        splitLayout.addWidget(self.splitButton)

        splitGroup.setLayout(splitLayout)
        mainLayout.addWidget(splitGroup)

        # 合并 PDF 区域
        mergeGroup = QGroupBox("Merge PDF")
        mergeLayout = QVBoxLayout()

        # 合并文件路径文本框
        self.mergeFileLineEdit = QLineEdit()
        self.mergeFileLineEdit.setPlaceholderText('Select PDFs to merge')

        # 选择合并文件按钮
        self.chooseMergeFilesButton = QPushButton('Select PDFs')
        self.chooseMergeFilesButton.clicked.connect(self.openMultipleFilesDialog)

        # 保存文件路径编辑框
        self.savePathLineEdit = QLineEdit()
        self.savePathLineEdit.setPlaceholderText('Select save path for merged PDF')

        # 保存文件路径布局
        self.chooseSavePathButton = QPushButton('Choose Save Path')
        self.chooseSavePathButton.clicked.connect(self.merge_saveFileDialog)

        # 合并 PDF 按钮
        self.mergeButton = QPushButton('Merge PDF')
        self.mergeButton.clicked.connect(self.mergePDF)

        # 将合并相关控件添加到 mergeLayout
        mergeLayout.addWidget(self.mergeFileLineEdit)
        mergeLayout.addWidget(self.chooseMergeFilesButton)
        mergeLayout.addWidget(self.savePathLineEdit)
        mergeLayout.addWidget(self.chooseSavePathButton)
        mergeLayout.addWidget(self.mergeButton)

        mergeGroup.setLayout(mergeLayout)
        mainLayout.addWidget(mergeGroup)


        # 设置中央小部件
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)


    def openFileDialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "select", "", "PDF 文件 (*.pdf)")
        if file_path:
            self.fileLineEdit.setText(file_path)

    
    def saveFileDialog(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "save", "", "PDF 文件 (*.pdf)")
        if save_path:
            self.saveLineEdit.setText(save_path)

    def merge_saveFileDialog(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "save", "", "PDF 文件 (*.pdf)")
        if save_path:
            self.savePathLineEdit.setText(save_path)

    def openMultipleFilesDialog(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDF files", "", "PDF Files (*.pdf)")
        if files:
            self.filesToMerge = files
            self.mergeFileLineEdit.setText('; '.join(files))  # 显示所选文件路径

    def splitPDF(self):
        sourcePath = self.fileLineEdit.text()
        savePath = self.saveLineEdit.text()
        pagesRanges = self.pagesLineEdit.text()

        if not self.isValidPageRanges(pagesRanges):
            QMessageBox.critical(self, 'wrong', 'invalid format, ranges like:1-3, 5-6')
            return

        try:
            pdf_splitter = PDFSplitter(sourcePath, savePath)
            for rangeStr in pagesRanges.split(','):
                start, end = map(int, rangeStr.strip().split('-'))
                pdf_splitter.add_range(start - 1, end - 1)
            pdf_splitter.split()
            QMessageBox.information(self, 'yes', 'DPDF!')
        except Exception as e:
            QMessageBox.critical(self, 'wrong', f'0.0: {e}')

    def isValidPageRanges(self, ranges):
        # 使用正则表达式来验证输入格式
        pattern = r'^(\d+-\d+\s*)(,\s*\d+-\d+\s*)*$'
        return re.match(pattern, ranges) is not None
   


    def mergePDF(self):
        if not self.filesToMerge:
            QMessageBox.warning(self, 'Warning', 'No PDF files selected to merge.')
            return

        save_path = self.savePathLineEdit.text()  # 获取用户选择的保存路径
        if not save_path:
            QMessageBox.warning(self, 'Warning', 'Please select a save path.')
            return

        try:
            pdf_merger = PDFMerger()
            for pdf_file in self.filesToMerge:
                pdf_merger.add_pdf(pdf_file)  # 添加PDF文件到合并器

            pdf_merger.merge(save_path)  # 合并PDF并保存
            QMessageBox.information(self, 'Success', 'PDFs merged successfully!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PDFApp()
    ex.show()
    sys.exit(app.exec_())
