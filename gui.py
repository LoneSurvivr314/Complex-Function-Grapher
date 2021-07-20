from tkinter.constants import TRUE
import PySimpleGUI as sg

layout = [[sg.Button("Add keyframe"), sg.Button("Preview Keyframe")],
          [sg.Button("Render Animation")]]

window = sg.Window('Animation Editor', layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    if event == "Add keyframe":
        equation = sg.popup_get_text("Enter equation in terms of z", "Enter equation", "z")
        print(equation)
    print(event, values)

window.close()