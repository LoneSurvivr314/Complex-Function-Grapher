import PySimpleGUI as sg

layout = [[sg.Button("Add keyframe"), sg.Button("Preview Keyframe")],[sg.Button("Render Animation")]]

window = sg.Window('Animation Editor', layout)

event, values = window.read()

window.close()

sg.Popup(event, values)