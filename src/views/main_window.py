import wx

# Importação das classes de abas específicas
from .tab_atribuicoes import TabAtribuicoes
from .tab_colaboradores import TabColaboradores
from .tab_coletores import TabColetores
from .tab_relatorios import TabRelatorios

from src.resources.logger import logger
#@logger(log_level=1)
class MainWindow(wx.Frame):
    """
    Classe principal da janela do sistema GesCol.

    Esta classe representa a janela principal do sistema, que contém um
    notebook com várias abas para gerenciar diferentes aspectos do sistema,
    como coletores, colaboradores, atribuições, relatórios e equipamentos.

    Args:
        parent (wx.Window): O componente pai da janela principal.
        title (str): O título da janela principal.
    """

    def __init__(self, parent, title):
        """
        Inicializa a janela principal do sistema.

        Cria um notebook e adiciona as abas correspondentes às funcionalidades
        do sistema.

        Args:
            parent (wx.Window): O componente pai da janela principal.
            title (str): O título da janela principal.
        """
        super().__init__(parent, title=title, size=(800, 600))

        # Criação do notebook para organizar as abas
        self.notebook = wx.Notebook(self)

        # Inicialização das abas
        self.tab_atribuicoes = TabAtribuicoes(self.notebook)
        self.tab_colaboradores = TabColaboradores(self.notebook)
        self.tab_relatorios = TabRelatorios(self.notebook)
        # self.tab_equipamentos = TabEquipamentos(self.notebook)
        self.tab_coletores = TabColetores(self.notebook)
        # As abas abaixo estão comentadas, mas podem ser ativadas se necessário
        # self.tab_empilhadeiras = TabEmpilhadeiras(self.notebook)
        # self.tab_transpaleteiras = TabTranspaleteiras(self.notebook)

        # Adiciona as abas ao notebook
        self.notebook.AddPage(self.tab_atribuicoes, 'Atribuições')
        # -*
        # +elf.tab_atribuicoes.Bind(wx.EVT_SHOW, lambda x: self.tab_atribuicoes.limpa_tela())
        self.notebook.AddPage(self.tab_relatorios, 'Relatórios')
        self.tab_relatorios.Bind(wx.EVT_SHOW, lambda x: self.tab_relatorios.atualizar_tela())
        self.notebook.AddPage(self.tab_colaboradores, 'Colaboradores')
        self.tab_colaboradores.Bind(wx.EVT_SHOW, lambda x: self.tab_colaboradores.on_atualizar_lista())
        # self.notebook.AddPage(self.tab_equipamentos, 'Equipamentos')
        self.notebook.AddPage(self.tab_coletores, 'Coletores')
        self.tab_coletores.Bind(wx.EVT_SHOW, lambda x: self.tab_coletores.on_atualizar_lista())

        # self.notebook.AddPage(self.tab_empilhadeiras, "Empilhadeiras")
        # self.notebook.AddPage(self.tab_transpaleteiras, "Transpaleteiras")

        # Cria uma barra de status na parte inferior da janela
        self.CreateStatusBar()
        self.SetStatusText('Bem-vindo ao GesCol!            |              v0.9.1')

        # Centraliza a janela na tela
        self.Centre()


if __name__ == '__main__':
    """
    Ponto de entrada do programa.

    Cria e exibe a janela principal do sistema GesCol.
    """
    app = wx.App()
    main_win = MainWindow(None, 'GesCol - Sistema de Gestão')
    main_win.Show()
    app.MainLoop()
