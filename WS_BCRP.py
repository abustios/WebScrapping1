
import wx

##clase de carga de información del bcr a sql server
class ws_bcr():
	def cargabcr():

		import requests
		from bs4 import BeautifulSoup
		import pypyodbc 

		connection = pypyodbc.connect(dsn='SQL') 
		cursor = connection.cursor() 

		r = requests.get('http://www.bcrp.gob.pe/estadisticas/indice-de-tasa-interbancaria-en-moneda-nacional.html')

		fuente=r.text
		sopa=BeautifulSoup(fuente, "lxml")
		tabla = sopa.find_all('td')
		li=[]

		for tb in tabla:
			li.append(tb)

		cursor.execute('TRUNCATE TABLE dm_ods.dbo.tasa_interbancaria')
		connection.commit()

		i=0
		while i<len(li):
			try:
				fecha =str(li[i]).replace('<td>','').replace('</td>','').replace('<span style="line-height: 15.808px;">','').replace('</span>','').replace('<td class="null">','').replace('<span style="line-height: 15.808px; background-color: #3399ff;"><span style="line-height: 15.808px; background-color: #ffffff;">','')
				Promedio_efectiva=str(li[i+1]).replace('<td>','').replace('</td>','').replace(',','.').replace('<span style="line-height: 15.808px;">','').replace('</span>','').replace('<td class="null">','').replace('<span style="line-height: 15.808px; background-color: #3399ff;"><span style="line-height: 15.808px; background-color: #ffffff;">','')
				Indice_diario=str(li[i+2]).replace('<td>','').replace('</td>','').replace(',','.').replace('<span style="line-height: 15.808px;">','').replace('</span>','').replace('<td class="null">','').replace('<span style="line-height: 15.808px; background-color: #3399ff;"><span style="line-height: 15.808px; background-color: #ffffff;">','')
				Indice_acumulado=str(li[i+3]).replace('<td>','').replace('</td>','').replace(',','.').replace('<span style="line-height: 15.808px;">','').replace('</span>','').replace('<td class="null">','').replace('<span style="line-height: 15.808px; background-color: #3399ff;"><span style="line-height: 15.808px; background-color: #ffffff;">','')
				i+=4
#		print(fecha,Promedio_efectiva,Indice_diario,Indice_acumulado)
				cursor.execute("INSERT INTO  dm_ods.dbo.TASA_INTERBANCARIA  VALUES (?,?,?,?)", (fecha,Promedio_efectiva,Indice_diario,Indice_acumulado ) ) 
				connection.commit()


				cursor.execute('SET LANGUAGE SPANISH')
				cursor.execute("update dm_ods.dbo.tasa_interbancaria SET FECHA=replace(replace(replace(replace(FECHA,'+','-'),'.','-'),'--','-'),' ','-')")
				cursor.execute("update dm_ods.dbo.tasa_interbancaria SET FECHA=replace(replace(replace(replace(replace(replace(replace(replace(replace(fecha,'4-Mar-17-','4-Mar-17'),'17-Set16','17-Set-16'),'7Nov-15','7-Nov-15'),'15-May11','15-May-11'),'31Ago-17','31-Ago-17'),'3Ago-17','3-Ago-17'),'12-Abr17','12-Abr-17'),'30-Dic17','30-Dic-17'),'30Set-17','30-Set-17')")
				cursor.execute("update dm_ods.dbo.tasa_interbancaria set fecha=REPLACE(FECHA,'Abril','Abr')")
				cursor.execute("update dm_ods.dbo.tasa_interbancaria set fecha='31-Dic-15' where fecha=' 31-Dic-15'")
				cursor.execute("update dm_ods.dbo.tasa_interbancaria set fecha='30-Dic-15' where fecha=' 30-Dic-15'")
				cursor.execute("update dm_ods.dbo.tasa_interbancaria set fecha=replace(fecha,'set','sep')")
				connection.commit()
			except (RuntimeError, TypeError, NameError):
				pass

		cursor.execute('update dm_ods.dbo.tasa_interbancaria set fecha= convert(varchar(8),cast(fecha as date),112)')
		connection.commit()

class Pantalla(wx.Frame):

	def __init__(self, *args, **kw):
		super(Pantalla, self).__init__(*args, **kw)
		self.InitUI()

	def InitUI(self):

		panel = wx.Panel(self)
		hbox = wx.BoxSizer(wx.HORIZONTAL)

		btnPanel = wx.Panel(panel)
		vbox = wx.BoxSizer(wx.VERTICAL)
		Carga = wx.Button(btnPanel, wx.ID_ANY, 'Cargar Tasa Interbancaria', size=(200, 30))

		self.Bind(wx.EVT_BUTTON, self.Ejecuta, id=Carga.GetId())

		vbox.Add((200, 50))
		vbox.Add(Carga)

		btnPanel.SetSizer(vbox)
		hbox.Add(btnPanel, 0.6, wx.EXPAND | wx.RIGHT, 50)
		hbox.Add(wx.TextCtrl(btnPanel), flag=wx.LEFT, border=5)
		panel.SetSizer(hbox)




		self.SetTitle('Carga Transferencia Interbancaria')
		self.Centre()

	def Ejecuta(self, event):

		ws_bcr.cargabcr()
		wx.CallLater(2000, self.ShowMessage)


	def ShowMessage(self):
		wx.MessageBox('Completado', 'Info',wx.OK | wx.ICON_INFORMATION)

def main():

    app = wx.App()
    ex = Pantalla(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()


