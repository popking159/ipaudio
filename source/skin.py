#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
IPAudio Modern Color Skins
- Orange: #FF6B35 (warm, energetic)
- Teal: #00BFA5 (cool, modern)
- Lime: #CDDC39 (fresh, vibrant)
"""

# Standard button colors
BUTTON_COLORS = {
    'red': '#ff0069',         # Exit/Cancel
    'green': '#00ffa9',       # Save/Reset
    'yellow': '#ffe800',      # 
    'blue': '#0094ff',        # DownloadList
    'grey': '#e0dfdb',        # Menu
    'whitegrey': '#d2bdbd',   # EPG
    'purple': '#d5a6bd',      # INFO
    'orange': '#ffa743',      # HELP
}

# Color definitions
COLORS = {
    'orange': {
        'primary': '#FF6B35',
        'selection': '#FF8C61',
        'text': '#FFFFFF',
        'text_dim': '#CCCCCC',
        'background': '#000000',
        'border': '#FF6B35',
    },
    'teal': {
        'primary': '#00BFA5',
        'selection': '#26D9C3',
        'text': '#FFFFFF',
        'text_dim': '#CCCCCC',
        'background': '#000000',
        'border': '#00BFA5',
    },
    'lime': {
        'primary': '#CDDC39',
        'selection': '#D7E361',
        'text': '#FFFFFF',
        'text_dim': '#CCCCCC',
        'background': '#000000',
        'border': '#CDDC39',
    }
}

def getSkinFHD(color_scheme):
    """Generate FHD skin XML for IPAudioScreen"""
    c = COLORS[color_scheme]
    b = BUTTON_COLORS
    
    return """
    <screen name="IPAudioScreen" position="center,center" size="1390,760" flags="wfNoBorder">
        <!-- Border layer (bottom) -->
        <eLabel name="" position="0,0" size="1390,760" zPosition="-3" backgroundColor="{border}" />
        <!-- Black background layer (top, 1px smaller on each side) -->
        <eLabel name="" position="1,1" size="1388,758" zPosition="-2" backgroundColor="{bg}" />
        
        <!-- Title -->
        <widget name="title" position="1164,30" size="200,60" font="Regular;30" foregroundColor="{primary}" backgroundColor="{bg}" halign="center" valign="center" transparent="0" />
        
        <!-- Header -->
        <widget name="server" position="20,20" size="640,50" font="Regular;32" foregroundColor="#000000" backgroundColor="{primary}" halign="center" valign="center" transparent="0" />
        
        <!-- Info bar -->
        <widget name="sync" position="20,85" size="300,30" font="Regular;20" foregroundColor="{primary}" backgroundColor="{bg}" halign="left" transparent="0" />
        <widget name="audio_delay" position="340,85" size="300,30" font="Regular;20" foregroundColor="{primary}" backgroundColor="{bg}" halign="left" transparent="0" />
        <widget name="network_status" position="660,85" size="200,30" font="Regular;20" foregroundColor="{primary}" backgroundColor="{bg}" halign="left" transparent="0" />
        
        <!-- Countdown Display (centered, large font) -->
        <widget name="countdown" position="678,20" size="200,50" font="Regular;28" foregroundColor="#000000" backgroundColor="{primary}" halign="center" valign="center" transparent="0" zPosition="100" />
        
        <!-- Channel List (840px width, 500px height = 10 items x 50px) -->
        <widget name="list" position="20,140" size="1350,540" backgroundColor="{bg}" foregroundColor="{text}" foregroundColorSelected="#000000" backgroundColorSelected="{primary}" itemHeight="60" scrollbarMode="showOnDemand" scrollbarBorderWidth="1" scrollbarBorderColor="{primary}" scrollbarBackgroundColor="#1a1a1a" scrollbarForegroundColor="{primary}" transparent="0" />
        
        <!-- Footer Buttons (Red, Green, Yellow, Blue) -->
        <widget name="key_red" position="20,695" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{red}" halign="center" valign="center" transparent="0" />
        <widget name="key_green" position="190,695" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{green}" halign="center" valign="center" transparent="0" />
        <widget name="key_yellow" position="360,695" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{yellow}" halign="center" valign="center" transparent="0" />
        <widget name="key_blue" position="530,695" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{blue}" halign="center" valign="center" transparent="0" />
        <widget name="key_menu" position="700,695" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{grey}" halign="center" valign="center" transparent="0" />
        <widget name="key_epg" position="870,695" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{whitegrey}" halign="center" valign="center" transparent="0" />
        <widget name="key_info" position="1040,695" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{purple}" halign="center" valign="center" transparent="0" />
        <widget name="key_help" position="1210,695" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{orange}" halign="center" valign="center" transparent="0" />
    </screen>
    """.format(
        bg=c['background'],
        border=c['border'],
        primary=c['primary'],
        text=c['text'],
        red=b['red'],
        green=b['green'],
        yellow=b['yellow'],
        blue=b['blue'],
        grey=b['grey'],
        whitegrey=b['whitegrey'],
        orange=b['orange'],
        purple=b['purple']
    )

def getSetupSkinFHD(color_scheme):
    """Generate FHD setup screen skin"""
    c = COLORS[color_scheme]
    b = BUTTON_COLORS
    
    return """
    <screen name="IPAudioSetup" position="center,center" size="1080,650" flags="wfNoBorder">
        <!-- Border layer (bottom) -->
        <eLabel name="" position="0,0" size="1080,650" zPosition="-3" backgroundColor="{border}" />
        <!-- Black background layer (top, 1px smaller on each side) -->
        <eLabel name="" position="1,1" size="1078,648" zPosition="-2" backgroundColor="{bg}" />
        
        <!-- Header -->
        <eLabel position="20,20" size="1040,50" text="IPAudio Settings" font="Regular;28" foregroundColor="#000000" backgroundColor="{primary}" halign="center" valign="center" transparent="0" />
        
        <!-- Config List (500px height = 10 items x 50px) -->
        <widget name="config" position="20,90" size="1040,500" backgroundColor="{bg}" foregroundColor="{text}" foregroundColorSelected="#000000" backgroundColorSelected="{primary}" itemHeight="50" scrollbarMode="showOnDemand" scrollbarBorderWidth="1" scrollbarBorderColor="{primary}" scrollbarForegroundColor="{primary}" transparent="0" />
        
        <!-- Footer Buttons -->
        <widget name="key_red" render="Label" position="20,595" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{red}" halign="center" valign="center" transparent="0" />
        <widget name="key_green" render="Label" position="190,595" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{green}" halign="center" valign="center" transparent="0" />
        <widget name="key_yellow" render="Label" position="360,595" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{yellow}" halign="center" valign="center" transparent="0" />
        <widget name="key_blue" render="Label" position="530,595" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{blue}" halign="center" valign="center" transparent="0" />
    </screen>
    """.format(
        bg=c['background'],
        border=c['border'],
        primary=c['primary'],
        text=c['text'],
        red=b['red'],
        green=b['green'],
        yellow=b['yellow'],
        blue=b['blue']
    )

def getPlaylistSkinFHD(color_scheme):
    """Generate FHD playlist management screen skin"""
    c = COLORS[color_scheme]
    button_text = c['text'] if color_scheme != 'lime' else '#000000'
    
    return """
    <screen name="IPAudioPlaylist" position="center,center" size="880,650" flags="wfNoBorder">
        <!-- Border layer (bottom) -->
        <eLabel name="" position="0,0" size="880,650" zPosition="-3" backgroundColor="{border}" />
        <!-- Black background layer (top, 1px smaller on each side) -->
        <eLabel name="" position="1,1" size="878,648" zPosition="-2" backgroundColor="{bg}" />
        
        <!-- Header -->
        <widget name="server" position="20,20" size="840,50" font="Regular;28" foregroundColor="{text}" backgroundColor="{primary}" halign="center" valign="center" transparent="0" />
        
        <!-- Channel List (500px height = 10 items x 50px) -->
        <widget name="list" position="20,90" size="840,500" backgroundColor="{bg}" foregroundColor="{text}" itemHeight="50" scrollbarMode="showOnDemand" scrollbarBorderWidth="1" scrollbarBorderColor="{primary}" scrollbarForegroundColor="{primary}" transparent="0" />
        
        <!-- Footer Buttons -->
        <widget name="key_green" position="250,590" size="180,50" font="Regular;22" foregroundColor="{button_text}" backgroundColor="{primary}" halign="center" valign="center" transparent="0" />
        <widget name="key_red" position="450,590" size="180,50" font="Regular;22" foregroundColor="#ffffff" backgroundColor="#cc0000" halign="center" valign="center" transparent="0" />
    </screen>
    """.format(
        bg=c['background'],
        border=c['border'],
        primary=c['primary'],
        text=c['text'],
        button_text=button_text
    )

def getInfoSkinFHD(color_scheme):
    """Generate FHD info screen skin"""
    c = COLORS[color_scheme]
    b = BUTTON_COLORS
    
    return """
    <screen name="IPAudioInfo" position="center,center" size="700,500" flags="wfNoBorder">
        <!-- Border layer (bottom) -->
        <eLabel name="" position="0,0" size="700,500" zPosition="-3" backgroundColor="{border}" />
        <!-- Black background layer (top, 1px smaller on each side) -->
        <eLabel name="" position="1,1" size="698,498" zPosition="-2" backgroundColor="{bg}" />
        
        <!-- Header -->
        <eLabel position="20,20" size="660,50" text="About IPAudio" font="Regular;32" foregroundColor="#000000" backgroundColor="{primary}" halign="center" valign="center" transparent="0" />
        
        <!-- Info Text -->
        <widget name="info_text" position="20,100" size="660,320" font="Regular;22" foregroundColor="{text}" backgroundColor="{bg}" halign="center" valign="top" transparent="1" />
        
        <!-- Close Button -->
        <widget name="key_red" position="20,440" size="160,50" font="Regular;24" foregroundColor="#000000" backgroundColor="{red}" halign="center" valign="center" transparent="0" />
    </screen>
    """.format(
        bg=c['background'],
        border=c['border'],
        primary=c['primary'],
        text=c['text'],
        red=b['red']
    )

def getHelpSkinFHD(color_scheme):
    """Generate FHD help screen skin with scrollbar"""
    c = COLORS[color_scheme]
    b = BUTTON_COLORS
    
    return """
    <screen name="IPAudioHelp" position="center,center" size="600,800" flags="wfNoBorder">
        <!-- Border layer (bottom) -->
        <eLabel name="" position="0,0" size="600,800" zPosition="-3" backgroundColor="{border}" />
        <!-- Black background layer (top, 1px smaller on each side) -->
        <eLabel name="" position="1,1" size="598,798" zPosition="-2" backgroundColor="{bg}" />
        
        <!-- Header -->
        <eLabel position="10,10" size="580,50" text="IPAudio Help" font="Regular;32" foregroundColor="#000000" backgroundColor="{primary}" halign="center" valign="center" transparent="0" />
        
        <!-- Scrollable Help Text -->
        <widget source="help_text" render="Listbox" position="10,70" size="580,660" backgroundColor="{bg}" foregroundColor="{text}" backgroundColorSelected="{primary}" scrollbarMode="showOnDemand" scrollbarBorderWidth="1" scrollbarBorderColor="{primary}" scrollbarForegroundColor="{primary}" transparent="1">
            <convert type="TemplatedMultiContent">
                {{"template": [
                    MultiContentEntryText(pos=(5, 0), size=(580, 30), font=0, flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER|RT_WRAP, text=0)
                ],
                "fonts": [gFont("Regular", 26)],
                "itemHeight": 30
                }}
            </convert>
        </widget>
        
        <!-- Close Button -->
        <widget name="key_red" position="10,740" size="160,50" font="Regular;24" foregroundColor="#000000" backgroundColor="{red}" halign="center" valign="center" transparent="0" />
    </screen>
    """.format(
        bg=c['background'],
        border=c['border'],
        primary=c['primary'],
        text=c['text'],
        red=b['red']
    )

def getSkinHD(color_scheme):
    """Generate HD skin XML for IPAudioScreen (scaled for 1280x720)"""
    c = COLORS[color_scheme]
    b = BUTTON_COLORS
    
    return """
    <screen name="IPAudioScreen" position="center,center" size="880,560" flags="wfNoBorder">
    <!-- Border layer (bottom) -->
    <eLabel name="" position="0,0" size="880,560" zPosition="-3" backgroundColor="{border}" />
    <!-- Black background layer (top, 1px smaller on each side) -->
    <eLabel name="" position="1,1" size="878,558" zPosition="-2" backgroundColor="{bg}" />

    <!-- Title -->
    <widget name="title" position="700,15" size="160,40"
        font="Regular;18" foregroundColor="{primary}" backgroundColor="{bg}"
        halign="center" valign="center" transparent="0" />

    <!-- Header -->
    <widget name="server" position="15,15" size="500,40"
        font="Regular;26" foregroundColor="#000000" backgroundColor="{primary}"
        halign="center" valign="center" transparent="0" />

    <!-- Info bar -->
    <widget name="sync" position="15,65" size="240,25"
        font="Regular;18" foregroundColor="{primary}" backgroundColor="{bg}"
        halign="left" transparent="0" />
    <widget name="audio_delay" position="265,65" size="240,25"
        font="Regular;18" foregroundColor="{primary}" backgroundColor="{bg}"
        halign="left" transparent="0" />
    <widget name="network_status" position="515,65" size="200,25"
        font="Regular;18" foregroundColor="{primary}" backgroundColor="{bg}"
        halign="left" transparent="0" />

    <!-- Countdown Display -->
    <widget name="countdown" position="510,15" size="170,40"
        font="Regular;22" foregroundColor="#000000" backgroundColor="{primary}"
        halign="center" valign="center" transparent="0" zPosition="100" />

    <!-- Channel List -->
    <widget name="list" position="15,110" size="850,370"
        backgroundColor="{bg}" foregroundColor="{text}"
        foregroundColorSelected="#000000" backgroundColorSelected="{primary}"
        itemHeight="45" scrollbarMode="showOnDemand"
        scrollbarBorderWidth="1" scrollbarBorderColor="{primary}"
        scrollbarBackgroundColor="#1a1a1a" scrollbarForegroundColor="{primary}"
        transparent="0" />

    <!-- Footer Buttons -->
    <widget name="key_red" position="15,495" size="130,40"
        font="Regular;18" foregroundColor="#000000" backgroundColor="{red}"
        halign="center" valign="center" transparent="0" />
    <widget name="key_green" position="155,495" size="130,40"
        font="Regular;18" foregroundColor="#000000" backgroundColor="{green}"
        halign="center" valign="center" transparent="0" />
    <widget name="key_yellow" position="295,495" size="130,40"
        font="Regular;18" foregroundColor="#000000" backgroundColor="{yellow}"
        halign="center" valign="center" transparent="0" />
    <widget name="key_blue" position="435,495" size="130,40"
        font="Regular;18" foregroundColor="#000000" backgroundColor="{blue}"
        halign="center" valign="center" transparent="0" />
    <widget name="key_menu" position="575,495" size="130,40"
        font="Regular;18" foregroundColor="#000000" backgroundColor="{grey}"
        halign="center" valign="center" transparent="0" />
    <widget name="key_epg" position="715,495" size="130,40"
        font="Regular;18" foregroundColor="#000000" backgroundColor="{whitegrey}"
        halign="center" valign="center" transparent="0" />
    </screen>
    """.format(
        bg=c['background'],
        border=c['border'],
        primary=c['primary'],
        text=c['text'],
        red=b['red'],
        green=b['green'],
        yellow=b['yellow'],
        blue=b['blue'],
        grey=b['grey'],
        whitegrey=b['whitegrey']
    )

def getSetupSkinHD(color_scheme):
    """Generate HD setup screen skin"""
    c = COLORS[color_scheme]
    b = BUTTON_COLORS
    
    return """
    <screen name="IPAudioSetup" position="center,center" size="600,442" flags="wfNoBorder">
        <!-- Border layer (bottom) -->
        <eLabel name="" position="0,0" size="600,442" zPosition="-3" backgroundColor="{border}" />
        <!-- Black background layer (top, 1px smaller on each side) -->
        <eLabel name="" position="1,1" size="598,440" zPosition="-2" backgroundColor="{bg}" />
        
        <!-- Header -->
        <eLabel position="14,14" size="571,34" text="IPAudio Settings" font="Regular;19" foregroundColor="{text}" backgroundColor="{primary}" halign="center" valign="center" transparent="0" />
        
        <!-- Config List (340px height = 5.86 items x 58px, round to 6) -->
        <widget name="config" position="14,61" size="571,348" backgroundColor="{bg}" foregroundColor="{text}" itemHeight="58" scrollbarMode="showOnDemand" scrollbarBorderWidth="1" scrollbarBorderColor="{primary}" scrollbarForegroundColor="{primary}" transparent="0" />
        
        <!-- Footer Buttons -->
        <widget source="key_green" render="Label" position="170,404" size="122,34" font="Regular;15" foregroundColor="#000000" backgroundColor="{green}" halign="center" valign="center" transparent="0" />
        <widget source="key_red" render="Label" position="40,404" size="122,34" font="Regular;15" foregroundColor="#000000" backgroundColor="{red}" halign="center" valign="center" transparent="0" />
        <widget source="key_blue" render="Label" position="442,404" size="122,34" font="Regular;15" foregroundColor="#000000" backgroundColor="{blue}" halign="center" valign="center" transparent="0" />
    </screen>
    """.format(
        bg=c['background'],
        border=c['border'],
        primary=c['primary'],
        text=c['text'],
        red=b['red'],
        green=b['green'],
        blue=b['blue']
    )

def getPlaylistSkinHD(color_scheme):
    """Generate HD playlist management screen skin"""
    c = COLORS[color_scheme]
    b = BUTTON_COLORS
    
    return """
    <screen name="IPAudioPlaylist" position="center,center" size="600,442" flags="wfNoBorder">
        <!-- Border layer (bottom) -->
        <eLabel name="" position="0,0" size="600,442" zPosition="-3" backgroundColor="{border}" />
        <!-- Black background layer (top, 1px smaller on each side) -->
        <eLabel name="" position="1,1" size="598,440" zPosition="-2" backgroundColor="{bg}" />
        
        <!-- Header -->
        <widget name="server" position="14,14" size="571,34" font="Regular;19" foregroundColor="{text}" backgroundColor="{primary}" halign="center" valign="center" transparent="0" />
        
        <!-- Channel List (348px height = 6 items x 58px) -->
        <widget name="list" position="14,61" size="571,348" backgroundColor="{bg}" foregroundColor="{text}" itemHeight="58" scrollbarMode="showOnDemand" scrollbarBorderWidth="1" scrollbarBorderColor="{primary}" scrollbarForegroundColor="{primary}" transparent="0" />
        
        <!-- Footer Buttons -->
        <widget name="key_green" position="170,404" size="122,34" font="Regular;15" foregroundColor="#000000" backgroundColor="{green}" halign="center" valign="center" transparent="0" />
        <widget name="key_red" position="306,404" size="122,34" font="Regular;15" foregroundColor="#ffffff" backgroundColor="{red}" halign="center" valign="center" transparent="0" />
    </screen>
    """.format(
        bg=c['background'],
        border=c['border'],
        primary=c['primary'],
        text=c['text'],
        green=b['green'],
        red=b['red']
    )

def getInfoSkinHD(color_scheme):
    """Generate HD info screen skin"""
    c = COLORS[color_scheme]
    b = BUTTON_COLORS
    
    return """
    <screen name="IPAudioInfo" position="center,center" size="476,340" flags="wfNoBorder">
        <!-- Border layer (bottom) -->
        <eLabel name="" position="0,0" size="476,340" zPosition="-3" backgroundColor="{border}" />
        <!-- Black background layer (top, 1px smaller on each side) -->
        <eLabel name="" position="1,1" size="474,338" zPosition="-2" backgroundColor="{bg}" />
        
        <!-- Header -->
        <eLabel position="14,14" size="449,34" text="About IPAudio" font="Regular;22" foregroundColor="{text}" backgroundColor="{primary}" halign="center" valign="center" transparent="0" />
        
        <!-- Info Text -->
        <widget name="info_text" position="27,68" size="422,217" font="Regular;15" foregroundColor="{text}" backgroundColor="{bg}" halign="center" valign="top" transparent="1" />
        
        <!-- Close Button -->
        <widget name="key_red" position="170,299" size="136,34" font="Regular;16" foregroundColor="#ffffff" backgroundColor="{red}" halign="center" valign="center" transparent="0" />
    </screen>
    """.format(
        bg=c['background'],
        border=c['border'],
        primary=c['primary'],
        text=c['text'],
        red=b['red']
    )

def getHelpSkinHD(color_scheme):
    """Generate HD help screen skin with scrollbar"""
    c = COLORS[color_scheme]
    b = BUTTON_COLORS
    
    return """
    <screen name="IPAudioHelp" position="center,center" size="680,442" flags="wfNoBorder">
        <!-- Border layer (bottom) -->
        <eLabel name="" position="0,0" size="680,442" zPosition="-3" backgroundColor="{border}" />
        <!-- Black background layer (top, 1px smaller on each side) -->
        <eLabel name="" position="1,1" size="678,440" zPosition="-2" backgroundColor="{bg}" />
        
        <!-- Header -->
        <eLabel position="14,14" size="653,34" text="IPAudio Help" font="Regular;22" foregroundColor="{text}" backgroundColor="{primary}" halign="center" valign="center" transparent="0" />
        
        <!-- Scrollable Help Text -->
        <widget source="help_text" render="Listbox" position="27,61" size="626,333" backgroundColor="{bg}" foregroundColor="{text}" scrollbarMode="showOnDemand" scrollbarBorderWidth="1" scrollbarBorderColor="{primary}" scrollbarForegroundColor="{primary}" transparent="1">
            <convert type="TemplatedMultiContent">
                {{"template": [
                    MultiContentEntryText(pos=(3, 0), size=(394, 20), font=0, flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER|RT_WRAP, text=0)
                ],
                "fonts": [gFont("Regular", 18)],
                "itemHeight": 20
                }}
            </convert>
        </widget>
        
        <!-- Close Button -->
        <widget name="key_red" position="272,401" size="136,34" font="Regular;16" foregroundColor="#ffffff" backgroundColor="{red}" halign="center" valign="center" transparent="0" />
    </screen>
    """.format(
        bg=c['background'],
        border=c['border'],
        primary=c['primary'],
        text=c['text'],
        red=b['red']
    )

def getGridSkinFHD(color_scheme):
    """Generate FHD skin with Grid view"""
    c = COLORS[color_scheme]
    b = BUTTON_COLORS
    
    return """
    <screen name="IPAudioScreenGrid" position="80,24" size="1730,1020" title="IPAudio Grid" backgroundColor="#20383636" flags="wfNoBorder">
    <!-- Header -->
    <widget name="title" position="1385,70" size="270,50" font="Regular;40" foregroundColor="#FFA500" transparent="1" halign="left" />
    <widget name="server" position="110,65" size="600,50" font="Regular;32" foregroundColor="#FFFFFF" transparent="1" halign="left" />
    <widget name="sync" position="830,120" size="250,40" font="Regular;28" foregroundColor="#00FF00" transparent="1" halign="left" />
    <widget name="audio_delay" position="1100,120" size="250,40" font="Regular;24" foregroundColor="#00FFFF" transparent="1" halign="left" />
    <widget name="network_status" position="95,120" size="400,40" font="Regular;24" foregroundColor="#FFFF00" transparent="1" />
    <widget name="countdown" position="510,120" size="300,40" font="Regular;24" foregroundColor="#FF6600" transparent="1" />

    <!-- Selection frame -->
    <widget name="frame" position="95,175" size="290,260" zPosition="1" alphatest="blend" transparent="1" />

    <!-- Row 1 -->
    <widget name="label_1" position="105,190" size="270,30" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_1" position="140,225" size="200,120" alphatest="blend" />
    <widget name="event_1" position="110,350" size="260,54" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_2" position="425,190" size="270,30" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_2" position="460,225" size="200,120" alphatest="blend" />
    <widget name="event_2" position="430,350" size="260,54" font="Regular;24" halign="center" valign="center" foregroundColor="{primary}" transparent="1" />

    <widget name="label_3" position="745,190" size="270,30" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_3" position="780,225" size="200,120" alphatest="blend" />
    <widget name="event_3" position="750,350" size="260,54" font="Regular;24" halign="center" valign="center" foregroundColor="{primary}" transparent="1" />

    <widget name="label_4" position="1065,190" size="270,30" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_4" position="1100,225" size="200,120" alphatest="blend" />
    <widget name="event_4" position="1070,350" size="260,54" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_5" position="1385,190" size="270,30" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_5" position="1420,225" size="200,120" alphatest="blend" />
    <widget name="event_5" position="1390,350" size="260,54" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <!-- Row 2 -->
    <widget name="label_6" position="105,450" size="270,30" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_6" position="140,485" size="200,120" alphatest="blend" />
    <widget name="event_6" position="110,610" size="260,54" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_7" position="425,450" size="270,30" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_7" position="460,485" size="200,120" alphatest="blend" />
    <widget name="event_7" position="430,610" size="260,54" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_8" position="745,450" size="270,30" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_8" position="780,485" size="200,120" alphatest="blend" />
    <widget name="event_8" position="750,610" size="260,54" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_9" position="1065,450" size="270,30" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_9" position="1100,485" size="200,120" alphatest="blend" />
    <widget name="event_9" position="1070,610" size="260,54" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_10" position="1385,450" size="270,30" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_10" position="1420,485" size="200,120" alphatest="blend" />
    <widget name="event_10" position="1390,610" size="260,54" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <!-- Row 3 -->
    <widget name="label_11" position="105,710" size="270,30" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_11" position="140,745" size="200,120" alphatest="blend" />
    <widget name="event_11" position="110,870" size="260,54" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_12" position="425,710" size="270,30" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_12" position="460,745" size="200,120" alphatest="blend" />
    <widget name="event_12" position="430,870" size="260,54" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_13" position="745,710" size="270,30" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_13" position="780,745" size="200,120" alphatest="blend" />
    <widget name="event_13" position="750,870" size="260,54" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_14" position="1065,710" size="270,30" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_14" position="1100,745" size="200,120" alphatest="blend" />
    <widget name="event_14" position="1070,870" size="260,54" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_15" position="1385,710" size="270,30" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_15" position="1420,745" size="200,120" alphatest="blend" />
    <widget name="event_15" position="1390,870" size="260,54" font="Regular;24" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <!-- Footer Buttons -->
    <widget name="key_red" position="160,960" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{red}" halign="center" valign="center" transparent="0" />
    <widget name="key_green" position="330,960" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{green}" halign="center" valign="center" transparent="0" />
    <widget name="key_yellow" position="500,960" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{yellow}" halign="center" valign="center" transparent="0" />
    <widget name="key_blue" position="670,960" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{blue}" halign="center" valign="center" transparent="0" />
    <widget name="key_menu" position="840,960" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{grey}" halign="center" valign="center" transparent="0" />
    <widget name="key_epg" position="1010,960" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{whitegrey}" halign="center" valign="center" transparent="0" />
