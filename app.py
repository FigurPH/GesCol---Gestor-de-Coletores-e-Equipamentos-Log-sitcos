import os
import sys

import wx

# Adiciona o diretório 'src' ao sys.path para importar os módulos corretamente
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
)

# Verifica se o parâmetro DEBUG foi passado como argumento
DEBUG = '--debug' in sys.argv

from views.main_window import MainWindow


if __name__ == '__main__':
    app = wx.App()
    main_window = MainWindow(
        None, 'GesCol - Gestão de Equipamentos Logísticos'
    )
    if not DEBUG:
        main_window.SetWindowStyle(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        main_window.Maximize()
    main_window.Show()

    app.MainLoop()


"""TODO: Talvez seja uma boa ideia colocar alguma forma de login
para saber quem fez cada alteração observada no logging.
Fazer logging de forma inteligente, semelhante ao Chibaku.
            Talvez estudar melhor a estrutura de um bom log.
"""
