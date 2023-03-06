import gtk

window = gtk.Window()

screen = window.get_screen()
ScreenWidth = gtk.gdk.screen_width()
ScreenHeight = gtk.gdk.screen_height()
print (str(ScreenWidth) + 'x' + str(ScreenHeight))