<widget name="key_info" position="1180,960" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{purple}" halign="center" valign="center" transparent="0" />
<widget name="key_help" position="1350,960" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{orange}" halign="center" valign="center" transparent="0" />
</screen>
    """.format(
        bg=c['background'],
        border=c['border'],
        primary=c['primary'],
        text=c['text'],
        red=b['red'],
        green=b['green'],
        yellow=b['yellow'],
        blue=b['blue'],
        grey=b['grey'],
        whitegrey=b['whitegrey'],
        orange=b['orange'],
        purple=b['purple']
    )

def getGridSkinHD(color_scheme):
    """Generate FHD skin with Grid view"""
    c = COLORS[color_scheme]
    b = BUTTON_COLORS
    
    return """
    <screen name="IPAudioScreenGrid" position="53,16" size="1153,680" title="IPAudio Grid" backgroundColor="#20383636" flags="wfNoBorder">
    <!-- Header -->
    <widget name="title" position="923,80" size="180,27" font="Regular;26" foregroundColor="#FFA500" transparent="1" halign="left" />
    <widget name="server" position="73,43" size="400,33" font="Regular;22" foregroundColor="#FFFFFF" transparent="1" halign="left" />
    <widget name="sync" position="553,80" size="167,27" font="Regular;19" foregroundColor="#00FF00" transparent="1" halign="left" />
    <widget name="audio_delay" position="733,80" size="167,27" font="Regular;17" foregroundColor="#00FFFF" transparent="1" halign="left" />
    <widget name="network_status" position="63,80" size="267,27" font="Regular;17" foregroundColor="#FFFF00" transparent="1" />
    <widget name="countdown" position="340,80" size="200,27" font="Regular;17" foregroundColor="#FF6600" transparent="1" />

    <!-- Selection frame -->
    <widget name="frame" position="63,117" size="193,173" zPosition="1" alphatest="blend" transparent="1" />

    <!-- Row 1 -->
    <widget name="label_1" position="70,127" size="180,20" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_1" position="93,150" size="133,80" alphatest="blend" />
    <widget name="event_1" position="73,233" size="173,36" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_2" position="283,127" size="180,20" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_2" position="307,150" size="133,80" alphatest="blend" />
    <widget name="event_2" position="287,233" size="173,36" font="Regular;17" halign="center" valign="center" foregroundColor="{primary}" transparent="1" />

    <widget name="label_3" position="497,127" size="180,20" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_3" position="520,150" size="133,80" alphatest="blend" />
    <widget name="event_3" position="500,233" size="173,36" font="Regular;17" halign="center" valign="center" foregroundColor="{primary}" transparent="1" />

    <widget name="label_4" position="710,127" size="180,20" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_4" position="733,150" size="133,80" alphatest="blend" />
    <widget name="event_4" position="713,233" size="173,36" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_5" position="923,127" size="180,20" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_5" position="947,150" size="133,80" alphatest="blend" />
    <widget name="event_5" position="927,233" size="173,36" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <!-- Row 2 -->
    <widget name="label_6" position="70,300" size="180,20" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_6" position="93,323" size="133,80" alphatest="blend" />
    <widget name="event_6" position="73,406" size="173,36" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_7" position="283,300" size="180,20" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_7" position="307,323" size="133,80" alphatest="blend" />
    <widget name="event_7" position="287,406" size="173,36" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_8" position="497,300" size="180,20" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_8" position="520,323" size="133,80" alphatest="blend" />
    <widget name="event_8" position="500,406" size="173,36" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_9" position="710,300" size="180,20" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_9" position="733,323" size="133,80" alphatest="blend" />
    <widget name="event_9" position="713,406" size="173,36" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_10" position="923,300" size="180,20" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_10" position="947,323" size="133,80" alphatest="blend" />
    <widget name="event_10" position="927,406" size="173,36" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <!-- Row 3 -->
    <widget name="label_11" position="70,473" size="180,20" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_11" position="93,496" size="133,80" alphatest="blend" />
    <widget name="event_11" position="73,579" size="173,36" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_12" position="283,473" size="180,20" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_12" position="307,496" size="133,80" alphatest="blend" />
    <widget name="event_12" position="287,579" size="173,36" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_13" position="497,473" size="180,20" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_13" position="520,496" size="133,80" alphatest="blend" />
    <widget name="event_13" position="500,579" size="173,36" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_14" position="710,473" size="180,20" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_14" position="733,496" size="133,80" alphatest="blend" />
    <widget name="event_14" position="713,579" size="173,36" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <widget name="label_15" position="923,473" size="180,20" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />
    <widget name="pixmap_15" position="947,496" size="133,80" alphatest="blend" />
    <widget name="event_15" position="927,579" size="173,36" font="Regular;17" halign="center" valign="center" transparent="1" foregroundColor="{primary}" />

    <!-- Footer Buttons -->
    <widget name="key_red" position="107,640" size="107,33" font="Regular;16" foregroundColor="#000000" backgroundColor="{red}" halign="center" valign="center" transparent="0" />
    <widget name="key_green" position="220,640" size="107,33" font="Regular;16" foregroundColor="#000000" backgroundColor="{green}" halign="center" valign="center" transparent="0" />
    <widget name="key_yellow" position="333,640" size="107,33" font="Regular;16" foregroundColor="#000000" backgroundColor="{yellow}" halign="center" valign="center" transparent="0" />
    <widget name="key_blue" position="447,640" size="107,33" font="Regular;16" foregroundColor="#000000" backgroundColor="{blue}" halign="center" valign="center" transparent="0" />
    <widget name="key_menu" position="560,640" size="107,33" font="Regular;16" foregroundColor="#000000" backgroundColor="{grey}" halign="center" valign="center" transparent="0" />
    <widget name="key_epg" position="673,640" size="107,33" font="Regular;16" foregroundColor="#000000" backgroundColor="{whitegrey}" halign="center" valign="center" transparent="0" />
