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
    'red': '#ff0069',      # Exit/Cancel
    'green': '#00ffa9',    # Save/Reset
    'yellow': '#ffe800',   # Help
    'blue': '#0094ff',     # Info
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
    <screen name="IPAudioScreen" position="center,center" size="880,720" flags="wfNoBorder">
        <!-- Border layer (bottom) -->
        <eLabel name="" position="0,0" size="880,720" zPosition="-3" backgroundColor="{border}" />
        <!-- Black background layer (top, 1px smaller on each side) -->
        <eLabel name="" position="1,1" size="878,718" zPosition="-2" backgroundColor="{bg}" />
        
        <!-- Title -->
        <widget name="title" position="680,20" size="180,50" font="Regular;22" foregroundColor="{primary}" backgroundColor="{bg}" halign="center" valign="center" transparent="0" />
        
        <!-- Header -->
        <widget name="server" position="20,20" size="640,50" font="Regular;32" foregroundColor="#000000" backgroundColor="{primary}" halign="center" valign="center" transparent="0" />
        
        <!-- Info bar -->
        <widget name="sync" position="20,85" size="300,30" font="Regular;20" foregroundColor="{primary}" backgroundColor="{bg}" halign="left" transparent="0" />
        <widget name="audio_delay" position="340,85" size="300,30" font="Regular;20" foregroundColor="{primary}" backgroundColor="{bg}" halign="left" transparent="0" />
        <widget name="network_status" position="660,85" size="200,30" font="Regular;20" foregroundColor="{primary}" backgroundColor="{bg}" halign="left" transparent="0" />
        
        <!-- Channel List (840px width, 500px height = 10 items x 50px) -->
        <widget name="list" position="20,140" size="840,500" backgroundColor="{bg}" foregroundColor="{text}" foregroundColorSelected="#000000" backgroundColorSelected="{primary}" itemHeight="50" scrollbarMode="showOnDemand" scrollbarBorderWidth="1" scrollbarBorderColor="{primary}" scrollbarBackgroundColor="#1a1a1a" scrollbarForegroundColor="{primary}" transparent="0" />
        
        <!-- Footer Buttons (Red, Green, Yellow, Blue) -->
        <widget name="key_red" position="20,655" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{red}" halign="center" valign="center" transparent="0" />
        <widget name="key_green" position="190,655" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{green}" halign="center" valign="center" transparent="0" />
        <widget name="key_yellow" position="360,655" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{yellow}" halign="center" valign="center" transparent="0" />
        <widget name="key_blue" position="530,655" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{blue}" halign="center" valign="center" transparent="0" />
        <widget name="key_menu" position="700,655" size="160,50" font="Regular;22" foregroundColor="#ffffff" backgroundColor="{bg}" halign="center" valign="center" transparent="0" />
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

