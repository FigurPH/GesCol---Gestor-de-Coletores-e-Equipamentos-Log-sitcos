# src/views/tab_colaboradores.py
import wx
from src.controllers import colaborador_controller
from models import Colaborador

class TabColaboradores(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.colaboradores = []  # Para armazenar os colaboradores exibidos (mantendo uma referência)
        self.controller = colaborador_controller  # Referência ao controller

        # --- Elementos da Interface ---
        self.list_ctrl = wx.ListCtrl(
            self,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SINGLE_SEL
        )
        self.list_ctrl.InsertColumn(0, "Matrícula", width=100)
        self.list_ctrl.InsertColumn(1, "Nome", width=200)
        self.list_ctrl.InsertColumn(2, "Cargo", width=150)
        self.list_ctrl.InsertColumn(3, "Transp.", width=60)
        self.list_ctrl.InsertColumn(4, "Empilh.", width=60)

        self.btn_adicionar = wx.Button(self, label="Adicionar")
        self.btn_editar = wx.Button(self, label="Editar")
        self.btn_excluir = wx.Button(self, label="Excluir")
        self.btn_atualizar = wx.Button(self, label="Atualizar Lista")

        # --- Layout ---
        sizer_principal = wx.BoxSizer(wx.VERTICAL)
        sizer_botoes = wx.BoxSizer(wx.HORIZONTAL)

        sizer_botoes.Add(self.btn_adicionar, 0, wx.ALL, 5)
        sizer_botoes.Add(self.btn_editar, 0, wx.ALL, 5)
        sizer_botoes.Add(self.btn_excluir, 0, wx.ALL, 5)
        sizer_botoes.Add(self.btn_atualizar, 0, wx.ALL, 5)

        sizer_principal.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 10)
        sizer_principal.Add(sizer_botoes, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(sizer_principal)

        # --- Eventos ---
        self.btn_adicionar.Bind(wx.EVT_BUTTON, self.on_adicionar_colaborador)
        self.btn_editar.Bind(wx.EVT_BUTTON, self.on_editar_colaborador)
        self.btn_excluir.Bind(wx.EVT_BUTTON, self.on_excluir_colaborador)
        self.btn_atualizar.Bind(wx.EVT_BUTTON, self.on_atualizar_lista)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_editar_colaborador) # Duplo clique

        # --- Inicialização ---
        self.carregar_colaboradores()
        self.atualizar_estado_botoes() # Inicializa o estado dos botões

    def carregar_colaboradores(self):
        """Carrega os colaboradores do banco de dados e exibe na lista."""
        self.list_ctrl.DeleteAllItems()
        self.colaboradores_data = {}
        self.colaboradores_lista = self.controller.listar_colaboradores_para_exibicao()
        for index, colaborador in enumerate(self.colaboradores_lista):
            list_index = self.list_ctrl.InsertItem(index, str(colaborador['matricula']))
            self.list_ctrl.SetItem(list_index, 1, colaborador['nome'])
            self.list_ctrl.SetItem(list_index, 2, colaborador['cargo'])
            self.list_ctrl.SetItem(list_index, 3, 'Sim' if colaborador['autorizado_transpaleteira'] else 'Não')
            self.list_ctrl.SetItem(list_index, 4, 'Sim' if colaborador['autorizado_empilhadeira'] else 'Não')
            self.colaboradores_data[colaborador['matricula']] = list_index # Mapeia matrícula para o índice da lista


    def on_editar_colaborador(self, event):
        """Evento chamado ao clicar no botão 'Editar' ou dar duplo clique na lista."""
        selected_index = self.list_ctrl.GetFirstSelected()
        if selected_index != -1:
            matricula = list(self.colaboradores_data.keys())[list(self.colaboradores_data.values()).index(selected_index)]
            colaborador = self.controller.buscar_colaborador(matricula)
            if colaborador:
                dlg = EditarColaboradorDialog(self, colaborador)
                if dlg.ShowModal() == wx.ID_OK:
                    nome = dlg.txt_nome.GetValue()
                    cargo = dlg.txt_cargo.GetValue()
                    autorizado_transp = dlg.cb_transpaleteira.GetValue()
                    autorizado_emp = dlg.cb_empilhadeira.GetValue()

                    if self.controller.editar_colaborador(matricula, nome, cargo, autorizado_transp, autorizado_emp):
                        wx.MessageBox(f"Colaborador {nome} (Matrícula: {matricula}) atualizado com sucesso!", "Sucesso", wx.OK | wx.ICON_INFORMATION)
                        self.carregar_colaboradores()
                    else:
                        wx.MessageBox(f"Erro ao atualizar o colaborador {nome} (Matrícula: {matricula}).", "Erro", wx.OK | wx.ICON_ERROR)
                dlg.Destroy()
        self.atualizar_estado_botoes()


    def on_atualizar_lista(self, event):
        """Evento chamado ao clicar no botão 'Atualizar Lista'."""
        self.carregar_colaboradores()
        self.atualizar_estado_botoes()

    def on_adicionar_colaborador(self, event):
        """Evento chamado ao clicar no botão 'Adicionar'."""
        dlg = AdicionarColaboradorDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            # ... (código para adicionar colaborador já existente) ...
            self.carregar_colaboradores()
        dlg.Destroy()
        self.atualizar_estado_botoes()

    def on_editar_colaborador(self, event):
        """Evento chamado ao clicar no botão 'Editar' ou dar duplo clique na lista."""
        selected_index = self.list_ctrl.GetFirstSelected()
        if selected_index != -1:
            matricula = self.list_ctrl.GetItemData(selected_index)
            colaborador = self.controller.buscar_colaborador(matricula)
            if colaborador:
                dlg = EditarColaboradorDialog(self, colaborador)
                if dlg.ShowModal() == wx.ID_OK:
                    nome = dlg.txt_nome.GetValue()
                    cargo = dlg.txt_cargo.GetValue()
                    autorizado_transp = dlg.cb_transpaleteira.GetValue()
                    autorizado_emp = dlg.cb_empilhadeira.GetValue()

                    if self.controller.editar_colaborador(matricula, nome, cargo, autorizado_transp, autorizado_emp):
                        wx.MessageBox(f"Colaborador {nome} (Matrícula: {matricula}) atualizado com sucesso!", "Sucesso", wx.OK | wx.ICON_INFORMATION)
                        self.carregar_colaboradores()
                    else:
                        wx.MessageBox(f"Erro ao atualizar o colaborador {nome} (Matrícula: {matricula}).", "Erro", wx.OK | wx.ICON_ERROR)
                dlg.Destroy()
        self.atualizar_estado_botoes()

    def on_excluir_colaborador(self, event):
        """Evento chamado ao clicar no botão 'Excluir'."""
        selected_index = self.list_ctrl.GetFirstSelected()
        if selected_index != -1:
            matricula = self.list_ctrl.GetItemData(selected_index)
            colaborador = self.controller.buscar_colaborador(matricula)
            if colaborador:
                dlg = wx.MessageDialog(self, f"Deseja realmente excluir o colaborador {colaborador.nome} (Matrícula: {matricula})?",
                                       "Confirmar Exclusão", wx.YES_NO | wx.ICON_QUESTION)
                if dlg.ShowModal() == wx.ID_YES:
                    if self.controller.excluir_colaborador(matricula):
                        wx.MessageBox(f"Colaborador {colaborador.nome} (Matrícula: {matricula}) excluído com sucesso!", "Sucesso", wx.OK | wx.ICON_INFORMATION)
                        self.carregar_colaboradores()
                    else:
                        wx.MessageBox(f"Erro ao excluir o colaborador {colaborador.nome} (Matrícula: {matricula}).", "Erro", wx.OK | wx.ICON_ERROR)
                dlg.Destroy()
        self.atualizar_estado_botoes()

    def atualizar_estado_botoes(self):
        """Atualiza o estado dos botões 'Editar' e 'Excluir' com base na seleção da lista."""
        tem_selecao = self.list_ctrl.GetFirstSelected() != -1
        self.btn_editar.Enable(tem_selecao)
        self.btn_excluir.Enable(tem_selecao)

