import customtkinter as ctk
import os
from PIL import Image

class DragManager:
    def __init__(self, controller):
        self.app = controller
        self.dragged_index = None
        self.dragged_frame = None
        self.drag_window = None

    def on_drag_start(self, event, index, frame):
        self.dragged_index = index
        self.dragged_frame = frame

        self.dragged_frame.configure(fg_color=("gray90", "gray10"), border_color=("gray70", "gray30"), border_width=1)
        for child in self.dragged_frame.winfo_children():
            try:
                child.configure(text_color=("gray80", "gray40"))
            except:
                pass

        self.drag_window = ctk.CTkToplevel(self.app)
        self.drag_window.overrideredirect(True)
        self.drag_window.attributes("-alpha", 0.9)
        self.drag_window.lift()

        ghost_frame = ctk.CTkFrame(self.drag_window, fg_color=("gray85", "gray20"), 
                                   corner_radius=8, border_width=2, border_color="#3a7ebf")
        ghost_frame.pack(fill="both", expand=True)

        path = self.app.image_paths[index]
        try:
            img = Image.open(path)
            img.thumbnail((40, 40))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(40, 40))
            lbl_img = ctk.CTkLabel(ghost_frame, image=ctk_img, text="")
            lbl_img.pack(side="left", padx=10, pady=5)
        except:
            pass

        filename = os.path.basename(path)
        if len(filename) > 25:
            filename = filename[:22] + "..."

        lbl_name = ctk.CTkLabel(ghost_frame, text=filename, width=150, anchor="w", font=ctk.CTkFont(weight="bold"))
        lbl_name.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        self.drag_window.geometry(f"+{event.x_root + 15}+{event.y_root + 15}")

    def on_drag_motion(self, event):
        if self.drag_window and self.drag_window.winfo_exists():
            self.drag_window.geometry(f"+{event.x_root + 15}+{event.y_root + 15}")

        y_mouse = event.y_root
        children = [w for w in self.app.ui.preview_frame.winfo_children() if isinstance(w, ctk.CTkFrame)]

        for widget in children:
            if widget == self.dragged_frame:
                continue

            widget_top = widget.winfo_rooty()
            widget_bottom = widget_top + widget.winfo_height()

            if widget_top - 5 <= y_mouse <= widget_bottom + 5:
                widget.configure(border_color="#3a7ebf", border_width=2)
            else:
                widget.configure(border_color=("gray70", "gray30"), border_width=1)

    def on_drag_release(self, event):
        try:
            if self.drag_window and self.drag_window.winfo_exists():
                self.drag_window.destroy()

            y_release = event.y_root
            new_index = self.dragged_index

            children = [w for w in self.app.ui.preview_frame.winfo_children() if isinstance(w, ctk.CTkFrame)]
            
            for i, widget in enumerate(children):
                if widget == self.dragged_frame:
                    continue
                    
                widget_top = widget.winfo_rooty()
                widget_bottom = widget_top + widget.winfo_height()
                
                if widget_top - 5 <= y_release <= widget_bottom + 5:
                    new_index = i
                    break
            else:
                if children and y_release > children[-1].winfo_rooty() + children[-1].winfo_height():
                    new_index = len(self.app.image_paths) - 1

            if new_index != self.dragged_index:
                item = self.app.image_paths.pop(self.dragged_index)
                self.app.image_paths.insert(new_index, item)
            
            self.app.refresh_preview()
        except Exception:
            self.app.refresh_preview()