import wx


class TabEquipamentos(wx.Panel):
	"""
	#TODO Tela de equipamentos.
	# Implementar uma tela contendo informações generalizadas
	# para equipamentos
	"""

	def __init__(self, parent):
		super().__init__(parent)
		wx.StaticText(self, label='Conteúdo da aba de Equipamentos')
