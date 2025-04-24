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
            wx.EVT_LIST_ITEM_SELECTED, lambda event: self.atualizar_estado_botoes()
        )   # Seleção de item na lista
        self.list_ctrl.Bind(
            wx.EVT_LIST_ITEM_DESELECTED, lambda event: self.atualizar_estado_botoes()
        )

        # --- Inicialiação dos Widgets ---
        self.carregar_equipamentos()
        self.atualizar_estado_botoes()

    def on_adicionar_equipamento(self, event=None):
        dialog = AdicionarEquipamentoDialog(self)

        @staticmethod
        def _showMessageBox(tipo_equipamento):
            wx.MessageBox(
                f'{tipo_equipamento} adicionada com sucesso!',
                'Sucesso',
                wx.OK | wx.ICON_INFORMATION,
            )
            self.carregar_equipamentos()

        if dialog.ShowModal() == wx.ID_OK:
            numero = dialog.txt_numero.GetValue()
            modelo = dialog.txt_modelo.GetValue()
            tipo = dialog.cb_tipo.GetValue()
            disponivel = dialog.cb_disponivel.GetValue()

            if numero and modelo and tipo and disponivel is not None:
                # Verifica o tipo de equipamento e cria a instância correspondente
                if tipo == 'Empilhadeira':
                    empilhadeira = self.controller.empilhadeira_controller.adicionar_empilhadeira(
                        id=numero,
                        modelo=modelo,
                        disponibilidade=disponivel,
                    )
                    if empilhadeira: _showMessageBox(tipo_equipamento=str(tipo))

                elif tipo == 'Transpaleteira':
                    transpaleteira = self.controller.transpaleteira_controller.adicionar_transpaleteira(
                        id=numero,
                        modelo=modelo,
                        disponibilidade=disponivel,
                        )
                    if transpaleteira: _showMessageBox(tipo_equipamento=str(tipo))

                # Cria a instância do equipamento com os dados fornecidos

            else:
                print('Erro: Número, modelo, tipo e disponibilidade são obrigatórios.')
                wx.MessageBox(
                    'Erro: Todos os campos são obrigatórios.',
                    'Erro',
                    wx.OK | wx.ICON_ERROR,
                )
                self.on_adicionar_equipamento()
        dialog.Destroy()

    def on_editar_equipamento(self, event=None):
        select_idex = self.list_ctrl.GetFirstSelected()
        if select_idex != -1:
            id_equipamento = self.list_ctrl.GetItemText(select_idex, 0)
            tipo_equipamento = self.list_ctrl.GetItemText(select_idex, 2)

            if tipo_equipamento == 'Empilhadeira':
                empilhadeira = self.controller.empilhadeira_controller.buscar_empilhadeira(
                    id_equipamento
                )
                if empilhadeira:
                    dlg = EditarEquipamentoDialog(self, empilhadeira, tipo_equipamento)

                    @staticmethod
                    def _showMessageBox(tipo_equipamento, sucesso: bool):
                        if sucesso:
                            wx.MessageBox(
                                f'{tipo_equipamento} editada com sucesso!',
                                'Sucesso',
                                wx.OK | wx.ICON_INFORMATION,
                            )
                        else:
                            wx.MessageBox(
                                f'Erro ao editar a {tipo_equipamento}.',
                                'Erro',
                                wx.OK | wx.ICON_ERROR,
                            )

                    if dlg.ShowModal() == wx.ID_OK:
                        modelo = dlg.txt_modelo.GetValue()
                        disponibilidade = dlg.cb_disponivel.GetValue()

                        if self.controller.empilhadeira_controller.editar_empilhadeira(
                            id_equipamento, modelo, disponibilidade
                        ):
                            _showMessageBox(tipo_equipamento=str(tipo_equipamento), sucesso=True)
                            self.carregar_equipamentos()
                        else:
                            _showMessageBox(tipo_equipamento=str(tipo_equipamento), sucesso=False)
                    dlg.Destroy()
            self.atualizar_estado_botoes()

    def on_excluir_equipamento(self, event=None):
        selected_index = self.list_ctrl.GetFirstSelected()
        if selected_index != -1:
            equipamento_id = self.list_ctrl.GetItemText(selected_index, 0)
            equipamento = self.equipamentos_lista[selected_index]
            if equipamento['tipo'] == 'Empilhadeira':
                empilhadeira = self.controller.empilhadeira_controller.buscar_empilhadeira(
                    equipamento_id
                )
                if empilhadeira:
                    dlg = wx.MessageDialog(
                        self,
                        f'Deseja realmente excluir a empilhadeira {empilhadeira.id}?',
                        'Confirmação',
                        wx.YES_NO | wx.ICON_QUESTION,
                    )
                    if dlg.ShowModal() == wx.ID_YES:
                        self.controller.empilhadeira_controller.excluir_empilhadeira(
                            equipamento_id
                        )
                        wx.MessageBox(
                            'Empilhadeira excluída com sucesso!',
                            'Sucesso',
                            wx.OK | wx.ICON_INFORMATION,
                        )
                        self.carregar_equipamentos()
                    else:
                        wx.MessageBox(
                            f'Erro ao excluir a empilhadeira {equipamento_id}.',
                            'Cancelado',
                            wx.OK | wx.ICON_INFORMATION,
                        )
                    dlg.Destroy()

            elif equipamento['tipo'] == 'Transpaleteira':
                transpaleteira = self.controller.transpaleteira_controller.buscar_transpaleteira(
                    equipamento_id
                )
                if transpaleteira:
                    dlg = wx.MessageDialog(
                        self,
                        f'Deseja realmente excluir a transpaleteira {transpaleteira.id}?',
                        'Confirmação',
                        wx.YES_NO | wx.ICON_QUESTION,
                    )
                    if dlg.ShowModal() == wx.ID_YES:
                        self.controller.transpaleteira_controller.excluir_transpaleteira(
                            equipamento_id
                        )
                        wx.MessageBox(
                            'Empilhadeira excluída com sucesso!',
                            'Sucesso',
                            wx.OK | wx.ICON_INFORMATION,
                        )
                        self.carregar_equipamentos()
                    else:
                        wx.MessageBox(
                            f'Erro ao excluir a transpaleteira {equipamento_id}.',
                            'Cancelado',
                            wx.OK | wx.ICON_INFORMATION,
                        )
                    dlg.Destroy()

    def on_atualizar_lista(self, event=None):
        self.atualizar_estado_botoes()
        self.carregar_equipamentos()

    def atualizar_estado_botoes(self, event=None):
        tem_selecao = self.list_ctrl.GetFirstSelected() != -1
        self.btn_editar.Enable(tem_selecao)
        self.btn_excluir.Enable(tem_selecao)

    def carregar_equipamentos(self, event=None):
        self.list_ctrl.DeleteAllItems()
        self.equipamentos_lista = self.controller.listar_equipamentos()

        for index, equipamento in enumerate(self.equipamentos_lista):
            list_index = self.list_ctrl.InsertItem(
                index, str(equipamento['id']).zfill(3)
            )
            self.list_ctrl.SetItem(
                list_index, 1, equipamento['modelo']
            )
            self.list_ctrl.SetItem(
                list_index, 2, equipamento['tipo']
            )
            self.list_ctrl.SetItem(
                list_index, 3,
                'Sim' if equipamento['disponibilidade'] else 'Não'
            )


class AdicionarEquipamentoDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title='Adicionar Equipamento', size=(400, 300))

        # --- Elementos da Interface ---
        self.txt_numero = wx.TextCtrl(self)
        self.txt_modelo = wx.TextCtrl(self)
        self.cb_tipo = wx.ComboBox(
            self,
            choices=['Empilhadeira', 'Transpaleteira'],
            style=wx.CB_READONLY,
        )
        self.cb_disponivel = wx.CheckBox(self, label='Disponível')
        self.cb_disponivel.SetValue(True)

        self.btn_salvar = wx.Button(self, wx.ID_OK, label='Salvar')
        self.btn_cancelar = wx.Button(self, wx.ID_CANCEL, label='Cancelar')

        # --- Layout ---
        sizer_principal = wx.BoxSizer(wx.VERTICAL)
        sizer_campos = wx.FlexGridSizer(rows=5, cols=2, hgap=5, vgap=5)

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
            (sizer_checkboxes, 0, wx.EXPAND),
        ])

        size_botoes.Add(self.btn_salvar, 0, wx.ALL, 5)
        size_botoes.Add(self.btn_cancelar, 0, wx.ALL, 5)

        sizer_principal.Add(sizer_campos, 0, wx.EXPAND | wx.ALL, 10)
        sizer_principal.Add(size_botoes, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.SetSizer(sizer_principal)
        self.Fit()


class EditarEquipamentoDialog(wx.Dialog):
    def __init__(self, parent, equipamento, tipo_equipamento):
        super().__init__(parent, title='Editar Equipamento', size=(400, 300))
        self.equipamento = equipamento
        print(equipamento)

        # --- Elementos da Interface ---
        self.txt_numero = wx.TextCtrl(
            self,
            value=str(equipamento.id),
            style=wx.TE_READONLY,
        )  # Número do equipamento não pode ser editado
        self.txt_modelo = wx.TextCtrl(self, value=equipamento.modelo)
        self.cb_tipo = wx.ComboBox(
            self,
            choices=['Empilhadeira', 'Transpaleteira'],
            style=wx.CB_READONLY,
            value=tipo_equipamento,
        )  # Tipo não pode ser editado
        self.cb_disponivel = wx.CheckBox(self, label='Disponível')
        self.cb_disponivel.SetValue(equipamento.disponibilidade)

        self.btn_salvar = wx.Button(self, wx.ID_OK, label='Salvar')
        self.btn_cancelar = wx.Button(self, wx.ID_CANCEL, label='Cancelar')

        # --- Layout ---
        sizer_principal = wx.BoxSizer(wx.VERTICAL)
        sizer_campos = wx.FlexGridSizer(rows=5, cols=2, hgap=5, vgap=5)

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
            (sizer_checkboxes, 0, wx.EXPAND),
        ])

        size_botoes.Add(self.btn_salvar, 0, wx.ALL, 5)
        size_botoes.Add(self.btn_cancelar, 0, wx.ALL, 5)
        sizer_principal.Add(sizer_campos, 0, wx.EXPAND | wx.ALL, 10)
        sizer_principal.Add(size_botoes, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.SetSizer(sizer_principal)
        self.Fit()
