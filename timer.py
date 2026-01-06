import tkinter as tk
import time
import threading

class FloatingStudyTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Timer")

        # Frameless & always on top
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        # Default position (bottom-right) – adjust as needed
        self.root.geometry("200x80+1400+900")

        # Timer variables
        self.running = False
        self.start_time = None
        self.elapsed_time = 0

        # Main frame
        self.frame = tk.Frame(root, bg="black")
        self.frame.pack(fill="both", expand=True)

        # Timer display
        self.label = tk.Label(self.frame, text="00:00:00",
                              font=("Arial", 20, "bold"),
                              fg="white", bg="black")
        self.label.pack(fill="both", expand=True)

        # Buttons frame
        btn_frame = tk.Frame(self.frame, bg="black")
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="▶", command=self.start_timer,
                  width=5, bg="green", fg="white").pack(side="left", expand=True, fill="x")
        tk.Button(btn_frame, text="⏸", command=self.stop_timer,
                  width=5, bg="orange", fg="white").pack(side="left", expand=True, fill="x")
        tk.Button(btn_frame, text="🔄", command=self.reset_timer,
                  width=5, bg="red", fg="white").pack(side="left", expand=True, fill="x")
        tk.Button(btn_frame, text="❌", command=self.root.destroy,
                  width=5, bg="gray", fg="white").pack(side="left", expand=True, fill="x")

        # Make window draggable everywhere
        self.widgets = [self.frame, self.label, btn_frame]
        for widget in self.widgets:
            widget.bind("<ButtonPress-1>", self.start_move)
            widget.bind("<ButtonRelease-1>", self.stop_move)
            widget.bind("<B1-Motion>", self.on_motion)

        # For dragging
        self.x = None
        self.y = None

    def update_timer(self):
        while self.running:
            now = time.time()
            self.elapsed_time = int(now - self.start_time)
            h, m, s = self.format_time(self.elapsed_time)
            self.label.config(text=f"{h:02d}:{m:02d}:{s:02d}")
            time.sleep(1)

    def start_timer(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            t = threading.Thread(target=self.update_timer)
            t.daemon = True
            t.start()

    def stop_timer(self):
        self.running = False

    def reset_timer(self):
        self.running = False
        self.elapsed_time = 0
        self.label.config(text="00:00:00")

    def format_time(self, seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return h, m, s

    # --- Dragging methods ---
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def on_motion(self, event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.root.geometry(f"+{x}+{y}")


# Run app
root = tk.Tk()
app = FloatingStudyTimer(root)
groot.mainloop()

