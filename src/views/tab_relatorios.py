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
        # Botão de atualização
        refresh_button = wx.Button(self, label="⟳", size=(20, 20))
        refresh_button.Bind(wx.EVT_BUTTON, self.atualizar_tela)

        # Adicionando cada elemento à janela
        for stat in [
            colaboradores_ativos, self.lbl_colaboradores_ativos,
            coletores_atribuidos, self.lbl_coletores_atribuidos,
            transpaleteiras_atribuidas, self.lbl_transpaleteiras_atribuidas,
            empilhadeiras_atribuidas, self.lbl_empilhadeiras_atribuidas

        ]: stats_sizer.Add(stat, 0, wx.ALL, 5)
        # Adiciona um separador visual entre as estatísticas
        stats_sizer.Add(refresh_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        main_sizer.Add(stats_sizer, 0, wx.EXPAND)


        # --- Seção de pesquisa/busca ---
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Filtros
        matricula_label = wx.StaticText(self, label="Matrícula:")
        self.matricula_field = wx.TextCtrl(self)
        search_sizer.Add(matricula_label, 0, wx.ALL|wx.CENTER, 5)
        search_sizer.Add(self.matricula_field, 1, wx.ALL, 5)
        
        coletor_label = wx.StaticText(self, label="Coletor:")
        self.coletor_field = wx.TextCtrl(self)
        search_sizer.Add(coletor_label, 0, wx.ALL|wx.CENTER, 5)
        search_sizer.Add(self.coletor_field, 1, wx.ALL, 5)
        
        '''equipamento_label = wx.StaticText(self, label="Equipamento:")
        self.equipamento_field = wx.TextCtrl(self)
        search_sizer.Add(equipamento_label, 0, wx.ALL|wx.CENTER, 5)
        search_sizer.Add(self.equipamento_field, 1, wx.ALL, 5)''' #TODO Adicionar filtro dos equipamentos com dropdow para selecionar tipo

        
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

        # Desabilita a seleção de itens na lista
        self.list_ctrl.Enable(False)
        

        # --- Inicialização ---
        self.atualizar_tela()
        


        # --- Bindings ---
        self.btn_filtrar.Bind(wx.EVT_BUTTON, self.on_filtrar)
        self.SetSizer(main_sizer)
        
    def atualizar_tela(self, event=None):
        self.atualizar_estatisticas()
        self.atualizar_relatorio()
        self.coletor_field.SetValue('')
        self.matricula_field.SetValue('')

    def atualizar_estatisticas(self,  event = None):
        """
        Atualiza as estatísticas de colaboradores e equipamentos atribuídos.
        """
        # Obtém os dados atualizados do controlador
        colaboradores_ativos = self.controller.contar_colaboradores_ativos()
        coletores_atribuidos = self.controller.contar_coletores_atribuidos()
        transpaleteiras_atribuidas = self.controller.contar_transpaleteiras_atribuidas()
        empilhadeiras_atribuidas = self.controller.contar_empilhadeiras_atribuidas()

        # Atualiza os rótulos com os novos valores
        self.lbl_colaboradores_ativos.SetLabel(str(colaboradores_ativos))
        self.lbl_coletores_atribuidos.SetLabel(str(coletores_atribuidos))
        self.lbl_transpaleteiras_atribuidas.SetLabel(str(transpaleteiras_atribuidas))
        self.lbl_empilhadeiras_atribuidas.SetLabel(str(empilhadeiras_atribuidas))

    def atualizar_relatorio(self, event=None):
        """
        Atualiza a lista de relatórios com os dados mais recentes.
        """
        # Limpa a lista atual
        self.list_ctrl.DeleteAllItems()

        # Obtém os dados atualizados do controlador
        relatorio = self.controller.buscar_atribuicoes()

        # Ordena as atribuições para que as mais antigas (acima de 24 horas) fiquem no topo
        relatorio.sort(key=lambda atrib: (atrib.data_inicio < wx.DateTime.Now() - wx.TimeSpan(24, 0), atrib.data_inicio))

        # Adiciona as linhas ao relatório, destacando as que estão ativas há mais de 24 horas
        for atrib in relatorio:
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), atrib.colaborador.matricula)
            self.list_ctrl.SetItem(index, 1, atrib.colaborador.nome)
            self.list_ctrl.SetItem(index, 2, str(atrib.coletor.id).zfill(3) if atrib.coletor else 'Sem Atribuição')
            self.list_ctrl.SetItem(index, 3, str(atrib.transpaleteira.id).zfill(3) if atrib.transpaleteira else 'Sem Atribuição')
            self.list_ctrl.SetItem(index, 4, str(atrib.empilhadeira.id).zfill(3) if atrib.empilhadeira else 'Sem Atribuição')
            self.list_ctrl.SetItem(index, 5, atrib.data_inicio.strftime('%Y-%m-%d %H:%M:%S'))

            # Verifica se a atribuição está ativa há mais de 24 horas
            if atrib.data_inicio < wx.DateTime.Now() - wx.TimeSpan(24, 0):
                self.list_ctrl.SetItemBackgroundColour(index, wx.Colour(255, 0, 0))


    def on_filtrar(self, event=None):
        # Obtém os valores dos campos de filtro
        matricula = self.matricula_field.GetValue().strip()
        coletor = self.coletor_field.GetValue().strip()
        # equipamento = self.equipamento_field.GetValue().strip()
        

        # Obtém os dados filtrados do controlador
        relatorio_filtrado = self.controller.filtrar_atribuicoes(
            matricula=matricula,
            coletor=coletor,
        )

        if relatorio_filtrado:
        # Limpa a lista atual
            self.list_ctrl.DeleteAllItems()

        # Preenche a lista com os dados filtrados

            self.list_ctrl.Append([
            relatorio_filtrado.colaborador.matricula,
            relatorio_filtrado.colaborador.nome,
            str(relatorio_filtrado.coletor.id).zfill(3) if relatorio_filtrado.coletor else 'Sem Atribuição',
            str(relatorio_filtrado.transpaleteira.id).zfill(3) if relatorio_filtrado.transpaleteira else 'Sem Atribuição',
            str(relatorio_filtrado.empilhadeira.id).zfill(3) if relatorio_filtrado.empilhadeira else 'Sem Atribuição',
            relatorio_filtrado.data_inicio.strftime('%Y-%m-%d %H:%M:%S')
            ])


