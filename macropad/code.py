from adafruit_macropad import MacroPad

macropad = MacroPad()

KEY_ACTIONS = (
    (macropad.Keycode.ONE, "lightson"),
    (macropad.Keycode.TWO, "lightsoff"),
    (32, "3rd"),
    (macropad.Keycode.FOUR, "4th")
)

ON_COLOR = (0, 0, 255)
OFF_COLOR = (0, 20, 0)
DEBUG=True

macropad.pixels.brightness = 0.5
text_lines = macropad.display_text(title="MacroPad Info")

for i in range (0,11,1):
    macropad.pixels.fill(OFF_COLOR)

LAST_SENT = None  # Track the last sent key

while True:
    event = macropad.keys.events.get()
    if event:
        key = event.key_number
        if key < len(KEY_ACTIONS):
            action = KEY_ACTIONS[key][1]
            if action:
                if DEBUG:
                    print(f"Key {key} pressed. Action: {action} Sending: {KEY_ACTIONS[key][0]}")
                text_lines[0].text = f"Key {key} pressed!"
                text_lines[1].text = f"Action: {action}"
                text_lines[2].text = f"Sending: {KEY_ACTIONS[key][0]}"
                text_lines.show()
                macropad.pixels[key] = ON_COLOR if event.pressed else OFF_COLOR
                if event.pressed:
                    macropad.keyboard_layout.write(action)  # Send the action as text
                    macropad.keyboard.send(KEY_ACTIONS[key][0])
            else:
                if DEBUG:
                    print(f"Key {key}")
                    print(f"sending {key+1}")
                    print(f"pressed? {event.pressed}")
