import wx

from controllers import atribuicao_controller

class TabAtribuicoes(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.atribuicao_lista = []
        self.controller = atribuicao_controller

        # --- Layout Principal ---
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # --- Linha Superior: Campo de ID e Botão Buscar ---
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.matricula = wx.TextCtrl(self, size=(200, -1), name="matricula")
        self.matricula.SetHint("Matrícula")
        self.matricula.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.btn_buscar = wx.Button(self, label="Buscar", name="btn_buscar")
        search_sizer.Add(self.matricula, 0, wx.ALL, 5)
        search_sizer.Add(self.btn_buscar, 0, wx.ALL, 5)
        main_sizer.Add(search_sizer, 0, wx.EXPAND)

        # --- Informações do Colaborador ---
        colaborador_sizer = wx.StaticBoxSizer(wx.StaticBox(self, label=""), wx.VERTICAL)
        self.lbl_nome = wx.StaticText(self, label="Nome")
        # self.lbl_nome.SetLabelText("Xuleipa") # usar essa abordagem para atribuir valor
        self.lbl_cargo = wx.StaticText(self, label="Cargo")
        colaborador_sizer.Add(self.lbl_nome, 0, wx.ALL, 5)
        colaborador_sizer.Add(self.lbl_cargo, 0, wx.ALL, 5)

        # --- Linha do Coletor ---
        coletor_sizer = wx.BoxSizer(wx.HORIZONTAL)
        coletor_label = wx.StaticText(self, label="Coletor:")
        self.txt_coletor_id = wx.TextCtrl(self, size=(150, -1), name="coletor_id")
        self.btn_atribuir_coletor = wx.Button(self, label="Atribuir", name="btn_atribuir_coletor")
        self.data_coletor = wx.StaticText(self, label="data_coletor")
        coletor_sizer.Add(coletor_label, 0, wx.ALL, 5)
        coletor_sizer.Add(self.txt_coletor_id, 0, wx.ALL, 5)
        coletor_sizer.Add(self.btn_atribuir_coletor, 0, wx.ALL, 5)
        coletor_sizer.Add(self.data_coletor, 0, wx.ALL, 5)
        colaborador_sizer.Add(coletor_sizer, 0, wx.EXPAND)

        main_sizer.Add(colaborador_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # --- Equipamentos ---
        equipamentos_sizer = wx.StaticBoxSizer(wx.StaticBox(self, label="Equipamentos"), wx.VERTICAL)

        # Linha da Transpaleteira
        transpaleteira_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_transpaleteira = wx.CheckBox(self, label="Transpaleteira")
        self.txt_transpaleteira_id = wx.TextCtrl(self, size=(150, -1), name="txt_transpaleteira_id")
        self.btn_atribuir_transpaleteira = wx.Button(self, label="Atribuir", name="btn_atribuir_transpaleteira")
        self.data_transpaleteira = wx.StaticText(self, label="data_transpaleteira")
        transpaleteira_sizer.Add(self.cb_transpaleteira, 0, wx.ALL, 5)
        transpaleteira_sizer.Add(self.txt_transpaleteira_id, 0, wx.ALL, 5)
        transpaleteira_sizer.Add(self.btn_atribuir_transpaleteira, 0, wx.ALL, 5)
        transpaleteira_sizer.Add(self.data_transpaleteira, 0, wx.ALL, 5)
        equipamentos_sizer.Add(transpaleteira_sizer, 0, wx.EXPAND)

        # Linha da Empilhadeira
        empilhadeira_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_empilhadeira = wx.CheckBox(self, label="Empilhadeira")
        self.txt_empilhadeira_id = wx.TextCtrl(self, size=(150, -1), name="txt_empilhadeira_id")
        self.btn_atribuir_empilhadeira = wx.Button(self, label="Atribuir", name="btn_atribuir_empilhadeira")
        self.data_empilhadeira = wx.StaticText(self, label="data_empilhadeira")
        empilhadeira_sizer.Add(self.cb_empilhadeira, 0, wx.ALL, 5)
        empilhadeira_sizer.Add(self.txt_empilhadeira_id, 0, wx.ALL, 5)
        empilhadeira_sizer.Add(self.btn_atribuir_empilhadeira, 0, wx.ALL, 5)
        empilhadeira_sizer.Add(self.data_empilhadeira, 0, wx.ALL, 5)
        equipamentos_sizer.Add(empilhadeira_sizer, 0, wx.EXPAND)

        main_sizer.Add(equipamentos_sizer, 0, wx.EXPAND | wx.ALL, 10)


        # --- Botões e campos iniciam desativados ---
        self.txt_coletor_id.Disable()
        self.btn_atribuir_coletor.Disable()
        self.txt_transpaleteira_id.Disable()
        self.btn_atribuir_transpaleteira.Disable()
        self.txt_empilhadeira_id.Disable()
        self.btn_atribuir_empilhadeira.Disable()
        self.cb_transpaleteira.Disable()
        self.cb_empilhadeira.Disable()
        self.data_coletor.Hide()
        self.data_transpaleteira.Hide()
        self.data_empilhadeira.Hide()
        

        # --- Configuração Final ---
        self.SetSizer(main_sizer)

        # --- Bindings ---
        self.btn_buscar.Bind(wx.EVT_BUTTON, self.on_buscar_colaborador)
        self.btn_atribuir_coletor.Bind(wx.EVT_BUTTON,
                                       lambda x: self.atribuir_equipamento('coletor'))
        self.btn_atribuir_transpaleteira.Bind(wx.EVT_BUTTON,
                                              lambda x: self.atribuir_equipamento('transpaleteira'))
        self.btn_atribuir_empilhadeira.Bind(wx.EVT_BUTTON,
                                            lambda x: self.atribuir_equipamento('empilhadeira'))



    def on_buscar_colaborador(self, evet=None):
        colaborador = atribuicao_controller.carregar_informacoes_colaborador(self.matricula.GetValue())
        self.lbl_nome.SetLabelText(colaborador.nome)
        self.lbl_cargo.SetLabelText(colaborador.cargo)
        self.btn_atribuir_coletor.Enable()
        if colaborador.autorizado_transpaleteira:
            self.cb_transpaleteira.SetValue(True)
            self.btn_atribuir_transpaleteira.Enable()
        if colaborador.autorizado_empilhadeira:
            self.cb_empilhadeira.SetValue(True)
            self.btn_atribuir_empilhadeira.Enable()


    def on_atribuir_coletor(self, evet=None):...

    def on_atribuir_transpaleteira(self, evet=None):...

    def on_atribuir_empilhadeira(self, evet=None):...

    def atribuir_equipamento(self, tipo_equipamento):
        match tipo_equipamento:
            case 'coletor':
                print('É um coletor')

            case 'transpaleteira':
                print('É uma transpaleteira')
                
            case 'empilhadeira':
                print('É uma empilhadeira')