def getSetupSkinFHD(color_scheme):
    """Generate FHD setup screen skin"""
    c = COLORS[color_scheme]
    b = BUTTON_COLORS
    
    return """
    <screen name="IPAudioSetup" position="center,center" size="880,650" flags="wfNoBorder">
        <!-- Border layer (bottom) -->
        <eLabel name="" position="0,0" size="880,650" zPosition="-3" backgroundColor="{border}" />
        <!-- Black background layer (top, 1px smaller on each side) -->
        <eLabel name="" position="1,1" size="878,648" zPosition="-2" backgroundColor="{bg}" />
        
        <!-- Header -->
        <eLabel position="20,20" size="840,50" text="IPAudio Settings" font="Regular;28" foregroundColor="#000000" backgroundColor="{primary}" halign="center" valign="center" transparent="0" />
        
        <!-- Config List (500px height = 10 items x 50px) -->
        <widget name="config" position="20,90" size="840,500" backgroundColor="{bg}" foregroundColor="{text}" foregroundColorSelected="#000000" backgroundColorSelected="{primary}" itemHeight="50" scrollbarMode="showOnDemand" scrollbarBorderWidth="1" scrollbarBorderColor="{primary}" scrollbarForegroundColor="{primary}" transparent="0" />
        
        <!-- Footer Buttons -->
        <widget source="key_green" render="Label" position="190,595" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{green}" halign="center" valign="center" transparent="0" />
        <widget source="key_red" render="Label" position="20,595" size="160,50" font="Regular;22" foregroundColor="#000000" backgroundColor="{red}" halign="center" valign="center" transparent="0" />
    </screen>
    """.format(
        bg=c['background'],
        border=c['border'],
        primary=c['primary'],
        text=c['text'],
        red=b['red'],
        green=b['green']
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
    <screen name="IPAudioScreen" position="center,center" size="600,490" flags="wfNoBorder">
        <!-- Border layer (bottom) -->
        <eLabel name="" position="0,0" size="600,490" zPosition="-3" backgroundColor="{border}" />
        <!-- Black background layer (top, 1px smaller on each side) -->
        <eLabel name="" position="1,1" size="598,488" zPosition="-2" backgroundColor="{bg}" />
        
        <!-- Title -->
        <widget name="title" position="463,14" size="122,20" font="Regular;15" foregroundColor="{primary}" backgroundColor="{bg}" halign="right" valign="center" transparent="0" />
        
        <!-- Header -->
        <widget name="server" position="14,14" size="435,34" font="Regular;22" foregroundColor="{text}" backgroundColor="{primary}" halign="left" valign="center" transparent="0" />
        
        <!-- Info bar -->
        <widget name="sync" position="14,58" size="204,20" font="Regular;14" foregroundColor="{primary}" backgroundColor="#1a1a1a" halign="left" transparent="0" />
        <widget name="audio_delay" position="231,58" size="204,20" font="Regular;14" foregroundColor="{primary}" backgroundColor="#1a1a1a" halign="left" transparent="0" />
        <widget name="network_status" position="449,58" size="136,20" font="Regular;14" foregroundColor="{primary}" backgroundColor="#1a1a1a" halign="left" transparent="0" />
        
        <!-- Channel List (571px width, 340px height = 5.86 items x 58px, round to 6) -->
        <widget name="list" position="14,95" size="571,348" backgroundColor="{bg}" foregroundColor="{text}" itemHeight="58" scrollbarMode="showOnDemand" scrollbarBorderWidth="1" scrollbarBorderColor="{primary}" scrollbarBackgroundColor="#1a1a1a" scrollbarForegroundColor="{primary}" transparent="0" />
        
        <!-- Footer Buttons (Red, Green, Yellow, Blue) -->
        <widget name="key_red" position="14,446" size="136,34" font="Regular;15" foregroundColor="#ffffff" backgroundColor="{red}" halign="center" valign="center" transparent="0" />
        <widget name="key_green" position="163,446" size="136,34" font="Regular;15" foregroundColor="#000000" backgroundColor="{green}" halign="center" valign="center" transparent="0" />
        <widget name="key_yellow" position="313,446" size="136,34" font="Regular;15" foregroundColor="#000000" backgroundColor="{yellow}" halign="center" valign="center" transparent="0" />
        <widget name="key_blue" position="463,446" size="122,34" font="Regular;15" foregroundColor="#ffffff" backgroundColor="{blue}" halign="center" valign="center" transparent="0" />
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
        <widget source="key_red" render="Label" position="306,404" size="122,34" font="Regular;15" foregroundColor="#ffffff" backgroundColor="{red}" halign="center" valign="center" transparent="0" />
    </screen>
    """.format(
        bg=c['background'],
        border=c['border'],
        primary=c['primary'],
        text=c['text'],
        red=b['red'],
        green=b['green']
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

# ===========================
# Orange Skins
# ===========================
SKIN_IPAudioScreen_ORANGE_FHD = getSkinFHD('orange')
SKIN_IPAudioSetup_ORANGE_FHD = getSetupSkinFHD('orange')
SKIN_IPAudioPlaylist_ORANGE_FHD = getPlaylistSkinFHD('orange')
SKIN_IPAudioInfo_ORANGE_FHD = getInfoSkinFHD('orange')
SKIN_IPAudioHelp_ORANGE_FHD = getHelpSkinFHD('orange')

SKIN_IPAudioScreen_ORANGE_HD = getSkinHD('orange')
SKIN_IPAudioSetup_ORANGE_HD = getSetupSkinHD('orange')
SKIN_IPAudioPlaylist_ORANGE_HD = getPlaylistSkinHD('orange')
SKIN_IPAudioInfo_ORANGE_HD = getInfoSkinHD('orange')
SKIN_IPAudioHelp_ORANGE_HD = getHelpSkinHD('orange')

# ===========================
# Teal Skins
# ===========================
SKIN_IPAudioScreen_TEAL_FHD = getSkinFHD('teal')
SKIN_IPAudioSetup_TEAL_FHD = getSetupSkinFHD('teal')
SKIN_IPAudioPlaylist_TEAL_FHD = getPlaylistSkinFHD('teal')
SKIN_IPAudioInfo_TEAL_FHD = getInfoSkinFHD('teal')
SKIN_IPAudioHelp_TEAL_FHD = getHelpSkinFHD('teal')

SKIN_IPAudioScreen_TEAL_HD = getSkinHD('teal')
SKIN_IPAudioSetup_TEAL_HD = getSetupSkinHD('teal')
SKIN_IPAudioPlaylist_TEAL_HD = getPlaylistSkinHD('teal')
SKIN_IPAudioInfo_TEAL_HD = getInfoSkinHD('teal')
SKIN_IPAudioHelp_TEAL_HD = getHelpSkinHD('teal')

# ===========================
# Lime Skins
# ===========================
SKIN_IPAudioScreen_LIME_FHD = getSkinFHD('lime')
SKIN_IPAudioSetup_LIME_FHD = getSetupSkinFHD('lime')
SKIN_IPAudioPlaylist_LIME_FHD = getPlaylistSkinFHD('lime')
SKIN_IPAudioInfo_LIME_FHD = getInfoSkinFHD('lime')
SKIN_IPAudioHelp_LIME_FHD = getHelpSkinFHD('lime')

SKIN_IPAudioScreen_LIME_HD = getSkinHD('lime')
SKIN_IPAudioSetup_LIME_HD = getSetupSkinHD('lime')
SKIN_IPAudioPlaylist_LIME_HD = getPlaylistSkinHD('lime')
SKIN_IPAudioInfo_LIME_HD = getInfoSkinHD('lime')
SKIN_IPAudioHelp_LIME_HD = getHelpSkinHD('lime')
