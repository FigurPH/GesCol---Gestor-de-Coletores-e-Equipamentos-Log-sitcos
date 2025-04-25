import wx
from controllers import relatorios_controller


class TabRelatorios(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.relatorio_lista = []
        self.controller = relatorios_controller

        # --- Sizer principal ---
        main_sizer = wx.BoxSizer(wx.VERTICAL)


        # --- Seção de superior de estatísticas ---
        stats_sizer = wx.BoxSizer(wx.HORIZONTAL)
        colaboradores_ativos = wx.StaticText(self, label='Colaboradores Ativos: ')
        self.lbl_colaboradores_ativos = wx.StaticText(self, label='0')
        coletores_atribuidos = wx.StaticText(self, label='Coletores Atribuídos: ')
        self.lbl_coletores_atribuidos = wx.StaticText(self, label='0')
        transpaleteiras_atribuidas = wx.StaticText(self, label='Transpaleteiras Atribuídas: ')
        self.lbl_transpaleteiras_atribuidas = wx.StaticText(self, label='0')
        empilhadeiras_atribuidas = wx.StaticText(self, label='Empilhadeiras Atribuídas: ')
        self.lbl_empilhadeiras_atribuidas = wx.StaticText(self, label='0')


        # Adicionando cada elemento à janela
        for stat in [
            colaboradores_ativos, self.lbl_colaboradores_ativos,
            coletores_atribuidos, self.lbl_coletores_atribuidos,
            transpaleteiras_atribuidas, self.lbl_transpaleteiras_atribuidas,
            empilhadeiras_atribuidas, self.lbl_empilhadeiras_atribuidas

        ]: stats_sizer.Add(stat, 0, wx.ALL, 5)
        main_sizer.Add(stats_sizer, 0, wx.EXPAND)


        # --- Seção de pesquisa/busca ---
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Filtros
        matricula_label = wx.StaticText(self, label="Matrícula:")
        self.matricula_field = wx.TextCtrl(self)
        search_sizer.Add(matricula_label, 0, wx.ALL|wx.CENTER, 5)
        search_sizer.Add(self.matricula_field, 1, wx.ALL, 5)
        
        colaborador_label = wx.StaticText(self, label="Colaborador:")
        self.colaborador_field = wx.TextCtrl(self)
        search_sizer.Add(colaborador_label, 0, wx.ALL|wx.CENTER, 5)
        search_sizer.Add(self.colaborador_field, 1, wx.ALL, 5)
        
        equipamento_label = wx.StaticText(self, label="Equipamento:")
        self.equipamento_field = wx.TextCtrl(self)
        search_sizer.Add(equipamento_label, 0, wx.ALL|wx.CENTER, 5)
        search_sizer.Add(self.equipamento_field, 1, wx.ALL, 5)
        
        self.btn_filtrar = wx.Button(self, label="Filtrar")
        search_sizer.Add(self.btn_filtrar, 0, wx.ALL, 5)
        
        main_sizer.Add(search_sizer, 0, wx.EXPAND|wx.ALL, 5)



        # --- Seção do relatório ---
        self.list_ctrl = wx.ListCtrl(
            self,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SINGLE_SEL,
        )
        self.list_ctrl.InsertColumn(0, "Matrícula", width=100)
        self.list_ctrl.InsertColumn(1, "Colaborador", width=200)
        self.list_ctrl.InsertColumn(2, "Coletor ID", width=80)
        self.list_ctrl.InsertColumn(3, "Transpaleteira ID", width=200)
        self.list_ctrl.InsertColumn(4, "Empilhadeira ID", width=200)
        self.list_ctrl.InsertColumn(5, "Data Atribuição", width=200)
        
        main_sizer.Add(self.list_ctrl, 1, wx.EXPAND|wx.ALL, 5)
        

        # --- Inicialização ---
        #self.carregar_conteudo()
        


        # --- Bindings ---
        self.btn_filtrar.Bind(wx.EVT_BUTTON, self.on_filtrar)
        self.SetSizer(main_sizer)
        


    def on_filtrar(self, event=None):
        # Add a counter attribute if it doesn't exist
        if not hasattr(self, 'counter'):
            self.counter = 0
            
        # Lambda function to increment counter
        increment = lambda x: x + 1
        self.counter = increment(self.counter)
        
        self.colaboradores_ativos.SetLabel(f'Colaboradores Ativos: {self.counter}')


