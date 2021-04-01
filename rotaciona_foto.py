# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RotacionaFoto
                                 A QGIS plugin
 Plugin que rotaciona imagens em ângulos de 90, 180 e 270 graus.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-03-17
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Jackson Oliveira/Topocart
        email                : jackend.dev@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import re
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from PyQt5.QtWidgets import QWidget, QPushButton, QRadioButton, QLabel, QProgressBar, QComboBox, QMessageBox
from PIL import Image

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .rotaciona_foto_dialog import RotacionaFotoDialog
from .foto_fachada_dialog import FotoFachadaDialog
import os.path
from qgis.core import Qgis, QgsMessageLog

class External(QThread):
    def __init__(self, entrada_dir, saida_dir, valor_angulo):
        QThread.__init__(self)
        self.entrada_dir = entrada_dir
        self.saida_dir = saida_dir
        self.valor_angulo = valor_angulo
    """
    Runs a counter thread.
    """
    valor_porcentagem = pyqtSignal(int)
    valor_contador = pyqtSignal(int)
    nome_arquivos = pyqtSignal(str)
    mensagem_erro = pyqtSignal(bool)

    def run(self):
        # Verifique se existe arquivos de imagens
        cont = 0
        contador = 0
        for qtd_img in os.listdir(self.entrada_dir):
            if re.search('\\.jpg\\b', qtd_img, re.IGNORECASE) or re.search('\\.png\\b', qtd_img, re.IGNORECASE)\
                    or re.search('\\.jpeg\\b', qtd_img, re.IGNORECASE):
                contador += 1
        if contador == 0:
            # Mostre a mensagem de erro
            exibir_mensagem = True
        else:
            # Inicie o processo de percorrer os arquivos, rotacionar e salvar no diretório de saída
            for arq in os.listdir(self.entrada_dir):
                tipo_arq = arq.split('.')
                if (tipo_arq[len(tipo_arq) - 1].upper() == 'PNG' or tipo_arq[len(tipo_arq) - 1].upper() == 'JPG'
                        or tipo_arq[len(tipo_arq) - 1].upper() == 'JPEG'):

                    img = Image.open('{}/{}'.format(self.entrada_dir, arq))
                    angulo = self.valor_angulo
                    out = img.rotate(angulo, expand=True)
                    out.save('{}/{}.jpg'.format(self.saida_dir, tipo_arq[0]))

                    cont += 1
                    porcentagem = cont / contador * 100
    # Emitir os sinais para a classe RotacionaFoto:
                    self.valor_porcentagem.emit(porcentagem)
                    self.nome_arquivos.emit(arq)

            self.valor_contador.emit(contador)
        self.mensagem_erro.emit(exibir_mensagem)


