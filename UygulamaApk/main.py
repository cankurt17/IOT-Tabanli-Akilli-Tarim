from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.picker import MDTimePicker
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.uix.label import MDLabel
from kivy.core.window import Window    
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout  
import requests
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivy.factory import Factory
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine 
from kivymd.uix.boxlayout import MDBoxLayout  
import datetime as dt
from kivymd.uix.bottomsheet import MDListBottomSheet 
from kivy.clock import Clock

Window.size=(400,700) 

KV = '''   
ScreenManager:
    id:'screen_manager'
    HomeScreen:  
    ManSulamaScreen:  
    OtoSulamaScreen: 
    GubreScreen:  
    KayitScreen: 
    SettingScreen:   
    ErrorScreen:   
    EditTextScreen:   
    GelistiriciScreen:  

<GelistiriciScreen>:
    name:'gelistiriciscreen'
    MDBoxLayout:
        orientation: "vertical" 
        MDToolbar:
            title: "Geliştirici"   
            elevation: 6
            left_action_items: [['menu', lambda x: nav_drawer.set_state()]]

        MDFloatLayout:
            Image: 
                source:'icons/logo.png'   
                size_hint_x:0.8
                allow_stretch: True
                halign:'center'    
                pos_hint: {"center_x": .5, "center_y": .8} 
            MDLabel:
                text:'İletşim:'     
                halign:'center'
                font_style:'H6'  
                font_size: 0.035 * root.width 
                pos_hint: {"center_x": .5, "center_y": .6}
            MDSeparator: 
                size_hint_x:.6
                height: "2dp"
                pos_hint: {"center_x": .5, "center_y": .58}  
            Image: 
                source:'icons/gmail.png'    
                size_hint_x: 0.07
                allow_stretch: True
                halign:'center'    
                pos_hint: {"center_x": .3, "center_y": .5} 
            MDLabel:
                text:'iletisim@evogar.com'
                theme_text_color: "Secondary"
                font_size: 0.035 * root.width 
                halign:'center'    
                pos_hint: {"center_x": .55, "center_y": .5}  
            MDLabel:
                text:'v.1.0.0'     
                halign:'center'
                theme_text_color: "Secondary"
                font_size: 0.035 * root.width 
                pos_hint: {"center_x": .5, "center_y": .14}
            MDLabel:
                text:'Can KURT'     
                halign:'center'
                theme_text_color: "Secondary"
                font_size: 0.035 * root.width 
                pos_hint: {"center_x": .5, "center_y": .11}
            MDLabel:
                text:'Mustafa SARIKAYA'     
                halign:'center'
                theme_text_color: "Secondary"
                font_size: 0.035 * root.width 
                pos_hint: {"center_x": .5, "center_y": .08}
            MDLabel:
                text:'Made with love in Kahramanmaras,TURKEY'     
                halign:'center'
                theme_text_color: "Secondary"
                font_size: 0.035 * root.width 
                pos_hint: {"center_x": .5, "center_y": .05}
    MDNavigationDrawer:
        id: nav_drawer
        ContentNavigationDrawer:   
            nav_drawer: nav_drawer 
            screen_manager: root.manager 
 
<EditTextScreen>:
    name:'edittextscreen'
    MDFloatLayout: 
        MDTextField: 
            id:edittext
            halign:'center' 
            input_type:'mail'
            pos_hint: {"center_x": .5 ,"center_y": .85} 
            hint_text: "E-Posta"
            helper_text: "Lütfen mail adresini doğru giriniz."
            helper_text_mode:"on_focus"
            size_hint_x: .75
            height: "30dp"   

        MDRectangleFlatIconButton:
            icon: "exit-to-app"
            text: "Vazgeç"
            halign:'center'
            pos_hint: {"center_x": .3,"center_y":0.5}    
            on_release: app.editCancel() 

        MDRectangleFlatIconButton:
            icon: "database-check"
            text: "KAYDET"
            halign:'center'
            pos_hint: {"center_x": .7,"center_y":0.5}   
            on_release: app.editKayit(edittext.text)

<HomeScreen>: 
    name:'homescreen' 
    MDBoxLayout:
        orientation: "vertical" 
        MDToolbar:
            title: "Anasayfa"   
            elevation: 6
            left_action_items: [['menu', lambda x: nav_drawer.set_state()]] 
        FloatLayout: 
            Image:
                source:'icons/bahce.png'  
                halign:'center' 
                size_hint_x: 0.7
                allow_stretch: True
                pos_hint:{'center_x':.5,'center_y':.8}  
            MDCard: 
                padding: "8dp" 
                size_hint: .47, .17
                pos_hint: {"center_x": .255, "center_y": .5}  
                elevation:10 
                FloatLayout: 
                    Image:
                        source:'icons/water-tap.png'  
                        halign:'center' 
                        size_hint_x: 0.3
                        allow_stretch: True
                        pos_hint:{'center_x':.2,'center_y':.5}  
                    MDLabel:
                        text:'Su durumu:'     
                        halign:'center'
                        font_size: 0.03 * root.width
                        pos_hint: {"center_x": .7, "center_y": .9}
                    MDSeparator:
                        size_hint_x: .5 
                        height: "1dp"
                        pos_hint: {"center_x": .7, "center_y": .8}
                    MDLabel: 
                        id:home_su_durum
                        text: "Açık"
                        pos_hint: {"center_x": .7,"center_y": .6}  
                        font_style:'H6'  
                        font_size: 0.035 * root.width
                        halign:'center'  
                    MDLabel:
                        text:'Debi:'     
                        halign:'center'
                        font_size: 0.03 * root.width
                        pos_hint: {"center_x": .7, "center_y": .36}
                    MDSeparator:
                        size_hint_x: .5 
                        height: "1dp"
                        pos_hint: {"center_x": .7, "center_y": .26}
                    MDLabel: 
                        id:home_su_debi
                        text: '12 L/sa'
                        pos_hint: {"center_x": .7,"center_y": .1}  
                        font_style:'H6'  
                        font_size: 0.035 * root.width
                        halign:'center'  
            MDCard: 
                padding: "8dp" 
                size_hint: .47, .17
                pos_hint: {"center_x": .255, "center_y": .32}  
                elevation:10  
                FloatLayout: 
                    Image:
                        source:'icons/gubre.png'  
                        halign:'center' 
                        size_hint_x: 0.3
                        allow_stretch: True
                        pos_hint:{'center_x':.2,'center_y':.5}  
                    MDLabel:
                        text:'Gübre durumu:'     
                        halign:'center'
                        font_size: 0.03 * root.width
                        pos_hint: {"center_x": .7, "center_y": .9}
                    MDSeparator:
                        size_hint_x: .5 
                        height: "1dp"
                        pos_hint: {"center_x": .7, "center_y": .8}
                    MDLabel: 
                        id:home_gubre_durum
                        text: 'Kapalı'
                        pos_hint: {"center_x": .7,"center_y": .6}  
                        font_style:'H6'  
                        font_size: 0.035 * root.width
                        halign:'center'  
                    MDLabel:
                        text:'Miktar:'     
                        halign:'center'
                        font_size: 0.03 * root.width
                        pos_hint: {"center_x": .7, "center_y": .36}
                    MDSeparator:
                        size_hint_x: .5 
                        height: "1dp"
                        pos_hint: {"center_x": .7, "center_y": .26}
                    MDLabel: 
                        id:home_gubre_miktar
                        text: '6 Litre'
                        pos_hint: {"center_x": .7,"center_y": .1}  
                        font_style:'H6'  
                        font_size: 0.035 * root.width
                        halign:'center'  
            MDCard: 
                padding: "8dp" 
                size_hint: .47, .17
                pos_hint: {"center_x": .255, "center_y": .14}  
                elevation:10 
                FloatLayout: 
                    Image:
                        source:'icons/setting.png'  
                        halign:'center' 
                        size_hint_x: 0.3
                        allow_stretch: True
                        pos_hint:{'center_x':.2,'center_y':.5}  
                    MDLabel:
                        text:'Mod:'     
                        halign:'center'
                        font_size: 0.03 * root.width
                        pos_hint: {"center_x": .7, "center_y": .8}
                    MDSeparator:
                        size_hint_x: .5 
                        height: "1dp"
                        pos_hint: {"center_x": .7, "center_y": .7}
                    MDLabel: 
                        id:home_mod
                        text: 'Manuel'
                        pos_hint: {"center_x": .7,"center_y": .4}  
                        font_style:'H6'  
                        font_size: 0.035 * root.width
                        halign:'center'  
            MDCard: 
                padding: "8dp" 
                size_hint: .47, .17
                pos_hint: {"center_x": .745, "center_y": .5}  
                elevation:10 
                FloatLayout: 
                    Image:
                        source:'icons/gardening.png'  
                        halign:'center' 
                        size_hint_x: 0.3
                        allow_stretch: True
                        pos_hint:{'center_x':.2,'center_y':.5}  
                    MDLabel:
                        text:'Toprak nemi:'     
                        halign:'center'
                        font_size: 0.03 * root.width
                        pos_hint: {"center_x": .7, "center_y": .8}
                    MDSeparator:
                        size_hint_x: .5 
                        height: "1dp"
                        pos_hint: {"center_x": .7, "center_y": .7}
                    MDLabel: 
                        id:home_toprak_nem
                        text: '% 43'
                        pos_hint: {"center_x": .7,"center_y": .4}  
                        font_style:'H6'  
                        font_size: 0.035 * root.width
                        halign:'center'  
            MDCard: 
                padding: "8dp" 
                size_hint: .47, .17
                pos_hint: {"center_x": .745, "center_y": .32}  
                elevation:10 
                FloatLayout: 
                    Image:
                        source:'icons/sun.png'  
                        halign:'center' 
                        size_hint_x: 0.3
                        allow_stretch: True
                        pos_hint:{'center_x':.2,'center_y':.5}  
                    MDLabel:
                        text:'Ortam Sıcaklığı:'     
                        halign:'center'
                        font_size: 0.03 * root.width
                        pos_hint: {"center_x": .7, "center_y": .9}
                    MDSeparator:
                        size_hint_x: .5 
                        height: "1dp"
                        pos_hint: {"center_x": .7, "center_y": .8}
                    MDLabel: 
                        id:home_sicaklik
                        text: '35 °C'
                        pos_hint: {"center_x": .7,"center_y": .6}  
                        font_style:'H6'  
                        font_size: 0.035 * root.width
                        halign:'center'  
                    MDLabel:
                        text:'Nem:'     
                        halign:'center'
                        font_size: 0.03 * root.width
                        pos_hint: {"center_x": .7, "center_y": .36}
                    MDSeparator:
                        size_hint_x: .5 
                        height: "1dp"
                        pos_hint: {"center_x": .7, "center_y": .26}
                    MDLabel: 
                        id:home_nem
                        text: '% 17'
                        pos_hint: {"center_x": .7,"center_y": .1}  
                        font_style:'H6'  
                        font_size: 0.035 * root.width
                        halign:'center'  
            MDCard: 
                padding: "8dp" 
                size_hint: .47, .17
                pos_hint: {"center_x": .745, "center_y": .14}  
                elevation:10 
                FloatLayout: 
                    Image:
                        source:'icons/battery.png'  
                        halign:'center' 
                        size_hint_x: 0.3
                        allow_stretch: True
                        pos_hint:{'center_x':.2,'center_y':.5}  
                    MDLabel:
                        text:'Pil seviyesi:'     
                        halign:'center'
                        font_size: 0.03 * root.width
                        pos_hint: {"center_x": .7, "center_y": .8}
                    MDSeparator:
                        size_hint_x: .5 
                        height: "1dp"
                        pos_hint: {"center_x": .7, "center_y": .7}
                    MDLabel: 
                        id:home_pil 
                        text: '% 43'
                        pos_hint: {"center_x": .7,"center_y": .4}  
                        font_style:'H6'  
                        font_size: 0.035 * root.width
                        halign:'center'   
            
    MDNavigationDrawer:
        id: nav_drawer
        ContentNavigationDrawer:   
            nav_drawer: nav_drawer 
            screen_manager: root.manager

<ErrorScreen>:
    name:'errorscreen'
    MDFloatLayout:
        Image: 
            source:'icons/no-wifi.png'    
            halign:'center'    
            size: self.texture_size
            pos_hint: {"center_x": .5, "center_y": .7}   
        MDLabel:
            text:'Lütfen internet bağlantınızı kontrol ediniz.'
            font_style:'Subtitle2' 
            theme_text_color: "Error"     
            halign:'center'
            font_size: 0.04 * root.width
            pos_hint: {"center_x": .5, "center_y": .3} 

        MDRectangleFlatIconButton:
            icon: "reload"
            text: "Bağlan"
            halign:'center'
            pos_hint: {"center_x": .5, "center_y": .2}   
            background_color:1,0,0,1 
            on_release: app.intKontrol() 
            
<SettingScreen>: 
    name:'settingscreen' 
    MDBoxLayout:
        orientation: "vertical" 
        MDToolbar:
            title: "Ayarlar"    
            elevation: 6
            left_action_items: [['menu', lambda x: nav_drawer.set_state()]]
        FloatLayout:
            MDCard: 
                padding: "8dp" 
                size_hint: .95, .08 
                pos_hint: {"center_x": .5, "center_y": .9}  
                elevation:10
                MDFloatLayout:
                    MDLabel: 
                        text: 'Mod:'
                        pos_hint: {"center_x": .15,"center_y": .5}  
                        font_style:'H6'  
                        font_size: 0.035 * root.width
                        halign:'center'  
                    MDSwitch:
                        id:mod_switch   
                        halign:'center'
                        pos_hint: {"center_x": .5,"center_y": .5}  
                        on_press:  setting_kaydet_button.disabled = False
                        on_release:  setting_kaydet_button.disabled = False
                        on_active:  setting_kaydet_button.disabled = False
                    MDLabel: 
                        text: 'Manuel' if mod_switch.active else 'Otomatik' 
                        pos_hint: {"center_x": .8,"center_y": .5}  
                        font_style:'H6' 
                        font_size: 0.035 * root.width
                        halign:'center'  

            MDCard: 
                padding: "8dp" 
                size_hint: .95, .08 
                pos_hint: {"center_x": .5, "center_y": .81}  
                elevation:10
                MDFloatLayout:  
                    MDLabel:
                        text: "Mail:"
                        font_style:'H6' 
                        pos_hint: {"center_x": .15, "center_y": .5} 
                        halign: 'center'
                        font_size: 0.035 * root.width
                    MDTextButton:
                        id:mail_label
                        text:'bencankurt17@gmail.com'
                        font_size: 0.038 * root.width
                        halign:'center'
                        on_press:app.show_editText('mail_label',mail_label)
                        pos_hint: {"center_x": .65, "center_y": .5} 
            
            MDCard: 
                padding: "8dp" 
                size_hint: .95, .08 
                pos_hint: {"center_x": .5, "center_y": .72}  
                elevation:10
                MDFloatLayout:   
                    MDLabel:
                        text: "Bahçe Alanı:"
                        font_style:'H6' 
                        pos_hint: {"center_x": .15, "center_y": .5} 
                        halign: 'center'
                        font_size: 0.035 * root.width
                    MDTextButton:
                        id:dekar_label
                        text:'1000 m2'
                        font_size: 0.038 * root.width
                        halign:'center'
                        on_press:app.show_editText('dekar_label',dekar_label)
                        pos_hint: {"center_x": .65, "center_y": .5} 
                        


            MDRectangleFlatButton:
                id: setting_kaydet_button  
                pos_hint: {"center_x": .5,"center_y": .2}  
                halign:'center'  
                text: "Kaydedildi"  if setting_kaydet_button.disabled else 'Kaydet'   
                disabled: False  
                on_press: app.settingKayit() 
                text_color: app.theme_cls.primary_color 

    MDNavigationDrawer:
        id: nav_drawer
        ContentNavigationDrawer:   
            nav_drawer: nav_drawer 
            screen_manager: root.manager

<ManSulamaScreen>: 
    name:'mansulamascreen' 
    MDBoxLayout:
        orientation: "vertical" 
        MDToolbar:
            title: "Sulama"   
            elevation: 6
            left_action_items: [['menu', lambda x: nav_drawer.set_state()]]

        FloatLayout:
            MDCard:
                size_hint: .95, .08
                padding:'10dp' 
                pos_hint: {"center_x": .5, "center_y": .9}
                elevation:10
                MDFloatLayout: 
                    MDSwitch: 
                        id:pzt_switch
                        thumb_color_disabled: 0.9,0.9,0.9,0.9
                        pos_hint: {'center_x': .05, 'center_y': .5}
                        on_active: app.switch_kontrol(*args)  
                    MDLabel:
                        text:'Pazartesi'
                        font_style:'H6' 
                        font_size: 0.04 * root.width
                        halign:'center'  
                        pos_hint:{'center_x':.3,'center_y':.5}
                    Image:
                        source:'icons/sulama_clock_on.png' if  pzt_switch.active else 'icons/sulama_clock_off.png'
                        halign:'center' 
                        size: self.texture_size
                        pos_hint:{'center_x':.55,'center_y':.5}  
                    MDTextButton:
                        id:pzt_start
                        text: "22:10" 
                        halign:'center'
                        pos_hint:{'center_x':.7,'center_y':.5}
                        on_press: app.show_time_picker(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:'' 
                        font_size: 0.042 * root.width
                    MDTextButton: 
                        id:pzt_stop
                        text: "22:10" 
                        halign:'center'
                        pos_hint:{'center_x':.9,'center_y':.5}
                        on_press: app.show_time_picker(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:'' 
                        font_size: 0.042 * root.width
            MDCard:
                size_hint: .95, .08 
                padding:'10dp' 
                pos_hint: {"center_x": .5, "center_y": .81}
                elevation:10
                MDFloatLayout: 
                    MDSwitch:
                        thumb_color_disabled: 0.9,0.9,0.9,0.9
                        id:sl_switch
                        pos_hint: {'center_x': .05, 'center_y': .5}
                        on_active: app.switch_kontrol(*args)
                    MDLabel:
                        text:'Salı'
                        font_style:'H6' 
                        font_size: 0.04 * root.width
                        halign:'center'
                        pos_hint:{'center_x':.3,'center_y':.5}
                    Image:
                        source:'icons/sulama_clock_on.png' if  sl_switch.active else 'icons/sulama_clock_off.png'
                        halign:'center' 
                        size: self.texture_size
                        pos_hint:{'center_x':.55,'center_y':.5}  
                    MDTextButton:
                        id:sl_start
                        text: "22:10" 
                        halign:'center'
                        pos_hint:{'center_x':.7,'center_y':.5}
                        on_press: app.show_time_picker(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:'' 
                        font_size: 0.042 * root.width
                    MDTextButton:
                        id:sl_stop
                        text: "22:10" 
                        halign:'center'
                        pos_hint:{'center_x':.9,'center_y':.5}
                        on_press: app.show_time_picker(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:'' 
                        font_size: 0.042 * root.width
            MDCard:
                size_hint: .95, .08
                padding:'10dp' 
                pos_hint: {"center_x": .5, "center_y": .72}
                elevation:10
                MDFloatLayout: 
                    MDSwitch:
                        id:crs_switch
                        thumb_color_disabled: 0.9,0.9,0.9,0.9
                        pos_hint: {'center_x': .05, 'center_y': .5}
                        on_active: app.switch_kontrol(*args)
                    MDLabel:
                        text:'Çarşamba'
                        font_style:'H6' 
                        font_size: 0.04 * root.width
                        halign:'center'
                        pos_hint:{'center_x':.3,'center_y':.5}
                    Image:
                        source:'icons/sulama_clock_on.png' if  crs_switch.active else 'icons/sulama_clock_off.png'
                        halign:'center' 
                        size: self.texture_size
                        pos_hint:{'center_x':.55,'center_y':.5}  
                    MDTextButton:
                        id:crs_start
                        text: "22:10" 
                        halign:'center'
                        pos_hint:{'center_x':.7,'center_y':.5}
                        on_press: app.show_time_picker(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:'' 
                        font_size: 0.042 * root.width
                    MDTextButton:
                        id:crs_stop
                        text: "22:10" 
                        halign:'center'
                        pos_hint:{'center_x':.9,'center_y':.5}
                        on_press: app.show_time_picker(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:'' 
                        font_size: 0.042 * root.width
            MDCard:
                size_hint: .95, .08 
                padding:'10dp' 
                pos_hint: {"center_x": .5, "center_y": .63}
                elevation:10
                MDFloatLayout: 
                    MDSwitch:
                        id:prs_switch
                        thumb_color_disabled: 0.9,0.9,0.9,0.9
                        pos_hint: {'center_x': .05, 'center_y': .5}
                        on_active: app.switch_kontrol(*args)
                    MDLabel:
                        text:'Perşembe'
                        font_style:'H6' 
                        font_size: 0.04 * root.width
                        halign:'center'
                        pos_hint:{'center_x':.3,'center_y':.5}
                    Image:
                        source:'icons/sulama_clock_on.png' if  prs_switch.active else 'icons/sulama_clock_off.png'
                        halign:'center' 
                        size: self.texture_size
                        pos_hint:{'center_x':.55,'center_y':.5}  
                    MDTextButton:
                        id:prs_start
                        text: "22:10" 
                        halign:'center'
                        pos_hint:{'center_x':.7,'center_y':.5}
                        on_press: app.show_time_picker(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:'' 
                        font_size: 0.042 * root.width
                    MDTextButton:
                        id:prs_stop
                        text: "22:10" 
                        halign:'center'
                        pos_hint:{'center_x':.9,'center_y':.5}
                        on_press: app.show_time_picker(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:'' 
                        font_size: 0.042 * root.width
            MDCard:
                size_hint: .95, .08 
                padding:'10dp' 
                pos_hint: {"center_x": .5, "center_y": .54}
                elevation:10
                MDFloatLayout: 
                    MDSwitch:
                        id:cm_switch
                        thumb_color_disabled: 0.9,0.9,0.9,0.9
                        pos_hint: {'center_x': .05, 'center_y': .5}
                        on_active: app.switch_kontrol(*args)
                    MDLabel:
                        text:'Cuma'
                        font_style:'H6' 
                        font_size: 0.04 * root.width
                        halign:'center'
                        pos_hint:{'center_x':.3,'center_y':.5}
                    Image:
                        source:'icons/sulama_clock_on.png' if  cm_switch.active else 'icons/sulama_clock_off.png'
                        halign:'center' 
                        size: self.texture_size
                        pos_hint:{'center_x':.55,'center_y':.5}  
                    MDTextButton:
                        id:cm_start
                        text: "22:10" 
                        halign:'center'
                        pos_hint:{'center_x':.7,'center_y':.5}
                        on_press: app.show_time_picker(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:'' 
                        font_size: 0.042 * root.width

                    MDTextButton:
                        id:cm_stop
                        text: "22:10" 
                        halign:'center'
                        pos_hint:{'center_x':.9,'center_y':.5} 
                        on_press: app.show_time_picker(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:'' 
                        font_size: 0.042 * root.width
            MDCard:
                size_hint: .95, .08
                padding:'10dp' 
                pos_hint: {"center_x": .5, "center_y": .45}
                elevation:10
                MDFloatLayout: 
                    MDSwitch:
                        id:ct_switch
                        thumb_color_disabled: 0.9,0.9,0.9,0.9
                        pos_hint: {'center_x': .05, 'center_y': .5}
                        on_active: app.switch_kontrol(*args)
                    MDLabel:
                        text:'Cumartesi'
                        font_style:'H6' 
                        font_size: 0.04 * root.width
                        halign:'center'
                        pos_hint:{'center_x':.3,'center_y':.5}
                    Image:
                        source:'icons/sulama_clock_on.png' if  ct_switch.active else 'icons/sulama_clock_off.png'
                        halign:'center' 
                        size: self.texture_size
                        pos_hint:{'center_x':.55,'center_y':.5}  
                    MDTextButton:
                        id:ct_start
                        text: "22:10" 
                        halign:'center'
                        pos_hint:{'center_x':.7,'center_y':.5}
                        on_press: app.show_time_picker(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:'' 
                        font_size: 0.042 * root.width
                    MDTextButton:
                        id:ct_stop
                        text: "22:10" 
                        halign:'center'
                        pos_hint:{'center_x':.9,'center_y':.5}
                        on_press: app.show_time_picker(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:'' 
                        font_size: 0.042 * root.width
            MDCard:
                size_hint: .95, .08 
                padding:'10dp' 
                pos_hint: {"center_x": .5, "center_y": .36}
                elevation:10
                MDFloatLayout: 
                    MDSwitch:
                        id:pz_switch
                        thumb_color_disabled: 0.9,0.9,0.9,0.9
                        height: dp(64) 
                        pos_hint: {'center_x': .05, 'center_y': .5}  
                        on_active: app.switch_kontrol(*args)
                    MDLabel:
                        text:'Pazar'
                        font_style:'H6' 
                        font_size: 0.04 * root.width
                        halign:'center'
                        pos_hint:{'center_x':.3,'center_y':.5}
                    Image:
                        source:'icons/sulama_clock_on.png' if  pz_switch.active else 'icons/sulama_clock_off.png'
                        halign:'center' 
                        size: self.texture_size
                        pos_hint:{'center_x':.55,'center_y':.5}  
                    MDTextButton:
                        id:pz_start
                        text: "22:10" 
                        halign:'center'
                        pos_hint:{'center_x':.7,'center_y':.5}
                        on_press: app.show_time_picker(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:'' 
                        font_size: 0.042 * root.width
                    MDTextButton:
                        id:pz_stop
                        text: "22:10" 
                        halign:'center'
                        pos_hint:{'center_x':.9,'center_y':.5}
                        on_press: app.show_time_picker(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:'' 
                        font_size: 0.042 * root.width
            MDRectangleFlatButton:
                id: man_kaydet_button   
                pos_hint: {"center_x": .5,"center_y": .2}  
                halign:'center'
                text: "Kaydedildi"  if man_kaydet_button.disabled else 'Kaydet'   
                disabled: True 
                on_press: app.man_settings_kayit()
                text_color: app.theme_cls.primary_color 

    MDNavigationDrawer:
        id: nav_drawer
        ContentNavigationDrawer:   
            nav_drawer: nav_drawer 
            screen_manager: root.manager

<OtoSulamaScreen>: 
    name:'otosulamascreen' 
    MDBoxLayout:
        orientation: "vertical" 
        MDToolbar:
            title: "Sulama"   
            elevation: 6
            left_action_items: [['menu', lambda x: nav_drawer.set_state()]]

        MDFloatLayout:  
            MDCard: 
                size_hint: .95, .1
                padding:'10dp' 
                pos_hint: {"center_x": .5, "center_y": .7}
                elevation:10
                FloatLayout:   
                    MDLabel:
                        text: "Başlangıç Nemi"
                        font_style:'H6' 
                        font_size: 0.04 * root.width
                        theme_text_color: "Primary" 
                        halign:'center'
                        pos_hint: {"center_x": .18,"center_y": .5}    
                    MDLabel: 
                        id:start_nem_text
                        text: '%25' 
                        font_style:'H6' 
                        theme_text_color: "Primary"
                        font_size:'20dp'
                        halign:'center'
                        font_size: 0.05 * root.width
                        pos_hint: {"center_x": .63,"center_y": .5}  
                    Image:
                        source:'icons/humidity.png' 
                        halign:'center' 
                        size_hint_x: 0.09
                        allow_stretch: True
                        pos_hint:{'center_x':.45,'center_y':.5}  
                    MDTextButton: 
                        text: "Ayarla" 
                        halign:'center'
                        pos_hint: {"center_x": .85,"center_y":0.5}   
                        on_press: app.nem_bottom_sheet(*args,True)    
                        font_size: 0.042 * root.width 

            MDCard: 
                size_hint: .95, .1
                padding:'10dp' 
                pos_hint: {"center_x": .5, "center_y": .59}
                elevation:10
                FloatLayout:   
                    MDLabel:
                        text: "Bitiş Nemi"
                        font_style:'H6' 
                        font_size: 0.04 * root.width
                        theme_text_color: "Primary" 
                        halign:'center'
                        pos_hint: {"center_x": .18,"center_y": .5}    
                    MDLabel: 
                        id:stop_nem_text
                        font_style:'H6' 
                        text: '%55' 
                        theme_text_color: "Primary" 
                        font_size: 0.05 * root.width
                        halign:'center'
                        pos_hint: {"center_x": .63,"center_y": .5}
                    Image:
                        source:'icons/humidity.png' 
                        halign:'center' 
                        size_hint_x: 0.09
                        allow_stretch: True
                        pos_hint:{'center_x':.45,'center_y':.5}  
                    MDTextButton: 
                        text: "Ayarla" 
                        halign:'center'
                        pos_hint: {"center_x": .85,"center_y":0.5}   
                        on_press: app.nem_bottom_sheet(*args,False)    
                        font_size: 0.042 * root.width  

            MDRectangleFlatButton:
                id: oto_kaydet_button  
                pos_hint: {"center_x": .5,"center_y": .2}  
                halign:'center'  
                text: "Kaydedildi"  if oto_kaydet_button.disabled else 'Kaydet'   
                disabled: False  
                on_press: app.nem_kayit() 
                text_color: app.theme_cls.primary_color 
    MDNavigationDrawer:
        id: nav_drawer
        ContentNavigationDrawer:   
            nav_drawer: nav_drawer 
            screen_manager: root.manager

<GubreScreen>: 
    name:'gubrescreen' 
    MDBoxLayout:
        orientation: "vertical" 
        MDToolbar:
            title: "Gübreleme"   
            elevation: 6
            left_action_items: [['menu', lambda x: nav_drawer.set_state()]]

        FloatLayout:
            MDLabel:
                id: gubre_text
                text:'Yalnızca sulamanın açık olduğu günler için gübre ayarı yapabilirsiniz.'  
                font_size: 0.028 * root.width
                halign:'center'  
                theme_text_color:'Secondary'
                pos_hint:{'center_x':.5,'center_y':.97}
            MDCard:
                id:pzt_card
                size_hint: .95, .08
                padding:'10dp' 
                font_size: 0.04 * root.width
                pos_hint: {"center_x": .5, "center_y": .9}
                elevation:10
                MDFloatLayout: 
                    MDSwitch: 
                        id:pzt_switch_gubre
                        font_size: 0.04 * root.width
                        thumb_color_disabled: 0.9,0.9,0.9,0.9
                        pos_hint: {'center_x': .05, 'center_y': .5}
                        on_active: app.gubre_switch_kontrol(*args)  
                    MDLabel:
                        text:'Pazartesi'
                        font_style:'H6' 
                        font_size: 0.04 * root.width
                        halign:'center'  
                        pos_hint:{'center_x':.3,'center_y':.5}
                    Image:
                        source:'icons/setting_gubre_var.png' if  not(pzt_card.disabled) else 'icons/setting_gubre_yok.png'
                        halign:'center' 
                        size: self.texture_size
                        pos_hint:{'center_x':.55,'center_y':.5}  
                    MDTextButton:
                        id:pzt_gubre_miktar
                        text: "10" 
                        halign:'center'
                        font_size: 0.04 * root.width
                        pos_hint:{'center_x':.7,'center_y':.5}
                        on_press: app.show_gubre_miktar_dialog(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:''  
                    MDTextButton:
                        id:pzt_gubre_birim
                        text: "mL/L" 
                        halign:'center'
                        font_size: 0.04 * root.width
                        pos_hint:{'center_x':.85,'center_y':.5}
                        on_press: app.select_gubre_birim(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:''  
            MDCard:
                id:sl_card
                size_hint: .95, .08
                padding:'10dp' 
                font_size: 0.04 * root.width
                pos_hint: {"center_x": .5, "center_y": .81}
                elevation:10
                MDFloatLayout: 
                    MDSwitch: 
                        id:sl_switch_gubre
                        font_size: 0.04 * root.width
                        thumb_color_disabled: 0.9,0.9,0.9,0.9
                        pos_hint: {'center_x': .05, 'center_y': .5}
                        on_active: app.gubre_switch_kontrol(*args)  
                    MDLabel:
                        text:'Salı'
                        font_style:'H6' 
                        font_size: 0.04 * root.width
                        halign:'center'  
                        pos_hint:{'center_x':.3,'center_y':.5}
                    Image:
                        source:'icons/setting_gubre_var.png' if  not(sl_card.disabled) else 'icons/setting_gubre_yok.png'
                        halign:'center' 
                        size: self.texture_size
                        pos_hint:{'center_x':.55,'center_y':.5}  
                    MDTextButton:
                        id:sl_gubre_miktar
                        text: "10" 
                        halign:'center'
                        font_size: 0.04 * root.width
                        pos_hint:{'center_x':.7,'center_y':.5}
                        on_press: app.show_gubre_miktar_dialog(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:''  
                    MDTextButton:
                        id:sl_gubre_birim
                        text: "mL/L" 
                        halign:'center'
                        font_size: 0.04 * root.width
                        pos_hint:{'center_x':.85,'center_y':.5}
                        on_press: app.select_gubre_birim(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:''  
            MDCard:
                id:crs_card
                size_hint: .95, .08
                padding:'10dp' 
                font_size: 0.04 * root.width
                pos_hint: {"center_x": .5, "center_y": .72}
                elevation:10
                MDFloatLayout: 
                    MDSwitch: 
                        id:crs_switch_gubre
                        font_size: 0.04 * root.width
                        thumb_color_disabled: 0.9,0.9,0.9,0.9
                        pos_hint: {'center_x': .05, 'center_y': .5}
                        on_active: app.gubre_switch_kontrol(*args)  
                    MDLabel:
                        text:'Çarşamba'
                        font_style:'H6' 
                        font_size: 0.04 * root.width
                        halign:'center'  
                        pos_hint:{'center_x':.3,'center_y':.5}
                    Image:
                        source:'icons/setting_gubre_var.png' if  not(crs_card.disabled) else 'icons/setting_gubre_yok.png'
                        halign:'center' 
                        size: self.texture_size
                        pos_hint:{'center_x':.55,'center_y':.5}  
                    MDTextButton:
                        id:crs_gubre_miktar
                        text: "10" 
                        halign:'center'
                        font_size: 0.04 * root.width
                        pos_hint:{'center_x':.7,'center_y':.5}
                        on_press: app.show_gubre_miktar_dialog(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:''  
                    MDTextButton:
                        id:crs_gubre_birim
                        text: "mL/L" 
                        halign:'center'
                        font_size: 0.04 * root.width
                        pos_hint:{'center_x':.85,'center_y':.5}
                        on_press: app.select_gubre_birim(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:''  
            MDCard:
                id:prs_card
                size_hint: .95, .08
                padding:'10dp' 
                font_size: 0.04 * root.width
                pos_hint: {"center_x": .5, "center_y": .63}
                elevation:10
                MDFloatLayout: 
                    MDSwitch: 
                        id:prs_switch_gubre
                        font_size: 0.04 * root.width
                        thumb_color_disabled: 0.9,0.9,0.9,0.9
                        pos_hint: {'center_x': .05, 'center_y': .5}
                        on_active: app.gubre_switch_kontrol(*args)  
                    MDLabel:
                        text:'Perşembe'
                        font_style:'H6' 
                        font_size: 0.04 * root.width
                        halign:'center'  
                        pos_hint:{'center_x':.3,'center_y':.5}
                    Image:
                        source:'icons/setting_gubre_var.png' if  not(prs_card.disabled) else 'icons/setting_gubre_yok.png'
                        halign:'center' 
                        size: self.texture_size
                        pos_hint:{'center_x':.55,'center_y':.5}  
                    MDTextButton:
                        id:prs_gubre_miktar
                        text: "10" 
                        halign:'center'
                        font_size: 0.04 * root.width
                        pos_hint:{'center_x':.7,'center_y':.5}
                        on_press: app.show_gubre_miktar_dialog(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:''  
                    MDTextButton:
                        id:prs_gubre_birim
                        text: "mL/L" 
                        halign:'center'
                        font_size: 0.04 * root.width
                        pos_hint:{'center_x':.85,'center_y':.5}
                        on_press: app.select_gubre_birim(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:'' 
            MDCard:
                id:cm_card
                size_hint: .95, .08
                padding:'10dp' 
                font_size: 0.04 * root.width
                pos_hint: {"center_x": .5, "center_y": .54}
                elevation:10
                MDFloatLayout: 
                    MDSwitch: 
                        id:cm_switch_gubre
                        font_size: 0.04 * root.width
                        thumb_color_disabled: 0.9,0.9,0.9,0.9
                        pos_hint: {'center_x': .05, 'center_y': .5}
                        on_active: app.gubre_switch_kontrol(*args)  
                    MDLabel:
                        text:'Cuma'
                        font_style:'H6' 
                        font_size: 0.04 * root.width
                        halign:'center'  
                        pos_hint:{'center_x':.3,'center_y':.5}
                    Image:
                        source:'icons/setting_gubre_var.png' if  not(cm_card.disabled) else 'icons/setting_gubre_yok.png'
                        halign:'center' 
                        size: self.texture_size
                        pos_hint:{'center_x':.55,'center_y':.5}  
                    MDTextButton:
                        id:cm_gubre_miktar
                        text: "10" 
                        halign:'center'
                        font_size: 0.04 * root.width
                        pos_hint:{'center_x':.7,'center_y':.5}
                        on_press: app.show_gubre_miktar_dialog(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:''  
                    MDTextButton:
                        id:cm_gubre_birim
                        text: "mL/L" 
                        halign:'center'
                        font_size: 0.04 * root.width
                        pos_hint:{'center_x':.85,'center_y':.5}
                        on_press: app.select_gubre_birim(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:'' 
            MDCard:
                id:ct_card
                size_hint: .95, .08
                padding:'10dp' 
                font_size: 0.04 * root.width
                pos_hint: {"center_x": .5, "center_y": .45}
                elevation:10
                MDFloatLayout: 
                    MDSwitch: 
                        id:ct_switch_gubre
                        font_size: 0.04 * root.width
                        thumb_color_disabled: 0.9,0.9,0.9,0.9
                        pos_hint: {'center_x': .05, 'center_y': .5}
                        on_active: app.gubre_switch_kontrol(*args)  
                    MDLabel:
                        text:'Cumartesi'
                        font_style:'H6' 
                        font_size: 0.04 * root.width
                        halign:'center'  
                        pos_hint:{'center_x':.3,'center_y':.5}
                    Image:
                        source:'icons/setting_gubre_var.png' if  not(ct_card.disabled) else 'icons/setting_gubre_yok.png'
                        halign:'center' 
                        size: self.texture_size
                        pos_hint:{'center_x':.55,'center_y':.5}  
                    MDTextButton:
                        id:ct_gubre_miktar
                        text: "10" 
                        halign:'center'
                        font_size: 0.04 * root.width
                        pos_hint:{'center_x':.7,'center_y':.5}
                        on_press: app.show_gubre_miktar_dialog(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:''  
                    MDTextButton:
                        id:ct_gubre_birim
                        text: "mL/L" 
                        halign:'center'
                        font_size: 0.04 * root.width
                        pos_hint:{'center_x':.85,'center_y':.5}
                        on_press: app.select_gubre_birim(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:'' 
            MDCard:
                id:pz_card
                size_hint: .95, .08
                padding:'10dp' 
                font_size: 0.04 * root.width
                pos_hint: {"center_x": .5, "center_y": .36}
                elevation:10
                MDFloatLayout: 
                    MDSwitch: 
                        id:pz_switch_gubre
                        font_size: 0.04 * root.width
                        thumb_color_disabled: 0.9,0.9,0.9,0.9
                        pos_hint: {'center_x': .05, 'center_y': .5}
                        on_active: app.gubre_switch_kontrol(*args)   
                    MDLabel:
                        text:'Pazar'
                        font_style:'H6' 
                        font_size: 0.04 * root.width
                        halign:'center'  
                        pos_hint:{'center_x':.3,'center_y':.5} 
                    Image:
                        source:'icons/setting_gubre_var.png' if  not(pz_card.disabled) else 'icons/setting_gubre_yok.png'
                        halign:'center' 
                        size: self.texture_size
                        pos_hint:{'center_x':.55,'center_y':.5}  
                    MDTextButton:
                        id:pz_gubre_miktar
                        text: "10" 
                        halign:'center'
                        font_size: 0.04 * root.width
                        pos_hint:{'center_x':.7,'center_y':.5}
                        on_press: app.show_gubre_miktar_dialog(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:''  
                    MDTextButton:
                        id:pz_gubre_birim
                        text: "mL/L" 
                        halign:'center'
                        font_size: 0.04 * root.width
                        pos_hint:{'center_x':.85,'center_y':.5}
                        on_press: app.select_gubre_birim(*args) 
                        disabled_color:0.9,0.9,0.9,0.9
                        background_color:1,1,1,1
                        background_disabled_normal:'' 
            MDRectangleFlatButton:
                id: gubre_kaydet_button   
                pos_hint: {"center_x": .5,"center_y": .2}  
                halign:'center'
                text: "Kaydedildi"  if gubre_kaydet_button.disabled else 'Kaydet'   
                disabled: False 
                on_press: app.gubre_settings_kayit()
                text_color: app.theme_cls.primary_color 

    MDNavigationDrawer:
        id: nav_drawer
        ContentNavigationDrawer:   
            nav_drawer: nav_drawer 
            screen_manager: root.manager

<KayitScreen>: 
    name:'kayitscreen' 
    MDBoxLayout:
        orientation: "vertical" 
        MDToolbar:
            title: "Kayıtlar"   
            elevation: 6
            left_action_items: [['menu', lambda x: nav_drawer.set_state()]]

        ScrollView: 
            MDGridLayout:
                id: kayitPage
                cols: 1
                adaptive_height: True

    MDNavigationDrawer:
        id: nav_drawer
        ContentNavigationDrawer:   
            nav_drawer: nav_drawer 
            screen_manager: root.manager 

<ContentNavigationDrawer>:    
    Screen: 
        Image:
            source:'icons/cloud.png'   
            pos_hint: {"center_y": .8}   
            allow_stretch: True
            size_hint_x: 1
            size_hint_y:1
            
        MDList:    
            pos_hint: {"center_y": .6}   
            OneLineIconListItem:
                text: "Anasayfa"     
                on_release:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current='homescreen'
                IconLeftWidget:
                    icon: "icons/navigation/nav_home.png"  
                    pos_hint: {"center_x": .7 ,"center_y": .5}
                    size: "24dp", "24dp"
                     
            OneLineIconListItem:
                text: "Sulama"     
                on_release:
                    root.nav_drawer.set_state("close") 
                on_press: 
                    app.DayScreen() 
                IconLeftWidget:
                    icon: "icons/navigation/nav_sulama.png"  
                    pos_hint: {"center_x": .7 ,"center_y": .5}
                    size: "24dp", "24dp"
            OneLineIconListItem:
                text: "Gübreleme"     
                on_release:
                    root.nav_drawer.set_state("close") 
                on_press: 
                    app.GubreScreen() 
                IconLeftWidget:
                    icon: "icons/navigation/nav_gubre.png"  
                    pos_hint: {"center_x": .7 ,"center_y": .5}
                    size: "24dp", "24dp"
            OneLineIconListItem:
                text: "Kayıtlar"     
                on_release:
                    root.nav_drawer.set_state("close") 
                on_press: 
                    app.KayitScreen() 
                IconLeftWidget:
                    icon: "icons/navigation/nav_calendar.png"  
                    pos_hint: {"center_x": .7 ,"center_y": .5}
                    size: "24dp", "24dp"
            OneLineIconListItem:
                text: "Ayarlar"      
                on_release:
                    root.nav_drawer.set_state("close")
                on_press: 
                    app.SettingScreen() 
                IconLeftWidget:
                    icon: "icons/navigation/nav_ayarlar.png"  
                    pos_hint: {"center_x": .7 ,"center_y": .5}
                    size: "24dp", "24dp"
        MDList:   
            OneLineIconListItem:
                text: "Hakkında"      
                IconLeftWidget:
                    icon: "icons/navigation/nav_info.png"  
                    pos_hint: {"center_x": .7 ,"center_y": .5}
                    size: "24dp", "24dp"
            OneLineIconListItem:
                text: "Geliştirici" 
                on_press:      
                    root.nav_drawer.set_state("close") 
                    root.screen_manager.current='gelistiriciscreen'
                IconLeftWidget:
                    icon: "icons/navigation/nav_gelistirici.png"  
                    pos_hint: {"center_x": .7 ,"center_y": .5}
                    size: "24dp", "24dp"

<CustomSheet@BoxLayout>:
    orientation: "vertical"
    size_hint_y: None
    height: "800dp" 
    MDFloatLayout: 
        MDIcon:
            icon:'water'
            halign:'center'
            pos_hint: {"center_x": .45 ,"center_y": .8}
            font_size:'26dp'
        MDLabel: 
            id:bottom_sheet_nem_text
            text: '%' + str(int(stop_nem.value))
            theme_text_color: "Primary"
            font_size:'22dp'
            halign:'center'
            pos_hint: {"center_x": .55,"center_y": .8}

        MDSlider:  
            id:stop_nem
            size_hint:.8,1 
            show_off:False
            min: 0 if app.nem_durum else int(app.start_nem.text.strip('%')) + 1
            max: int(app.stop_nem.text.strip('%')) -1 if app.nem_durum else 100
            halign:'center'
            pos_hint: {"center_x": .5,"center_y":0.6}   

        MDRectangleFlatIconButton:
            icon: "database-check"
            text: "KAYDET"
            halign:'center'
            pos_hint: {"center_x": .5,"center_y":0.4}   
            on_release: app.set_nem(bottom_sheet_nem_text.text)
  
<Content>
    adaptive_height: True 
    height: '140dp'
    MDCard: 
        MDFloatLayout:
            padding:'5dp'
            MDLabel:
                text:'Mod:'
                halign:'center'
                font_style:'Subtitle2'
                pos_hint: {"center_x": .15,"center_y":0.8}
            MDLabel:
                id:tablo_mod
                text:"Otomatik"
                halign:'center'  
                font_style:'Subtitle2'
                theme_text_color:'Secondary'
                pos_hint: {"center_x": .35,"center_y":0.8}
            MDLabel:
                text:'Bşl saati:'
                halign:'center' 
                font_style:'Subtitle2'
                pos_hint: {"center_x": .15,"center_y":0.6}
            MDLabel:
                id:tablo_bslSaat
                text:'22:10'
                halign:'center'
                font_style:'Subtitle2'
                theme_text_color:'Secondary'
                pos_hint: {"center_x": .35,"center_y":0.6}
            MDLabel:
                text:'Bitiş saati:'
                halign:'center'
                font_style:'Subtitle2'
                pos_hint: {"center_x": .15,"center_y":0.4}
            MDLabel:
                id:tablo_btsSaat
                text:'22:30'
                halign:'center'
                font_style:'Subtitle2'
                theme_text_color:'Secondary'
                pos_hint: {"center_x": .35,"center_y":0.4}
                
            MDLabel:
                text:'Gübre:'
                halign:'center'
                font_style:'Subtitle2'
                pos_hint: {"center_x": .15,"center_y":0.2}
            MDLabel:
                id:tablo_gubre
                text:'Yok'
                halign:'center'
                font_style:'Subtitle2'
                theme_text_color:'Secondary'
                pos_hint: {"center_x": .35,"center_y":0.2}

            MDLabel:
                text:'Toplam:'
                halign:'center'
                font_style:'Subtitle2'
                pos_hint: {"center_x": .6,"center_y":0.8}
            MDLabel:
                id:tablo_toplam
                text:'20 Dk'
                halign:'center'
                font_style:'Subtitle2'
                theme_text_color:'Secondary'
                pos_hint: {"center_x": .8,"center_y":0.8}
            MDLabel:
                text:'Bşl nemi:'
                halign:'center'
                font_style:'Subtitle2'
                pos_hint: {"center_x": .6,"center_y":0.6}
            MDLabel:
                id:tablo_bslNem
                text:'% 10'
                halign:'center'
                font_style:'Subtitle2'
                theme_text_color:'Secondary'
                pos_hint: {"center_x": .8,"center_y":0.6}
            MDLabel:
                text:'Bitiş nemi:'
                halign:'center'
                font_style:'Subtitle2'
                pos_hint: {"center_x": .6,"center_y":0.4}
            MDLabel:
                id:tablo_btsNem
                text:'% 20'
                halign:'center'
                font_style:'Subtitle2'
                theme_text_color:'Secondary'
                pos_hint: {"center_x": .8,"center_y":0.4}

            MDLabel:
                text:'Arıza:'
                halign:'center'
                font_style:'Subtitle2'
                pos_hint: {"center_x": .6,"center_y":0.2}
            MDLabel:
                id:tablo_hata
                text:'-'
                halign:'center'
                font_style:'Subtitle2'
                theme_text_color:'Secondary'
                pos_hint: {"center_x": .8,"center_y":0.2}
 

'''

