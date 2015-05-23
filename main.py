#!/usr/bin/env python
from gi.repository import Gtk, Gdk
import json, os, pprint
import subprocess
from threading import Thread
from Queue import Queue, Empty

class EventHandler():
	global toInstallArray
	global labelStatus
	def appendToArrayIfChecked(self, args, btncheck, aptget):
		if btncheck.get_active():
			self.toInstallArray.append(aptget)
			self.labelStatus.set_text('Adding '+aptget.title())
		else:
			self.toInstallArray.remove(aptget)
			self.labelStatus.set_text('Remove '+aptget.title())
	def __init__(self, builder):
		self.labelStatus = builder.get_object('label_status')
		self.listbox = Gtk.ListBox()
		self.listbox.set_selection_mode(False)
		self.toInstallArray = []
		#load applist into applistJson
		with open('applist.json') as jfile:
			self.applistJson = json.load(jfile)
		for item in self.applistJson:
			btn =  Gtk.CheckButton(label=item['appname'])
			btn.set_active(True)
			btn.connect('toggled', self.appendToArrayIfChecked, btn, item['aptget'])
			lbr = Gtk.ListBoxRow()
			lbr.add(btn)
			self.listbox.add(lbr)
			self.toInstallArray.append(item['aptget'])
		self.sw = builder.get_object('sw')
		self.sw.add(self.listbox)
		self.sw.show_all()
	def onBtnInstallClicked(self, *args):
		if len(self.toInstallArray) > 0:
			self.labelStatus.set_text('Prepare install of apps..!')
			for aptget in self.toInstallArray:
				p = subprocess.Popen(['apt-get', '-y', 'install', aptget])
				p.wait()
				if p.returncode == 0:
					self.labelStatus.set_text('Install of '+aptget+' is done!')
				else:
					self.labelStatus.set_text('Error while install apps..!')
				#for line in proc.stdout:
				#	print line
				#print proc.returncode
			self.labelStatus.set_text('Install is done..!')
		else:
			self.labelStatus.set_text('You need to choose at lest one app..!')
class OpenAppInstaller:
	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file(os.getcwd()+'/ui/main.glade')
		self.bgColor = Gdk.RGBA.from_color(Gdk.color_parse('#4b4943'))

		self.window = builder.get_object('window_main')
		self.logo = builder.get_object('image_logo')
		self.logo.set_from_file(os.getcwd()+'/images/svg/ubuntu.svg')
		self.btnInstall = builder.get_object('btn_install')		
		self.labelStatus = builder.get_object('label_status')
		self.labelStatus.set_text('OpenAppInstaller')

		eh = EventHandler(builder)
		self.btnInstall.connect('clicked', eh.onBtnInstallClicked,self)

		self.window.set_title('OpenApp-Installer')
		self.window.set_icon_from_file(os.getcwd()+'/images/svg/ubuntu.svg')
		self.window.override_background_color(0, self.bgColor)
		self.window.connect('delete-event', Gtk.main_quit)
		self.window.show_all()
css = """ 
#OpenAppInstaller {
	background-color: #F00;
}
	#OpenAppInstaller GtkButton {
		color: #fff;
		padding: 10px;
	}
		#OpenAppInstaller GtkButton:hover {
			background-color: #40aa54;
			color: #fff;
		}
	#btnInstall {
		background-color: #40aa54;
		color: #000;
	}
	#OpenAppInstaller GtkLabel {
		color: #fff;
	}
"""
styleProvider = Gtk.CssProvider()
styleProvider.load_from_data(css)

Gtk.StyleContext.add_provider_for_screen(
	Gdk.Screen.get_default(),
	styleProvider,
	Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
mainWindow = OpenAppInstaller()
Gtk.main()
