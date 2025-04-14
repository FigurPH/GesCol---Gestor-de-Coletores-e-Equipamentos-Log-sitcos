import wx

from src.controllers import equipamentos_controller


class TabEquipamentos(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.equipamentos_lista = []
        self.controller = equipamentos_controller

        # --- Elementos da Interface ---
        self.list_ctrl = wx.ListCtrl(
            self,
            style=wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL,
        )

        # Criação das colunas ID, modelo, tipo (Emp. | Trp.), disponível
        self.list_ctrl.InsertColumn(0, 'Núm. Equipamento', width=150)
        self.list_ctrl.InsertColumn(1, 'Modelo', width=150)
        self.list_ctrl.InsertColumn(2, 'Tipo', width=100)
        self.list_ctrl.InsertColumn(3, 'Disponível', width=100)

        self.btn_adicionar = wx.Button(self, label='Adicionar')
        self.btn_editar = wx.Button(self, label='Editar')
        self.btn_excluir = wx.Button(self, label='Excluir')
        self.btn_atualizar = wx.Button(self, label='Atualizar Lista')
        self.btn_upload_csv = wx.Button(self, label='...')

        # --- Layout ---
        sizer_principal = wx.BoxSizer(wx.VERTICAL)
        sizer_botoes = wx.BoxSizer(wx.HORIZONTAL)

        sizer_botoes.Add(self.btn_adicionar, 0, wx.ALL, 5)
        sizer_botoes.Add(self.btn_editar, 0, wx.ALL, 5)
        sizer_botoes.Add(self.btn_excluir, 0, wx.ALL, 5)
        sizer_botoes.Add(self.btn_atualizar, 0, wx.ALL, 5)
        sizer_botoes.AddStretchSpacer()
        sizer_botoes.Add(self.btn_upload_csv, 0, wx.ALL, 5)

        sizer_principal.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 10)
        sizer_principal.Add(sizer_botoes, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(sizer_principal)

        # --- Captura de Eventos ---
        self.btn_adicionar.Bind(wx.EVT_BUTTON, self.on_adicionar_equipamento)
        self.btn_editar.Bind(wx.EVT_BUTTON, self.on_editar_equipamento)
        self.btn_excluir.Bind(wx.EVT_BUTTON, self.on_excluir_equipamento)
        self.btn_atualizar.Bind(wx.EVT_BUTTON, self.on_atualizar_lista)
        self.list_ctrl.Bind(
            wx.EVT_LIST_ITEM_ACTIVATED, self.on_editar_equipamento
        )   # Clique duplo na linha da lista
        self.list_ctrl.Bind(
            wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected
        )   # Seleção de item na lista
        self.list_ctrl.Bind(
            wx.EVT_LIST_ITEM_DESELECTED, self.on_item_deselected
        )

        # --- Inicialiação dos Widgets ---
        self.carregar_equipamentos()
        self.atualizar_estado_botoes()

    def on_adicionar_equipamento(self, event=None):
        dialog = AdicionarEquipamentoDialog(self)
        if dialog.ShowModal() == wx.ID_OK:
            numero = dialog.txt_numero.GetValue()
            modelo = dialog.txt_modelo.GetValue()
            tipo = dialog.cb_tipo.GetValue()
            disponivel = dialog.cb_disponivel.GetValue()
            if numero:
                print(f'Número: {numero}', 
                      f'Modelo: {modelo}',
                      f'Tipo: {tipo}',
                      f'Disponível: {disponivel}') #FUncionando até aqui. #TODO Terminar aqui

            # Adiciona o equipamento usando o controller
            '''self.controller.adicionar_equipamento(
                numero, modelo, tipo, disponivel
            )
            self.carregar_equipamentos()'''
        dialog.Destroy()

    def on_editar_equipamento(self, event=None): ...

    def on_excluir_equipamento(self, event=None): ...

    def on_atualizar_lista(self, event=None):
        self.atualizar_estado_botoes()
        self.carregar_equipamentos()

    def on_item_selected(self, event=None): ...

    def on_item_deselected(self, event=None): ...

    def atualizar_estado_botoes(self, event=None): ...

    def carregar_equipamentos(self, event=None): ...


class AdicionarEquipamentoDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title='Adicionar Equipamento', size=(400, 300))

        # --- Elementos da Interface ---
        self.txt_numero = wx.TextCtrl(self)
        self.txt_modelo = wx.TextCtrl(self)
        self.cb_disponivel = wx.CheckBox(self, label='Disponível')
        self.cb_disponivel.SetValue(True)
        self.cb_tipo = wx.ComboBox(
            self,
            choices=['Empilhadeira', 'Transpaleteira'],
            style=wx.CB_READONLY,
        )

        self.btn_salvar = wx.Button(self, wx.ID_OK, label='Salvar')
        self.btn_cancelar = wx.Button(self, wx.ID_CANCEL, label='Cancelar')

        # --- Layout ---
        sizer_principal = wx.BoxSizer(wx.VERTICAL)
        sizer_campos = wx.FlexGridSizer(rows=4, cols=2, hgap=5, vgap=5)

        sizer_checkboxes = wx.BoxSizer(wx.VERTICAL)
        size_botoes = wx.BoxSizer(wx.HORIZONTAL)

        sizer_campos.AddMany([
            (wx.StaticText(self, label='Número do Equipamento'), 0, 
             wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL),
            (self.txt_numero, 0, wx.EXPAND),
            (wx.StaticText(self, label='Modelo'), 0,
             wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL),
            (self.txt_modelo, 0, wx.EXPAND),
            (wx.StaticText(self, label='Tipo'), 0,
             wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL),
            (self.cb_tipo, 0, wx.EXPAND),
            (self.cb_disponivel, 0, wx.EXPAND),
            (wx.StaticText(self, label=''), 0,),  # Espaço vazio
        ])

        size_botoes.Add(self.btn_salvar, 0, wx.ALL, 5)
        size_botoes.Add(self.btn_cancelar, 0, wx.ALL, 5)

        sizer_principal.Add(sizer_campos, 0, wx.EXPAND | wx.ALL, 10)
        sizer_principal.Add(size_botoes, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.SetSizer(sizer_principal)
        self.Fit()
