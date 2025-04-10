import sys
import os
import wx
import logging #TODO Implementar Logging: timestamp da alteração e o que foi alterado.
# Adiciona o diretório 'src' ao sys.path para importar os módulos corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from views.main_window import MainWindow

if __name__ == '__main__':
    app = wx.App()
    main_window = MainWindow(None, "GesCol - Gestão de Equipamentos Logísticos")
    main_window.Show()
    app.MainLoop()

"""TODO: Talvez seja uma boa ideia colocar alguma forma de login
para saber quem fez cada alteração observada no logging.
Fazer logging de forma inteligente, semelhante ao Chibaku.
            Talvez estudar melhor a estrutura de um bom log.
"""