import re
import appModuleHandler
import api
import controlTypes
from scriptHandler import script
import ui

class AppModule(appModuleHandler.AppModule):
	switch= False
	notes = {'C': 'Do',
		'D': 'Re',
		'E': 'Mi',
		'F': 'Fa',
		'G': 'Sol',
		'A': 'La',
		'B': 'Si'
	}

	def event_NVDAObject_init(self, obj):
		if not self.switch or not hasattr(obj, 'UIAAutomationId') or obj.UIAAutomationId != 'AccessibleObject': return
		str = re.sub(r'Nota ', '', obj.name)
		str = re.sub(r'\([^\)]+\)', '', str)
		str = re.sub(r'Compás[\d\s]+Tiempo[\d\s\.]+', '', str)
		for k in self.notes.keys():
			str = re.sub(f'^{k}(?=\\s)', self.notes[k], str)
		obj.name = str

	@script(gesture="kb:control+space")
	def script_switch(self, gesture):
		if self.switch:
			self.switch = False
			ui.message("Desactivado")
		elif not self.switch:
			self.switch = True
			ui.message("Activado")

	@script(gesture='kb:control+shift+c')
	def script_compasAnnounce(self, gesture):
		obj = api.getFocusObject()
		if obj.role == 7 and hasattr(obj, 'UIAAutomationId') and obj.UIAAutomationId == 'AccessibleObject':
			anc = api.getFocusAncestors()
			cmp = next((o for o in anc if re.search(r'[Cc]omp[áa]s\s\d+,', o.name)), None)
			if cmp:
				cmp = re.sub(r',.+', '', cmp.name)
				ui.message(cmp)

	@script(gestures=['kb:upArrow', 'kb:downArrow'])
	def script_block(self, gesture):
		obj = api.getFocusObject()
		if obj.role != 7 or not hasattr(obj, 'UIAAutomationId') or obj.UIAAutomationId != 'AccessibleObject':
			gesture.send()
