import wx

from .tab_atribuicoes import TabAtribuicoes
from .tab_colaboradores import TabColaboradores
from .tab_coletores import TabColetores
from .tab_empilhadeiras import TabEmpilhadeiras
from .tab_equipamentos import TabEquipamentos
from .tab_relatorios import TabRelatorios
from .tab_transpaleteiras import TabTranspaleteiras


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 600))

        self.notebook = wx.Notebook(self)

        self.tab_colaboradores = TabColaboradores(self.notebook)
        self.tab_coletores = TabColetores(self.notebook)
        self.tab_empilhadeiras = TabEmpilhadeiras(self.notebook)
        self.tab_transpaleteiras = TabTranspaleteiras(self.notebook)
        self.tab_atribuicoes = TabAtribuicoes(self.notebook)
        self.tab_relatorios = TabRelatorios(self.notebook)
        self.tab_equipamentos = TabEquipamentos(self.notebook)

        self.notebook.AddPage(self.tab_coletores, 'Coletores')
        self.notebook.AddPage(self.tab_colaboradores, 'Colaboradores')
        self.notebook.AddPage(self.tab_atribuicoes, 'Atribuições')
        self.notebook.AddPage(self.tab_relatorios, 'Relatórios')
        self.notebook.AddPage(self.tab_equipamentos, 'Equipamentos')
        # self.notebook.AddPage(self.tab_empilhadeiras, "Empilhadeiras")
        # self.notebook.AddPage(self.tab_transpaleteiras, "Transpaleteiras")

        self.CreateStatusBar()
        self.SetStatusText('Bem-vindo ao GesCol!')

        self.Centre()


if __name__ == '__main__':
    app = wx.App()
    main_win = MainWindow(None, 'GesCol - Sistema de Gestão')
    main_win.Show()
    app.MainLoop()