</screen>

    """.format(
        bg=c['background'],
        border=c['border'],
        primary=c['primary'],
        text=c['text'],
        red=b['red'],
        green=b['green'],
        yellow=b['yellow'],
        blue=b['blue'],
        grey=b['grey'],
        whitegrey=b['whitegrey']
    )

# ===========================
# Orange Skins
# ===========================
SKIN_IPAudioScreen_ORANGE_FHD = getSkinFHD('orange')
SKIN_IPAudioSetup_ORANGE_FHD = getSetupSkinFHD('orange')
SKIN_IPAudioPlaylist_ORANGE_FHD = getPlaylistSkinFHD('orange')
SKIN_IPAudioInfo_ORANGE_FHD = getInfoSkinFHD('orange')
SKIN_IPAudioHelp_ORANGE_FHD = getHelpSkinFHD('orange')
SKIN_IPAudioScreenGrid_ORANGE_FHD = getGridSkinFHD('orange')

SKIN_IPAudioScreen_ORANGE_HD = getSkinHD('orange')
SKIN_IPAudioSetup_ORANGE_HD = getSetupSkinHD('orange')
SKIN_IPAudioPlaylist_ORANGE_HD = getPlaylistSkinHD('orange')
SKIN_IPAudioInfo_ORANGE_HD = getInfoSkinHD('orange')
SKIN_IPAudioHelp_ORANGE_HD = getHelpSkinHD('orange')
SKIN_IPAudioScreenGrid_ORANGE_HD = getGridSkinHD('orange')

# ===========================
# Teal Skins
# ===========================
SKIN_IPAudioScreen_TEAL_FHD = getSkinFHD('teal')
SKIN_IPAudioSetup_TEAL_FHD = getSetupSkinFHD('teal')
SKIN_IPAudioPlaylist_TEAL_FHD = getPlaylistSkinFHD('teal')
SKIN_IPAudioInfo_TEAL_FHD = getInfoSkinFHD('teal')
SKIN_IPAudioHelp_TEAL_FHD = getHelpSkinFHD('teal')
SKIN_IPAudioScreenGrid_TEAL_FHD = getGridSkinFHD('teal')

SKIN_IPAudioScreen_TEAL_HD = getSkinHD('teal')
SKIN_IPAudioSetup_TEAL_HD = getSetupSkinHD('teal')
SKIN_IPAudioPlaylist_TEAL_HD = getPlaylistSkinHD('teal')
SKIN_IPAudioInfo_TEAL_HD = getInfoSkinHD('teal')
SKIN_IPAudioHelp_TEAL_HD = getHelpSkinHD('teal')
SKIN_IPAudioScreenGrid_TEAL_HD = getGridSkinHD('teal')

# ===========================
# Lime Skins
# ===========================
SKIN_IPAudioScreen_LIME_FHD = getSkinFHD('lime')
SKIN_IPAudioSetup_LIME_FHD = getSetupSkinFHD('lime')
SKIN_IPAudioPlaylist_LIME_FHD = getPlaylistSkinFHD('lime')
SKIN_IPAudioInfo_LIME_FHD = getInfoSkinFHD('lime')
SKIN_IPAudioHelp_LIME_FHD = getHelpSkinFHD('lime')
SKIN_IPAudioScreenGrid_LIME_FHD = getGridSkinFHD('lime')

SKIN_IPAudioScreen_LIME_HD = getSkinHD('lime')
SKIN_IPAudioSetup_LIME_HD = getSetupSkinHD('lime')
SKIN_IPAudioPlaylist_LIME_HD = getPlaylistSkinHD('lime')
SKIN_IPAudioInfo_LIME_HD = getInfoSkinHD('lime')
SKIN_IPAudioHelp_LIME_HD = getHelpSkinHD('lime')
SKIN_IPAudioScreenGrid_LIME_HD = getGridSkinHD('lime')