class EditarColaboradorDialog(wx.Dialog):
    """Dialog para editar um colaborador existente."""
    def __init__(self, parent, colaborador):
        super().__init__(parent, title="Editar Colaborador", size=(400, 300))
        self.colaborador = colaborador

        # --- Elementos da Interface ---
        wx.StaticText(self, label="Matrícula:")
        self.txt_matricula = wx.TextCtrl(self, value=self.colaborador.matricula, style=wx.TE_READONLY) # Não permitir editar a matrícula
        wx.StaticText(self, label="Nome:")
        self.txt_nome = wx.TextCtrl(self, value=self.colaborador.nome)
        wx.StaticText(self, label="Cargo:")
        self.txt_cargo = wx.TextCtrl(self, value=self.colaborador.cargo)
        self.cb_transpaleteira = wx.CheckBox(self, label="Autorizado Transpaleteira", value=self.colaborador.autorizado_transpaleteira)
        self.cb_empilhadeira = wx.CheckBox(self, label="Autorizado Empilhadeira", value=self.colaborador.autorizado_empilhadeira)

        self.btn_salvar = wx.Button(self, wx.ID_OK, "Salvar")
        self.btn_cancelar = wx.Button(self, wx.ID_CANCEL, "Cancelar")

        # --- Layout ---
        sizer_principal = wx.BoxSizer(wx.VERTICAL)
        sizer_campos = wx.FlexGridSizer(rows=4, cols=2, vgap=5, hgap=5)
        sizer_checkboxes = wx.BoxSizer(wx.VERTICAL)
        sizer_botoes = wx.BoxSizer(wx.HORIZONTAL)

        sizer_campos.AddMany([
            (wx.StaticText(self, label="Matrícula:"), 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL),
            (self.txt_matricula, 0, wx.EXPAND),
            (wx.StaticText(self, label="Nome:"), 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL),
            (self.txt_nome, 0, wx.EXPAND),
            (wx.StaticText(self, label="Cargo:"), 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL),
            (self.txt_cargo, 0, wx.EXPAND),
            (wx.StaticText(self, label=""), 0), # Espaço vazio
            (sizer_checkboxes, 0, wx.EXPAND)
        ])

        sizer_checkboxes.Add(self.cb_transpaleteira, 0, wx.ALL, 5)
        sizer_checkboxes.Add(self.cb_empilhadeira, 0, wx.ALL, 5)

        sizer_botoes.Add(self.btn_salvar, 0, wx.ALL, 5)
        sizer_botoes.Add(self.btn_cancelar, 0, wx.ALL, 5)

        sizer_principal.Add(sizer_campos, 0, wx.EXPAND | wx.ALL, 10)
        sizer_principal.Add(sizer_botoes, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        self.SetSizer(sizer_principal)
        self.Fit()

# --- Adicione estas funções ao colaborador_controller.py ---
def editar_colaborador(matricula, nome, cargo, autorizado_transpaleteira, autorizado_empilhadeira):
    """Edita as informações de um colaborador existente."""
    try:
        colaborador = Colaborador.get(Colaborador.matricula == matricula)
        colaborador.nome = nome
        colaborador.cargo = cargo
        colaborador.autorizado_transpaleteira = autorizado_transpaleteira
        colaborador.autorizado_empilhadeira = autorizado_empilhadeira
        colaborador.save()
        return True
    except Colaborador.DoesNotExist:
        print(f"Erro ao editar: Colaborador com matrícula {matricula} não encontrado.")
        return False
    except Exception as e:
        print(f"Erro ao editar colaborador: {e}")
        return False

def excluir_colaborador(matricula):
    """Exclui um colaborador pela sua matrícula."""
    try:
        colaborador = Colaborador.get(Colaborador.matricula == matricula)
        colaborador.delete_instance()
        return True
    except Colaborador.DoesNotExist:
        print(f"Erro ao excluir: Colaborador com matrícula {matricula} não encontrado.")
        return False
    except Exception as e:
        print(f"Erro ao excluir colaborador: {e}")
        return False