class Content(MDBoxLayout):
    pass
 
class ManSulamaScreen(Screen):  
    pass    

class OtoSulamaScreen(Screen):  
    pass    

class HomeScreen(Screen): 
    pass 
 
class GubreScreen(Screen): 
    pass 
 
class KayitScreen(Screen): 
    pass 

class SettingScreen(Screen): 
    pass 

class ErrorScreen(Screen): 
    pass 
 
class EditTextScreen(Screen): 
    pass 

class ContentNavigationDrawer(BoxLayout): 
    pass

class GelistiriciScreen(Screen): 
    pass 

sm = ScreenManager()
sm.add_widget(HomeScreen(name='homescreen'))
sm.add_widget(ManSulamaScreen(name='mansulamascreen'))
sm.add_widget(OtoSulamaScreen(name='otosulamascreen'))
sm.add_widget(GubreScreen(name='gubrescreen'))
sm.add_widget(KayitScreen(name='kayitscreen'))
sm.add_widget(SettingScreen(name='settingscreen'))
sm.add_widget(ErrorScreen(name='errorgscreen'))
sm.add_widget(EditTextScreen(name='edittextscreen')) 
sm.add_widget(GelistiriciScreen(name='gelistiriciscreen'))



class MainApp(MDApp):
    dialog = None
    custom_sheet = None 
    su="abc"
    def build(self):  
        self.screen = Builder.load_string(KV) 
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"   
 
        return  self.screen

    def on_start(self): 
        self.postUrl = 'https://enlodi.com/Sulama-Proje/post-esp-data.php'

        self.home_su_durum = self.screen.get_screen('homescreen').ids.home_su_durum  
        self.home_su_debi = self.screen.get_screen('homescreen').ids.home_su_debi  
        self.home_toprak_nem = self.screen.get_screen('homescreen').ids.home_toprak_nem  
        self.home_sicaklik= self.screen.get_screen('homescreen').ids.home_sicaklik  
        self.home_nem = self.screen.get_screen('homescreen').ids.home_nem   
        self.home_pil = self.screen.get_screen('homescreen').ids.home_pil   
        self.home_gubre_durum = self.screen.get_screen('homescreen').ids.home_gubre_durum  
        self.home_gubre_miktar = self.screen.get_screen('homescreen').ids.home_gubre_miktar  
        self.home_mod = self.screen.get_screen('homescreen').ids.home_mod  

        self.getHomeData(0)

        Clock.schedule_interval(self.getHomeData, 10)

    
    def getHomeData(self,dt):   
        try: 
            if(self.screen.current == 'homescreen'):
                self.arduino_data = requests.get('http://enlodi.com/Sulama-Proje/tablo-arduino.php')
                self.arduino_data = self.arduino_data.json()
                self.home_toprak_nem.text = '% ' + self.arduino_data["0"]["toprak_nem"]
                self.home_su_durum.text = 'Açık' if self.arduino_data["0"]["durum"] == "1" else 'Kapalı'
                self.home_nem.text = '% ' + self.arduino_data["0"]["ortam_nem"]
                self.home_sicaklik.text = self.arduino_data["0"]["ortam_sicaklik"] + ' °C'
                self.home_su_debi.text = self.arduino_data["0"]["su_debi"] + ' L/sa'
                self.home_pil.text = '% ' + self.arduino_data["0"]["pil"] 
                self.home_gubre_durum.text = 'Açık' if self.arduino_data["0"]["gubre_durum"] == "1" else 'Kapalı'
                self.home_gubre_miktar.text = self.arduino_data["0"]["gubre_miktar"] + ' Litre' 
                self.mod_data = requests.get('http://enlodi.com/Sulama-Proje/tablo-mod.php')
                self.mod_data = self.mod_data.json()
                self.home_mod.text = 'Manuel'  if self.mod_data["0"]["durum"] == "1" else 'Otomatik'
        except requests.exceptions.ConnectionError:
            self.setError() 

    def switch_kontrol(self, durum, value):

        for i in self.day_list:
            if durum == i[1]:
                i[2].disabled = not (i[1].active)
                i[3].disabled = not (i[1].active)

        self.man_kaydet_button.disabled = False

    def ManScreen(self):  
        self.pzt_switch = self.screen.get_screen('mansulamascreen').ids.pzt_switch
        self.pzt_start = self.screen.get_screen('mansulamascreen').ids.pzt_start
        self.pzt_stop = self.screen.get_screen('mansulamascreen').ids.pzt_stop

        self.sl_switch = self.screen.get_screen('mansulamascreen').ids.sl_switch
        self.sl_start = self.screen.get_screen('mansulamascreen').ids.sl_start
        self.sl_stop = self.screen.get_screen('mansulamascreen').ids.sl_stop

        self.crs_switch = self.screen.get_screen('mansulamascreen').ids.crs_switch
        self.crs_start = self.screen.get_screen('mansulamascreen').ids.crs_start
        self.crs_stop = self.screen.get_screen('mansulamascreen').ids.crs_stop

        self.prs_switch = self.screen.get_screen('mansulamascreen').ids.prs_switch
        self.prs_start = self.screen.get_screen('mansulamascreen').ids.prs_start
        self.prs_stop = self.screen.get_screen('mansulamascreen').ids.prs_stop

        self.cm_switch = self.screen.get_screen('mansulamascreen').ids.cm_switch
        self.cm_start = self.screen.get_screen('mansulamascreen').ids.cm_start
        self.cm_stop = self.screen.get_screen('mansulamascreen').ids.cm_stop

        self.ct_switch = self.screen.get_screen('mansulamascreen').ids.ct_switch
        self.ct_start = self.screen.get_screen('mansulamascreen').ids.ct_start
        self.ct_stop = self.screen.get_screen('mansulamascreen').ids.ct_stop

        self.pz_switch = self.screen.get_screen('mansulamascreen').ids.pz_switch
        self.pz_start = self.screen.get_screen('mansulamascreen').ids.pz_start
        self.pz_stop = self.screen.get_screen('mansulamascreen').ids.pz_stop

        self.man_kaydet_button = self.screen.get_screen('mansulamascreen').ids.man_kaydet_button

        
        self.day_list = [
            ["Pazartesi", self.pzt_switch, self.pzt_start, self.pzt_stop],
            ["Salı", self.sl_switch, self.sl_start, self.sl_stop],
            ["Çarşamba", self.crs_switch, self.crs_start, self.crs_stop],
            ["Perşembe", self.prs_switch, self.prs_start, self.prs_stop],
            ["Cuma", self.cm_switch, self.cm_start, self.cm_stop],
            ["Cumartesi", self.ct_switch, self.ct_start, self.ct_stop],
            ["Pazar", self.pz_switch, self.pz_start, self.pz_stop],
        ] 
          
        self.get_mandays_data() 
    def OtoScreen(self): 

        self.start_nem = self.screen.get_screen('otosulamascreen').ids.start_nem_text
        self.stop_nem = self.screen.get_screen('otosulamascreen').ids.stop_nem_text
        self.oto_kaydet_button = self.screen.get_screen('otosulamascreen').ids.oto_kaydet_button
        try:
            self.nem_data = requests.get('http://enlodi.com/Sulama-Proje/tablo-nem.php')
            self.nem_data = self.nem_data.json()
            self.start_nem.text = '%' + str(self.nem_data["0"]["start"])
            self.stop_nem.text = '%' + str(self.nem_data["0"]["stop"])
        except requests.exceptions.ConnectionError:
            self.setError()

    def DayScreen(self): 
        try:
            self.mod_data = requests.get('http://enlodi.com/Sulama-Proje/tablo-mod.php')
            self.mod_data = self.mod_data.json()
            self.modd = 1 if self.mod_data["0"]["durum"] == "1" else 0
            
            if self.modd == 1:
                self.ManScreen()
            else:
                self.OtoScreen()
            self.screen.current='mansulamascreen' if self.modd  else 'otosulamascreen'   
        except requests.exceptions.ConnectionError:
            self.setError()

    def man_settings_kayit(self): 
        try:
            for i in self.day_list: 
                
                myobj = {'api_key': 'tPmAT5Ab3j7F9', 'day': i[0], 'start': i[2].text, 'stop': i[3].text,
                        'durum': 1 if i[1].active else 0,'toplam':0, 'tablo': 'tablo_days'}
                requests.post(self.postUrl, data=myobj)
                
            self.man_kaydet_button.disabled = True 
            myobj = {'api_key': 'tPmAT5Ab3j7F9', 'durum': 1, 'tablo': 'tablo_kayit'}
            requests.post(self.postUrl, data=myobj)
        except requests.exceptions.ConnectionError:
            self.setError()

    def show_time_picker(self, data):
        self.data = data
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

    def get_time(self, instance, time):
        self.yedekSaat = self.data.text
        if time.hour < 10:
            saat = '0' + str(time.hour)
        else:
            saat = str(time.hour)
        if time.minute < 10:
            dk = '0' + str(time.minute)
        else:
            dk = str(time.minute)

        self.zaman = saat + ":" + dk
        self.data.text = self.zaman
        self.saat_kontrol()
        return time

    def saat_kontrol(self):
        self.man_kaydet_button.disabled = False
        """
        for i in self.day_list:
            start = int(i[2].text.replace(":",""))
            stop = int(i[3].text.replace(":",""))
            if start > stop : 
                self.show_alert_dialog()
                self.dialog.title = "Saat Uyarısı!" 
                self.dialog.text = i[0]+" günü başlangıç saati bitiş saatinden geride olmalıdır."
                self.data.text = self.yedekSaat 
        """ 
              
    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Başlık",
                text= "Metin",
                buttons=[
                    MDFlatButton(
                        text="OK", 
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_dialog
                    ), 
                ],
            )
        self.dialog.open()
     

    def close_dialog(self,obj):
        self.dialog.dismiss()

    def get_mandays_data(self):
        try:
            self.days_data = requests.get('http://enlodi.com/Sulama-Proje/tablo-days.php')
            self.days_data = self.days_data.json()
            day = 0
            for i in self.day_list:
                i[2].text = self.days_data[str(day)]["start"]
                i[3].text = self.days_data[str(day)]["stop"]
                i[1].active = int(self.days_data[str(day)]["durum"])
                i[2].disabled = not (i[1].active)
                i[3].disabled = not (i[1].active)
                day += 1
        except requests.exceptions.ConnectionError:
            self.setError()

    def SettingScreen(self): 
        try:
            self.mod_switch = self.screen.get_screen('settingscreen').ids.mod_switch
            self.setting_kaydet_button = self.screen.get_screen('settingscreen').ids.setting_kaydet_button
            self.mail_label = self.screen.get_screen('settingscreen').ids.mail_label
 
            self.mod_data = requests.get('http://enlodi.com/Sulama-Proje/tablo-mod.php')
            self.mod_data = self.mod_data.json()
            self.mod_switch.active = 1 if self.mod_data["0"]["durum"] == "1" else 0
            self.mail_label.text = self.mod_data["0"]["mail"]

            self.screen.current =  'settingscreen'
        except requests.exceptions.ConnectionError:
            self.setError()

    def settingKayit(self):
        try:
            myobj = {'api_key': 'tPmAT5Ab3j7F9', 'durum': 1 if self.mod_switch.active else 0, 'tablo': 'tablo_mod'}
            requests.post(self.postUrl, data=myobj)
            
            myobj = {'api_key': 'tPmAT5Ab3j7F9', 'durum': self.mail_label.text , 'tablo': 'tablo_mail'}
            requests.post(self.postUrl, data=myobj)
            myobj = {'api_key': 'tPmAT5Ab3j7F9', 'durum': 1, 'tablo': 'tablo_kayit'}
            requests.post(self.postUrl, data=myobj)
            self.setting_kaydet_button.disabled = True
        except requests.exceptions.ConnectionError:
            self.setError()

    def nem_bottom_sheet(self, button, durum):
        self.nem_durum = durum
        self.custom_sheet = MDCustomBottomSheet(screen=Factory.CustomSheet())
        self.custom_sheet.open()
        
    def set_nem(self, value):
        try:
            if self.nem_durum:
                self.start_nem.text = value
            else:
                self.stop_nem.text = value
            self.oto_kaydet_button.disabled = False
            self.custom_sheet.dismiss()
        except requests.exceptions.ConnectionError:
            self.setError() 

    def nem_kayit(self):
        try:  
            myobj = {'api_key': 'tPmAT5Ab3j7F9', 'start': self.start_nem.text.strip('%'),
                    'stop': self.stop_nem.text.strip('%'), 'tablo': 'tablo_nem'}
            requests.post(self.postUrl, data=myobj)
            myobj = {'api_key': 'tPmAT5Ab3j7F9', 'durum': 1, 'tablo': 'tablo_kayit'}
            requests.post(self.postUrl, data=myobj)
            self.oto_kaydet_button.disabled = True
        except requests.exceptions.ConnectionError:
            self.setError()

    def KayitScreen(self):  
        self.create_table()

    def create_table(self):
        try:
            table_data = requests.get('http://enlodi.com/Sulama-Proje/tablo-sulamaKayit.php')
            table_data = table_data.json()

            self.errorList=["-","Evg-001","Evg-002","Evg-003"]
            dataList = list()
            for i in table_data:
                data = list()
                data.append(table_data[str(i)]["id"])
                data.append(table_data[str(i)]["day"])
                data.append(table_data[str(i)]["date"])
                data.append(table_data[str(i)]["start"])
                data.append(table_data[str(i)]["stop"])
                data.append(table_data[str(i)]["count"])
                data.append(table_data[str(i)]["start_nem"])
                data.append(table_data[str(i)]["stop_nem"])
                data.append(table_data[str(i)]["mod_durum"])
                data.append(table_data[str(i)]["gubre"])
                data.append(table_data[str(i)]["hata"])
                dataList.append(data)

            self.table_data = dataList 
    
            for i in range(len(table_data)):
                id_=i
                self.panel = MDExpansionPanel(
                    icon="icons/tablo/table"+self.table_data[i][10]+".png",   
                    content=Content(),  
                    panel_cls=MDExpansionPanelTwoLine(
                        text=dt.datetime.strptime(str(f"{self.table_data[i][2]}"), "%Y-%m-%d").strftime("%d/%m/%Y"),
                        secondary_text=self.table_data[i][0]+"-"+self.table_data[i][1], 
                    )
                )
                # pylint: disable=no-member
                self.panel.bind(on_open=self.set_table)
                self.screen.get_screen('kayitscreen').ids.kayitPage.add_widget(self.panel) 
            
            self.screen.current = 'kayitscreen' 
        except requests.exceptions.ConnectionError:
            self.setError()
            
    def set_table(self,instance):  
        id = instance.panel_cls.secondary_text.split("-")[0] 
        for i in self.table_data:
            if int(i[0])==int(id):
                instance.content.ids.tablo_bslSaat.text=i[3]
                instance.content.ids.tablo_btsSaat.text=i[4]
                instance.content.ids.tablo_toplam.text=i[5]+" Dk"
                instance.content.ids.tablo_bslNem.text="% "+i[6]
                instance.content.ids.tablo_btsNem.text="% "+i[7]
                instance.content.ids.tablo_mod.text=i[8]
                instance.content.ids.tablo_gubre.text="Var" if i[9]=="1" else "Yok"
                instance.content.ids.tablo_hata.text= self.errorList[int(i[10])-1]

    
    def GubreScreen(self): 
        try:
            self.pzt_switch_gubre = self.screen.get_screen('gubrescreen').ids.pzt_switch_gubre
            self.pzt_gubre_miktar = self.screen.get_screen('gubrescreen').ids.pzt_gubre_miktar
            self.pzt_gubre_birim = self.screen.get_screen('gubrescreen').ids.pzt_gubre_birim

            self.sl_switch_gubre = self.screen.get_screen('gubrescreen').ids.sl_switch_gubre
            self.sl_gubre_miktar = self.screen.get_screen('gubrescreen').ids.sl_gubre_miktar
            self.sl_gubre_birim = self.screen.get_screen('gubrescreen').ids.sl_gubre_birim
            
            self.crs_switch_gubre = self.screen.get_screen('gubrescreen').ids.crs_switch_gubre
            self.crs_gubre_miktar = self.screen.get_screen('gubrescreen').ids.crs_gubre_miktar
            self.crs_gubre_birim = self.screen.get_screen('gubrescreen').ids.crs_gubre_birim
            
            self.prs_switch_gubre = self.screen.get_screen('gubrescreen').ids.prs_switch_gubre
            self.prs_gubre_miktar = self.screen.get_screen('gubrescreen').ids.prs_gubre_miktar
            self.prs_gubre_birim = self.screen.get_screen('gubrescreen').ids.prs_gubre_birim
            
            self.cm_switch_gubre = self.screen.get_screen('gubrescreen').ids.cm_switch_gubre
            self.cm_gubre_miktar = self.screen.get_screen('gubrescreen').ids.cm_gubre_miktar
            self.cm_gubre_birim = self.screen.get_screen('gubrescreen').ids.cm_gubre_birim
            
            self.ct_switch_gubre = self.screen.get_screen('gubrescreen').ids.ct_switch_gubre
            self.ct_gubre_miktar = self.screen.get_screen('gubrescreen').ids.ct_gubre_miktar
            self.ct_gubre_birim = self.screen.get_screen('gubrescreen').ids.ct_gubre_birim
            
            self.pz_switch_gubre = self.screen.get_screen('gubrescreen').ids.pz_switch_gubre
            self.pz_gubre_miktar = self.screen.get_screen('gubrescreen').ids.pz_gubre_miktar
            self.pz_gubre_birim = self.screen.get_screen('gubrescreen').ids.pz_gubre_birim
            
            self.gubre_kaydet_button = self.screen.get_screen('gubrescreen').ids.gubre_kaydet_button

            self.pzt_card = self.screen.get_screen('gubrescreen').ids.pzt_card
            self.sl_card = self.screen.get_screen('gubrescreen').ids.sl_card
            self.crs_card = self.screen.get_screen('gubrescreen').ids.crs_card
            self.prs_card = self.screen.get_screen('gubrescreen').ids.prs_card
            self.cm_card = self.screen.get_screen('gubrescreen').ids.cm_card
            self.ct_card = self.screen.get_screen('gubrescreen').ids.ct_card
            self.pz_card = self.screen.get_screen('gubrescreen').ids.pz_card

            self.gubre_text = self.screen.get_screen('gubrescreen').ids.gubre_text

            self.gubre_cards = [self.pzt_card,self.sl_card,self.crs_card,self.prs_card,self.cm_card,self.ct_card,self.pz_card]

            self.ManScreen()
    
            self.gubre_day_list = [
                ["Pazartesi", self.pzt_switch_gubre, self.pzt_gubre_miktar, self.pzt_gubre_birim], 
                ["Salı", self.sl_switch_gubre, self.sl_gubre_miktar, self.sl_gubre_birim],
                ["Çarşamba", self.crs_switch_gubre, self.crs_gubre_miktar, self.crs_gubre_birim],
                ["Perşembe", self.prs_switch_gubre, self.prs_gubre_miktar, self.prs_gubre_birim],
                ["Cuma", self.cm_switch_gubre, self.cm_gubre_miktar, self.cm_gubre_birim],
                ["Cumartesi", self.ct_switch_gubre, self.ct_gubre_miktar, self.ct_gubre_birim],
                ["Pazar", self.pz_switch_gubre, self.pz_gubre_miktar, self.pz_gubre_birim],
            ] 

            for id,item in enumerate(self.day_list):
                if item[1].active == 1:
                    self.gubre_cards[id].disabled=False
                else:
                    self.gubre_cards[id].disabled=True

            for i in self.gubre_day_list:
                if i[1].active == 0:
                    i[2].disabled = True 
                    i[3].disabled = True

            
            self.gubre_birim = ["mL","L"] 

            
            self.get_gubredays_data()

            
            self.mod_data = requests.get('http://enlodi.com/Sulama-Proje/tablo-mod.php')
            self.mod_data = self.mod_data.json()
            self.modd = 1 if self.mod_data["0"]["durum"] == "1" else 0

            if self.modd == 1: 
                self.gubre_text.text='Yalnızca sulamanın açık olduğu günler için gübre ayarı yapabilirsiniz.'
            else:   
                self.gubre_text.text="Yalnızca manuel mod için gübre ayarı yapabilirsiniz."
                for i in self.gubre_cards:
                    i.disabled=True
            self.screen.current='gubrescreen'
        except requests.exceptions.ConnectionError:
            self.setError()

    def gubre_switch_kontrol(self, durum, value):

        for i in self.gubre_day_list:
            if durum == i[1]:
                i[2].disabled = not (i[1].active)
                i[3].disabled = not (i[1].active)

        self.gubre_kaydet_button.disabled = False
    
    def gubre_settings_kayit(self):  
        try:
            for i in self.gubre_day_list: 
                myobj = {'api_key': 'tPmAT5Ab3j7F9', 'day': i[0], 'start': 1 if i[1].active else 0, 'stop': i[2].text,
                        'durum': self.gubre_birim.index(i[3].text), 'tablo': 'tablo_gubre'}
                requests.post(self.postUrl, data=myobj) 
            myobj = {'api_key': 'tPmAT5Ab3j7F9', 'durum': 1, 'tablo': 'tablo_kayit'}
            requests.post(self.postUrl, data=myobj)
            self.gubre_kaydet_button.disabled = True 

        except requests.exceptions.ConnectionError:
            self.setError()

    def show_gubre_miktar_dialog(self, value): 
        self.show_editText("gubre_miktar",value) 
     
    
    def select_gubre_birim(self,value): 
        self.inGubre = value 
        bottom_sheet_menu = MDListBottomSheet()

        self.gubre_birimler={"mL":"mililitre","L":"Litre"}

        for i, k in self.gubre_birimler.items():
            bottom_sheet_menu.add_item(
                str(i) + '  ' + k,
                lambda x, y=i: self.callback_for_menu_items(
                    y
                ), 
            )
        bottom_sheet_menu.open()

    def callback_for_menu_items(self, birim): 
        self.inGubre.text = birim

    def get_gubredays_data(self): 
        try:
            self.days_data = requests.get('http://enlodi.com/Sulama-Proje/tablo-days-gubre.php')
            self.days_data = self.days_data.json()
            day = 0
            for i in self.gubre_day_list:
                i[2].text = self.days_data[str(day)]["miktar"]
                i[3].text = self.gubre_birim[int(self.days_data[str(day)]["birim"])]
                i[1].active = int(self.days_data[str(day)]["gubre"])
                i[2].disabled = not (i[1].active)
                i[3].disabled = not (i[1].active)
                day += 1 
        except requests.exceptions.ConnectionError:
            self.setError()
      
    
    def show_editText(self,value,_id): 
        self.ekran = self.screen.current
        self.editTextId = _id
        self.editValue = value  
        self.editText = self.screen.get_screen('edittextscreen').ids.edittext  
        self.editText.text=""
        if(self.editValue=='mail_label'):
            self.editText.hint_text="E-Posta"
            self.editText.helper_text="Lütfen mail adresini doğru giriniz." 
        elif(self.editValue=='dekar_label'):
            self.editText.hint_text="Alan(metrekare)"
            self.editText.helper_text="Lütfen bahçe alanını m2 olarak giriniz."
        elif(self.editValue=='gubre_miktar'):
            self.editText.hint_text="Gübre miktarı"  
            self.editText.helper_text="Lütfen sadece tam sayı giriniz.Örn: 10 , 150 , 200"
             
        self.screen.current='edittextscreen'

    def editKayit(self, edittext): 
        self.edittext = edittext 
        if(self.editValue=='mail_label'):
            if self.edittext == "":
                self.screen.current= self.ekran
            elif  edittext.count("@") !=1 or edittext.count(".") !=1 : 
                self.dialog.title = "Girdi Uyarısı!"
                self.dialog.text = "Lütfen mailinizi kontrol ediniz."
                self.show_alert_dialog() 
            else:
                self.editTextId.text = edittext
                self.setting_kaydet_button.disabled = False
                self.screen.current= self.ekran
        elif(self.editValue=='dekar_label'):
            try: 
                if self.edittext  == "":
                    self.screen.current= self.ekran
                else:
                    text = float(self.edittext)
                    self.editTextId.text = str(text) +" m2"
                    self.setting_kaydet_button.disabled = False 
                    self.screen.current= self.ekran
            except: 
                self.show_alert_dialog()
                self.dialog.title = "Girdi Uyarısı!"
                self.dialog.text = "Lütfen sadece sayı giriniz."
                pass  
        elif(self.editValue=='gubre_miktar'):
            try: 
                if self.edittext  == "":
                    self.screen.current= self.ekran
                else:
                    text = int(self.edittext)
                    self.editTextId.text = str(text) 
                    self.gubre_kaydet_button.disabled = False 
                    self.screen.current= self.ekran
            except: 
                self.show_alert_dialog()
                self.dialog.title = "Girdi Uyarısı!"
                self.dialog.text = "Lütfen sadece tam sayı giriniz."
                pass 
    def editCancel(self):
        self.screen.current= self.ekran
     
    def setError(self): 
        self.screen.current='errorscreen' 
    
    def intKontrol(self):
        try:
            requests.get("https://www.google.com/")
            self.screen.current='homescreen'
        except:
            pass

 
MainApp().run()