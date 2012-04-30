import sys, os, subprocess, time, shutil
from gi.repository import Gtk

class LTWork():
    '''
    The class that does the work.
    If you're writing scripts, you probably just want to subclass this one
    '''
    def __init__(self):
        '''
        self.lenses is a dictionary of lists of structure:
        {lensName : BOOL_IS_ENABLED, lensName : BOOL_IS_ENABLED}
        '''
        self.unitylensroot = '/usr/share/unity/lenses/'
        try:
            os.mkdir('/usr/share/unity/lenses.ignore')
        except:
            pass
        
    def getlenses(self):
        return self.getList()
    
    def getList(self):
        '''
        Get the list...takes no arguments
        '''
        lenses = {}
        dirlist = os.listdir(self.unitylensroot)
        for adir in dirlist:
            lenses[adir] =  True
        dirlist = os.listdir(self.unitylensroot + '../lenses.ignore')
        for adir in dirlist:
            lenses[adir] =  False
        return lenses
        
    def applyToggles(self, desired = {}):
        '''
        Apply pending toggles
        '''
        for lens, state in desired.iteritems():
            if state:
                try:
                    shutil.move(self.unitylensroot + '../lenses.ignore/' + lens, self.unitylensroot + '/' + lens)
                except:
                    pass
            else:
                try:
                    shutil.move(self.unitylensroot + '/' + lens, self.unitylensroot + '../lenses.ignore/' + lens)
                except:
                    pass
                
class TogglerAbout():
    '''
    #TODO
    '''            

class TogglerButtonBox(Gtk.Box):
    '''
    Set up the buttons
    '''
    def __init__(self, rootbox):
        super(TogglerButtonBox, self).__init__(expand=False, homogeneous = True)
        self.root = rootbox
        self.applyb = Gtk.Button("Apply", expand=False)
        self.resetb = Gtk.Button("Reset", expand=False)
        self.refreshb = Gtk.Button("Refresh", expand=False)
        self.disableb = Gtk.Button("Disable All", expand=False)
        self.applyb.connect("clicked", self.apply, None)
        self.resetb.connect("clicked", self.reset, None)
        self.refreshb.connect("clicked", self.refresh, None)
        self.disableb.connect("clicked", self.disable, None)
        self.add(self.refreshb)
        self.add(self.applyb)
        self.add(self.resetb)
        self.add(self.disableb)
        
    def apply(self, widget, arg):
        self.root.getAll()
    def reset(self, widget, arg):
        self.root.resetButton()
    def refresh(self, widget, arg):
        self.root.refreshButton()
    def disable(self, widget, arg):
        self.root.disableButton()
        

class listItem(Gtk.Box):
    '''
    Obvious
    '''
    def __init__(self):
        super(listItem, self).__init__(expand=False)
        self.toggle = Gtk.Switch(active=True, expand=False)
        self.label = Gtk.Label(expand=True)
        self.add(self.toggle)
        self.add(self.label)
    def pair(self, Toggle=False, Name='Test da lenses'):
        '''
        utility function
        '''
        #set toggle state
        self.toggle.set_active(Toggle)
        #set lens name
        self.label.set_label(Name)
    
        

class TogglerListBox(Gtk.VBox):
    '''
    Listbox to hold the toggles
    '''
    def __init__(self):
        super(TogglerListBox, self).__init__(expand=True)

    def dummy(self):
        '''
        I used this for testing...
        '''
        listitemb = listItem()
        listitemb.pair()
        
        self.add(listitemb)
        for i in range(100):
            listitem = listItem()
            listitem.label.set_label("Test Lens " + str(i))
            self.add(listitem)

        
    def add_lens(self, item):
        '''
        add a lens
        '''
        self.add(item)
        
    def clear(self):
        '''
        clear the lenses
        '''
        children = self.get_children()
        for child in children:
            self.remove(child)
            
    def getAll(self):
        '''
        get the states
        '''
        retme = {}
        children = self.get_children()
        for child in children:
            grandchild = child.get_children()
            retme[grandchild[1].get_label()] = grandchild[0].get_active()
        return retme
    

class TogglerContent(Gtk.VBox):
    '''
    The content box and all its nested components
    '''
    def __init__(self, rootbox):
        self.root = rootbox
        super(TogglerContent, self).__init__(homogeneous = False)

        #all the nested boxes
        self.forthescrollbar = Gtk.ScrolledWindow()
        self.forthescrollbar.set_size_request(400,200)

        self.listbox = TogglerListBox()

        viewport = Gtk.Viewport()
        viewport.add(self.listbox)
        self.forthescrollbar.add(viewport)
        self.add(self.forthescrollbar)

        #now the buttonbox
        self.buttonbox = TogglerButtonBox(self.root)
        #add that one
        self.add(self.buttonbox)        

        
class TogglerMenu(Gtk.MenuBar):
    '''
    The Top Menu
    '''
    def __init__(self):
        super(TogglerMenu, self).__init__()
        #File
        file_menu = Gtk.Menu()
        file_menu_name = Gtk.MenuItem("File")
        file_menu_name.set_submenu(file_menu)
       
        file_exit = Gtk.MenuItem("Exit")
        file_exit.connect("activate", Gtk.main_quit)
        file_menu.append(file_exit)

        self.append(file_menu_name)

        #Help
        help_menu = Gtk.Menu()
        help_menu_name = Gtk.MenuItem("Help")
        help_menu_name.set_submenu(help_menu)
        
        help_about = Gtk.MenuItem("About")
        help_about.connect("activate", self.about)
        help_menu.append(help_about)

        self.append(help_menu_name)
    def about(self):
        '''
        TODO
        '''


class TogglerUI(Gtk.Window):
    '''
    The container for all of it
    '''
    def __init__(self):
        super(TogglerUI, self).__init__(title="Lens Toggle Privacy Tool")
        self.LTWork = LTWork()
        self.lenses = self.LTWork.getlenses()
        
        self.connect("destroy", Gtk.main_quit)
        #start with the big box
        self.bigbox = Gtk.VBox(homogeneous=False, spacing = 0)
        
        #adding our menus
        menubar = TogglerMenu()
        self.bigbox.add(menubar)
        
        #content
        self.contentbox = TogglerContent(self)
        
        #finally
        self.bigbox.add(self.contentbox)
        self.add(self.bigbox)
        
        self.set_resizable(False)
        self.lenses = self.LTWork.getlenses()
        self.updatelistbox()
        
        self.show_all()
        
    def refreshButton(self):
        '''
        refresh the lenses
        '''
        self.lenses = self.LTWork.getlenses()
        self.updatelistbox()
        
    def resetButton(self):
        '''
        reset to all enabled
        '''
        self.lenses = self.LTWork.getlenses()
        for lens in self.lenses.keys():
            self.lenses[lens] = True
        self.updatelistbox()

    def disableButton(self):
        '''
        disable all
        '''
        self.lenses = self.LTWork.getlenses()
        for lens in self.lenses.keys():
            self.lenses[lens] = False
        self.updatelistbox()
        
    def updatelistbox(self):
        '''
        update the listbox
        '''
        self.contentbox.listbox.clear()
        for lensname, lensestate in self.lenses.iteritems():
            listitem = listItem()
            listitem.pair(lensestate, lensname) 
            self.contentbox.listbox.add_lens(listitem)
        self.contentbox.listbox.show_all()
    
    def getAll(self):
        '''
        get all the lenses and apply the toggles
        '''
        self.lenses = self.contentbox.listbox.getAll()
        self.LTWork.applyToggles(self.lenses)
        
if __name__=='__main__':
    Toggler = TogglerUI()
    Gtk.main()

