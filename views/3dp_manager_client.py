# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from forward_declare import PrinterCard
import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class Home
###########################################################################

class Home ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"3D打印机机器管理系统"), pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetFont( wx.Font( 11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False, "阿里妈妈方圆体 VF Medium" ) )

        self.m_menubar1 = wx.MenuBar( 0 )
        self.sys_menu = wx.Menu()
        self.m_menuItem1 = wx.MenuItem( self.sys_menu, wx.ID_ANY, _(u"系统设置"), wx.EmptyString, wx.ITEM_NORMAL )
        self.sys_menu.Append( self.m_menuItem1 )

        self.m_menubar1.Append( self.sys_menu, _(u"设置") )

        self.m_menu2 = wx.Menu()
        self.m_menuItem2 = wx.MenuItem( self.m_menu2, wx.ID_ANY, _(u"开/关灯"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu2.Append( self.m_menuItem2 )

        self.m_menubar1.Append( self.m_menu2, _(u"操作") )

        self.SetMenuBar( self.m_menubar1 )

        self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
        home_base_layout = wx.GridSizer( 3, 3, 0, 0 )

        self.printer_card = PrinterCard( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 300,-1 ), wx.BORDER_SIMPLE|wx.TAB_TRAVERSAL )
        self.printer_card.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
        self.printer_card.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
        self.printer_card.SetMinSize( wx.Size( 300,-1 ) )
        self.printer_card.SetMaxSize( wx.Size( 300,-1 ) )

        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        gSizer3 = wx.GridSizer( 1, 2, 0, 0 )

        self.name_label = wx.StaticText( self.printer_card, wx.ID_ANY, _(u"P1S_AMS"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.name_label.Wrap( -1 )

        self.name_label.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "阿里妈妈方圆体 VF" ) )

        gSizer3.Add( self.name_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.state_label = wx.StaticText( self.printer_card, wx.ID_ANY, _(u"状态：--"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.state_label.Wrap( -1 )

        self.state_label.SetFont( wx.Font( 11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False, "阿里妈妈方圆体 VF Medium" ) )

        gSizer3.Add( self.state_label, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer3.Add( gSizer3, 1, wx.EXPAND, 5 )

        gSizer4 = wx.GridSizer( 1, 2, 0, 0 )

        self.layer_label = wx.StaticText( self.printer_card, wx.ID_ANY, _(u"层: 0/0"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.layer_label.Wrap( -1 )

        self.layer_label.SetFont( wx.Font( 11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False, "阿里妈妈方圆体 VF Medium" ) )

        gSizer4.Add( self.layer_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.time_label = wx.StaticText( self.printer_card, wx.ID_ANY, _(u"--h--m"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.time_label.Wrap( -1 )

        self.time_label.SetFont( wx.Font( 11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False, "阿里妈妈方圆体 VF Medium" ) )

        gSizer4.Add( self.time_label, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer3.Add( gSizer4, 1, wx.EXPAND, 5 )

        self.endtime_label = wx.StaticText( self.printer_card, wx.ID_ANY, _(u"-- --"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.endtime_label.Wrap( -1 )

        self.endtime_label.SetFont( wx.Font( 11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False, "阿里妈妈方圆体 VF Medium" ) )

        bSizer3.Add( self.endtime_label, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

        self.print_file_name = wx.StaticText( self.printer_card, wx.ID_ANY, _(u"p1s_test_SUNLU_PETG.3mf"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.print_file_name.Wrap( -1 )

        bSizer3.Add( self.print_file_name, 0, wx.ALL, 5 )

        self.progress_bar = wx.Gauge( self.printer_card, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 400,8 ), wx.GA_HORIZONTAL )
        self.progress_bar.SetValue( 0 )
        self.progress_bar.SetMaxSize( wx.Size( 400,8 ) )

        bSizer3.Add( self.progress_bar, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        self.printer_card.SetSizer( bSizer3 )
        self.printer_card.Layout()
        home_base_layout.Add( self.printer_card, 1, wx.EXPAND|wx.ALL, 5 )


        self.SetSizer( home_base_layout )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_MENU, self.to_light, id = self.m_menuItem2.GetId() )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def to_light( self, event ):
        event.Skip()


