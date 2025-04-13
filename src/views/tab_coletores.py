import wx

from src.controllers import coletor_controller


class TabColetores(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.coletores_lista = []  # Criação da lista de coletores a serem exibidos
        self.controller = coletor_controller  # Referencia ao controller

        # --- Elementos da Interface ---
        self.list_ctrl = (
            wx.ListCtrl(  # Cria um elemento de lista controlado pelo wx
                self,
                style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SINGLE_SEL,
            )
        )
        # Criação das colunas ID, modelo, disponibilidade no elemento de lista
        self.list_ctrl.InsertColumn(0, 'Número Col.', width=100)
        self.list_ctrl.InsertColumn(1, 'Modelo Col.', width=100)
        self.list_ctrl.InsertColumn(2, 'Disponível', width=80)

        self.btn_adicionar = wx.Button(self, label='Adicionar')
        self.btn_editar = wx.Button(self, label='Editar')
        self.btn_excluir = wx.Button(self, label='Excluir')
        self.btn_atualizar = wx.Button(self, label='Atualizar Lista')
        self.btn_upload_csv = wx.Button(self, label='...')
        """
        #TODO fazer essa lógica aqui. Replicar depois em tab_colaborador.
        #INFO Manter essa anotação de ToDo até terminar todas TABS!
        """

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

        # --- Captura de eventos ---
        self.btn_adicionar.Bind(wx.EVT_BUTTON, self.on_adicionar_coletor)
        self.btn_editar.Bind(wx.EVT_BUTTON, self.on_editar_coletor)
        self.btn_excluir.Bind(wx.EVT_BUTTON, self.on_excluir_coletor)
        self.btn_atualizar.Bind(wx.EVT_BUTTON, self.on_atualizar_lista)
        self.list_ctrl.Bind(
            wx.EVT_LIST_ITEM_ACTIVATED, self.on_editar_coletor
        )  # Duplo clique
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        self.list_ctrl.Bind(
            wx.EVT_LIST_ITEM_DESELECTED, self.on_item_deselected
        )

        # --- Inicialização dos Widgets ---
        self.carregar_coletores()  # Carrega os coletores para exibição
        self.atualizar_estado_botoes()  # Atualiza os estados dos botões Editar e Excluir

    def on_atualizar_lista(self, event):
        self.atualizar_estado_botoes()
        self.carregar_coletores()

    def carregar_coletores(self):
        self.list_ctrl.DeleteAllItems()
        self.coletores_lista = self.controller.listar_coletores()
        for index, coletor in enumerate(self.coletores_lista):
            list_index = self.list_ctrl.InsertItem(
                index, str(coletor['id']).zfill(3)
            )
            self.list_ctrl.SetItem(list_index, 1, coletor['modelo'])
            self.list_ctrl.SetItem(
                list_index,
                2,
                'Sim' if coletor['disponibilidade'] else 'Não',
            )

    def atualizar_estado_botoes(self):
        """Atualiza o estado dos botões 'Editar' e 'Excluir' com base na seleção da lista."""
        tem_selecao = self.list_ctrl.GetFirstSelected() != -1
        self.btn_editar.Enable(tem_selecao)
        self.btn_excluir.Enable(tem_selecao)

    def on_item_selected(self, event):
        """Evento chamado quando um item da lista é selecionado."""
        self.atualizar_estado_botoes()

    def on_item_deselected(self, event):
        """Evento chamado quando um item da lista é deselecionado."""
        self.atualizar_estado_botoes()

    def on_adicionar_coletor(self, event=None):
        dlg = AdiconarColetorDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            numero = dlg.txt_numero.GetValue()
            modelo = dlg.txt_modelo.GetValue()
            disponivel = dlg.cb_disponivel.GetValue()
            coletor = self.controller.adicionar_coletor(
                id=numero,
                modelo=modelo,
                disponibilidade=disponivel,
            )

            if coletor:
                wx.MessageBox(
                    f'Coletor {numero} adicionado com sucesso!',
                    'Sucesso',
                    wx.OK | wx.ICON_INFORMATION,
                )
                self.carregar_coletores()
        dlg.Destroy()
        self.atualizar_estado_botoes()
        return True

    def on_editar_coletor(self, event):
        """Evento chamado ao clicar no botão 'Editar' ou dar duplo clique na lista."""
        select_index = self.list_ctrl.GetFirstSelected()
        if select_index != -1:
            id = self.list_ctrl.GetItemText(select_index, 0)
            coletor = self.controller.buscar_coletor(int(id))
            if coletor:
                dlg = EditarColetorDialog(self, coletor)
                if dlg.ShowModal() == wx.ID_OK:
                    numero = dlg.txt_numero.GetValue()
                    modelo = dlg.txt_modelo.GetValue()
                    disponivel = dlg.cb_disponivel.GetValue()

                    if self.controller.editar_coletor(
                        numero, modelo, disponivel
                    ):
                        wx.MessageBox(
                            f'Coletor {numero} atualizado com sucesso!',
                            'Sucesso',
                            wx.OK | wx.ICON_INFORMATION,
                        )
                        self.carregar_coletores()
                    else:
                        wx.MessageBox(
                            f'Erro ao atualizar o coletor {str(numero).zfill(3)}.',
                            'Erro',
                            wx.OK | wx.ICON_ERROR,
                        )
                dlg.Destroy()
        self.atualizar_estado_botoes()

    def on_excluir_coletor(self, event):
        selected_index = self.list_ctrl.GetFirstSelected()
        if selected_index != -1:
            coletor_numero = self.list_ctrl.GetItemText(selected_index, 0)
            print(f'Tentando excluir coletor {coletor_numero}')
            coletor = self.controller.buscar_coletor(coletor_numero)
            if coletor:
                dlg = wx.MessageDialog(
                    self,
                    f'Deseja mesmo excluir o coletor {coletor_numero}?',
                    'Confirmar Exclusão',
                    wx.YES_NO | wx.ICON_QUESTION,
                )
                if dlg.ShowModal() == wx.ID_YES:
                    if self.controller.excluir_coletor(coletor_numero):
                        wx.MessageBox(
                            f'Coletor {coletor_numero} excluído com sucesso!',
                            'Sucesso',
                            wx.OK | wx.ICON_INFORMATION,
                        )
                        self.carregar_coletores()
                    else:
                        wx.MessageBox(
                            f'Erro ao excluir o coletor {coletor_numero}',
                            'Erro',
                            wx.OK | wx.ICON_ERROR,
                        )
            dlg.Destroy()
        self.atualizar_estado_botoes()

    def upload_csv(self):
        print('Longpress')


class AdiconarColetorDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title='Adicionar Coletor', size=(400, 300))

        # --- Elementos da Interface ---
        self.txt_numero = wx.TextCtrl(self)
        self.txt_modelo = wx.TextCtrl(self)
        self.cb_disponivel = wx.CheckBox(self, label='Disponível')
        self.cb_disponivel.SetValue(True)  # Define como marcado por padrão.

        self.btn_salvar = wx.Button(self, wx.ID_OK, 'Salvar')
        self.btn_cancelar = wx.Button(self, wx.ID_CANCEL, 'Cancelar')

        # --- Layout ---
        sizer_principal = wx.BoxSizer(wx.VERTICAL)
        sizer_campos = wx.FlexGridSizer(rows=4, cols=2, vgap=5, hgap=5)

        sizer_checkboxes = wx.BoxSizer(wx.VERTICAL)
        sizer_botoes = wx.BoxSizer(wx.HORIZONTAL)

        sizer_campos.AddMany([
            (
                wx.StaticText(self, label='Número:'),
                0,
                wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
            ),
            (self.txt_numero, 0, wx.EXPAND),
            (
                wx.StaticText(self, label='Modelo:'),
                0,
                wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
            ),
            (self.txt_modelo, 0, wx.EXPAND),
            (
                wx.StaticText(self, label='Disponível:'),
                0,
                wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
            ),
            (self.cb_disponivel, 0, wx.EXPAND),
            (
                wx.StaticText(self, label=''),
                0,
            ),  # Espaço vazio
            (sizer_checkboxes, 0, wx.EXPAND),
        ])

        # sizer_checkboxes.Add(self.cb_disponivel, 0, wx.ALL, 5)

        sizer_botoes.Add(self.btn_salvar, 0, wx.ALL, 5)
        sizer_botoes.Add(self.btn_cancelar, 0, wx.ALL, 5)

        sizer_principal.Add(sizer_campos, 0, wx.EXPAND | wx.ALL, 10)
        sizer_principal.Add(sizer_botoes, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        self.SetSizer(sizer_principal)
        self.Fit()


class EditarColetorDialog(wx.Dialog):
    """Dialog para editar um Coletor"""

    def __init__(self, parent, coletor):
        super().__init__(parent, title='Editar Coletor', size=(400, 300))
        self.coletor = coletor

        # --- Elementos da Interface ---
        self.txt_numero = wx.TextCtrl(
            self,
            value=str(self.coletor.id),
            style=wx.TE_READONLY,
        )  # Não permitir editar o ID
        self.txt_modelo = wx.TextCtrl(self, value=self.coletor.modelo)
        self.cb_disponivel = wx.CheckBox(self, label='Disponível')
        self.cb_disponivel.SetValue(self.coletor.disponibilidade)

        self.btn_salvar = wx.Button(self, wx.ID_OK, 'Salvar')
        self.btn_cancelar = wx.Button(self, wx.ID_CANCEL, 'Cancelar')

        # --- Layout ---
        sizer_principal = wx.BoxSizer(wx.VERTICAL)
        sizer_campos = wx.FlexGridSizer(rows=4, cols=2, vgap=5, hgap=5)

        sizer_checkboxes = wx.BoxSizer(wx.VERTICAL)
        sizer_botoes = wx.BoxSizer(wx.HORIZONTAL)

        sizer_campos.AddMany([
            (
                wx.StaticText(self, label='Número:'),
                0,
                wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
            ),
            (self.txt_numero, 0, wx.EXPAND),
            (
                wx.StaticText(self, label='Modelo:'),
                0,
                wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
            ),
            (self.txt_modelo, 0, wx.EXPAND),
            (
                wx.StaticText(self, label='Disponível:'),
                0,
                wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
            ),
            (self.cb_disponivel, 0, wx.EXPAND),
            (
                wx.StaticText(self, label=''),
                0,
            ),  # Espaço vazio
            (sizer_checkboxes, 0, wx.EXPAND),
        ])

        sizer_botoes.Add(self.btn_salvar, 0, wx.ALL, 5)
        sizer_botoes.Add(self.btn_cancelar, 0, wx.ALL, 5)

        sizer_principal.Add(sizer_campos, 0, wx.EXPAND | wx.ALL, 10)
        sizer_principal.Add(sizer_botoes, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        self.SetSizer(sizer_principal)
        self.Fit()