class RotacionaFoto:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'RotacionaFoto_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Rotaciona Foto')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('RotacionaFoto', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/rotaciona_foto/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Rotaciona Foto'),
                action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            # self.first_start = False
            self.dlg = RotacionaFotoDialog()
            self.foto = FotoFachadaDialog()

        # show the dialog
        self.dlg.show()

        # Inicialize as variaveis de acordo com a GUI
        diretorio_origem  = self.dlg.findChild(QgsFileWidget, "dir_entrada")
        diretorio_destino = self.dlg.findChild(QgsFileWidget, "dir_saida")
        btn_img_original = self.dlg.findChild(QPushButton, "btn_imagem_original")
        btn_iniciar = self.dlg.findChild(QPushButton, "btn_iniciar")
        btn_preview = self.dlg.findChild(QPushButton, "btn_preview")
        btn_cancelar = self.dlg.findChild(QPushButton, "btn_cancelar")
        comboBox_angulo = self.dlg.findChild(QComboBox, "comboBox_grau")
        lbl_nome_imagem = self.dlg.findChild(QLabel, "label_nome_foto")
        barra_progresso = self.dlg.findChild(QProgressBar, "progressBar")

        # Retorne o valor do ângulo quando o comboBox for alterado
        def retornar_valor_comboBox():
            if comboBox_angulo.currentText() == "90º":
                return 270
            if comboBox_angulo.currentText() == "180º":
                return 180
            if comboBox_angulo.currentText() == "270º":
                return 90

        # Inicie o processo de rotação
        def iniciar():
            iniciar_progresso(self)
            # Ative o botão de cancelar quando o processo for iniciado
            btn_cancelar.setEnabled(True)

        # Inicie a thread e a barra de progresso
        def iniciar_progresso(self):
            qtd_rotacao = retornar_valor_comboBox()

            # Inicialize a variavel com a classe External(QThread)
            self.calc = External(diretorio_origem.filePath(), diretorio_destino.filePath(), qtd_rotacao)

            self.calc.valor_porcentagem.connect(difinir_valor_porcentagem)
            self.calc.valor_contador.connect(exibir_mensagem_qtd)
            self.calc.nome_arquivos.connect(exibir_nome_arquivos)
            self.calc.mensagem_erro.connect(exibir_mensagem_erro)
            self.calc.start()

        # Define o valor da porcentagem na barra de progresso
        def difinir_valor_porcentagem(valor):
            barra_progresso.setValue(valor)

        # Exibe mensagem de conclusão e a quantidade de imagens rotacionadas
        def exibir_mensagem_qtd(qtd):
            iface.messageBar().pushMessage("Concluído", f"{qtd} imagens rotacionadas com sucesso!",
                                           level=Qgis.Success)
            QMessageBox.information(None, f"Concluído", f"{qtd} imagens rotacionadas.")

        # Define o nomes dos arquivos na GUI
        def exibir_nome_arquivos(arq):
            lbl_nome_imagem.setText(arq)

        # Exibir mensagem de erro quando não existe arquivos no diretório de entrada
        def exibir_mensagem_erro(bool):
            if bool == True:
                iface.messageBar().pushMessage("Erro", "Nenhum arquivo de imagem foi encontrado no "
                                                        "diretório selecionado!",
                                               level=Qgis.Critical)
        # Exibir imagem preliminar antes de iniciar o processo
        def preview_imagem():
            # Verifique se existe arquivos de imagens
            contador = 0
            for qtd_img in os.listdir(diretorio_origem.filePath()):
                if re.search('\\.jpg\\b', qtd_img, re.IGNORECASE) or re.search('\\.png\\b', qtd_img, re.IGNORECASE) \
                        or re.search('\\.jpeg\\b', qtd_img, re.IGNORECASE):
                    contador += 1
            if contador == 0:
                exibir_mensagem_erro(True)
            else:
                # Inicie o processo de percorrer os arquivos
                qtd_rotacao = retornar_valor_comboBox()
                caminho_temp = "C:\\Users\\{}\\AppData\\Local\\Temp".format(os.getlogin())

                arquivo = None
                while arquivo == None:
                    for arq in os.listdir(diretorio_origem.filePath()):
                        if re.search('\\.jpg\\b', arq, re.IGNORECASE) or re.search('\\.png\\b', arq, re.IGNORECASE) \
                                or re.search('\\.jpeg\\b', arq, re.IGNORECASE):
                            arquivo = arq

                #  Rotacione a imagem preliminar para salvar no diretório temporário
                img = Image.open('{}/{}'.format(diretorio_origem.filePath(), arquivo))
                angulo = qtd_rotacao
                out = img.rotate(angulo, expand=True)
                out.save('{}\preview.jpg'.format(caminho_temp))

                # Exibir a imagem preliminar
                path_file = '{}\preview.jpg'.format(caminho_temp)
                # print("img", path_file)
                self.foto.label.setPixmap(QtGui.QPixmap(path_file))
                self.foto.show()

        # Exibir a imagem original do diretório de entrada
        def exibir_img_original():
            contador = 0
            for qtd_img in os.listdir(diretorio_origem.filePath()):
                if re.search('\\.jpg\\b', qtd_img, re.IGNORECASE) or re.search('\\.png\\b', qtd_img, re.IGNORECASE) \
                        or re.search('\\.jpeg\\b', qtd_img, re.IGNORECASE):
                    contador += 1
            if contador == 0:
                exibir_mensagem_erro(True)
            else:
                arquivo = None
                while arquivo == None:
                    for arq in os.listdir(diretorio_origem.filePath()):
                        if re.search('\\.jpg\\b', arq, re.IGNORECASE) or re.search('\\.png\\b', arq, re.IGNORECASE)\
                                or re.search('\\.jpeg\\b', arq, re.IGNORECASE):
                            arquivo = arq

                path_file = '{}\{}'.format(diretorio_origem.filePath(), arquivo)
                # print("img", path_file)
                self.foto.label.setPixmap(QtGui.QPixmap(path_file))
                self.foto.show()

        # Ative os botões após definir diretório de entrada e saída
        def ativar_btns():
            tamanho_dir_origem = int(len(diretorio_origem.filePath()))
            tamanho_dir_destino = int(len(diretorio_destino.filePath()))

            if not tamanho_dir_origem > 0:
                btn_img_original.setEnabled(False)
                btn_preview.setEnabled(False)
                btn_iniciar.setEnabled(False)
            elif not tamanho_dir_destino > 0:
                btn_iniciar.setEnabled(False)
            else:
                btn_img_original.setEnabled(True)
                btn_preview.setEnabled(True)
                btn_iniciar.setEnabled(True)

        # Pare a thread e a barra de progresso
        def parar_progresso():
            self.calc.terminate()

        # Cancele o progresso
        def cancelar(self):
            parar_progresso()

        # Sinalize os botões de acordo com cada função
        comboBox_angulo.currentTextChanged.connect(retornar_valor_comboBox)
        btn_iniciar.clicked.connect(iniciar)
        btn_preview.clicked.connect(preview_imagem)
        btn_img_original.clicked.connect(exibir_img_original)
        btn_cancelar.clicked.connect(cancelar)
        diretorio_origem.fileChanged.connect(ativar_btns)
        diretorio_destino.fileChanged.connect(ativar_btns)
        diretorio_origem.fileChanged.connect(exibir_mensagem_erro)
