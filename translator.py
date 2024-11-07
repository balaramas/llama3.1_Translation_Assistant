import tkinter as tk
from tkinter import ttk
from pynput import keyboard
import subprocess
import threading
import ollama

class TranslationAssistant:
    def __init__(self):
        self.languages = {
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Italian": "it",
            "Portuguese": "pt",
            "Chinese": "zh",
            "Japanese": "ja",
            "Korean": "ko",
            "Russian": "ru"
        }

        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

    def on_key_press(self, key):
        try:
            if key == keyboard.Key.f6:
                # Show language selector window
                self.show_language_selector()
        except AttributeError:
            pass

    def show_language_selector(self):
        # Create language selection window
        self.lang_window = tk.Tk()
        self.lang_window.title("Select Target Language")
        window_width = 300
        window_height = 150
        screen_width = self.lang_window.winfo_screenwidth()
        screen_height = self.lang_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.lang_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Create and pack language dropdown
        label = ttk.Label(self.lang_window, text="Select target language:")
        label.pack(pady=10)

        self.selected_lang = tk.StringVar()
        lang_dropdown = ttk.Combobox(
            self.lang_window,
            textvariable=self.selected_lang,
            values=list(self.languages.keys())
        )
        lang_dropdown.set("Spanish")  # Default selection
        lang_dropdown.pack(pady=10)

        # Create translate button
        translate_btn = ttk.Button(
            self.lang_window,
            text="Translate",
            command=self.translate_text
        )
        translate_btn.pack(pady=10)
        self.lang_window.mainloop()

    def translate_text(self):
        # Get selected text from clipboard
        text_to_translate = self.paste_from_clipboard()
        target_lang = self.languages[self.selected_lang.get()]

        # Close language selector window
        self.lang_window.destroy()
        prompt = f"Translate the following text to {self.selected_lang.get()}:\n\n{text_to_translate}"

        # Run translation in a separate thread to avoid GUI freezing
        threading.Thread(target=self.perform_translation, args=(prompt,)).start()

    def perform_translation(self, prompt):
        try:
            # Change model name accordingly
            response = ollama.generate(model='llama3.1', prompt=prompt) 
            translated_text = response['response']
            self.show_result(translated_text)
        except Exception as e:
            self.show_result(f"Translation error: {str(e)}")

    def show_result(self, text):
        # Create result window
        result_window = tk.Tk()
        result_window.title("Translation Result")

        # Center the window
        window_width = 400
        window_height = 300
        screen_width = result_window.winfo_screenwidth()
        screen_height = result_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        result_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Create text widget with scrollbar
        text_widget = tk.Text(result_window, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        # Pack widgets
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Insert translation result
        text_widget.insert("1.0", text)

        # Add copy button
        copy_btn = ttk.Button(
            result_window,
            text="Copy to Clipboard",
            command=lambda: self.copy_to_clipboard(text)
        )
        copy_btn.pack(pady=10)
        result_window.mainloop()

    def copy_to_clipboard(self, text):
        subprocess.run(['wl-copy'], input=text.encode('utf-8'))

    def paste_from_clipboard(self):
        result = subprocess.run(['wl-paste'], capture_output=True, text=True)
        return result.stdout

if __name__ == "__main__":
    app = TranslationAssistant()
    # Keep the main thread running
    while True:
        pass  
