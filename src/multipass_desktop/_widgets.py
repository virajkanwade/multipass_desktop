import tkinter as tk
from tkinter.font import Font


class InstancesListFrame(tk.Frame):
    def __init__(self, master, multipass_client, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.multipass_client = multipass_client

        self._create_layout()
        self._load_instances_list()

    def _create_layout(self):
        def _on_configure(event):
            # update scrollregion after starting 'mainloop'
            # when all widgets are in canvas
            self.instances_canvas.configure(scrollregion=self.instances_canvas.bbox(tk.ALL))
            self.instances_canvas.itemconfig(self.instances_canvas_window, width=event.width)

        def _bound_to_mousewheel(event):
            self.instances_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbound_to_mousewheel(event):
            self.instances_canvas.unbind_all("<MouseWheel>")

        def _on_mousewheel(event):
            self.instances_canvas.yview_scroll(int(-1*(event.delta/5)), tk.UNITS)

        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.instances_canvas = tk.Canvas(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.instances_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.instances_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.instances_canvas.bind('<Configure>', _on_configure)
        self.instances_canvas.bind('<Enter>', _bound_to_mousewheel)
        self.instances_canvas.bind('<Leave>', _unbound_to_mousewheel)

        self.instances_list = tk.Frame(self.instances_canvas, bg='blue')
        self.instances_canvas_window = self.instances_canvas.create_window((0, 0), window=self.instances_list, anchor=tk.NW)

    def _load_instances_list(self):
        instances_list = self.multipass_client.instances_list()

        for instance in instances_list:
            lvmi = ListVMInstance(self.instances_list, instance, highlightbackground="#7b7b7b", highlightcolor="#7b7b7b", highlightthickness=1)
            lvmi.pack(side=tk.TOP, anchor=tk.NW, fill=tk.X, expand=True)


class InstanceInfoFrame(tk.Frame):
    def __init__(self, master, multipass_client, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.multipass_client = multipass_client


class ListVMInstance(tk.Frame):
    def __init__(self, master, instance, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.instance_name = tk.Label(
            self,
            text=instance['name'],
            font=Font(
                size=18,
                weight='bold'
            )
        )
        self.instance_name.pack(anchor=tk.NW, fill=tk.Y, expand=True)

        self.instance_status = tk.Label(self, text=instance['status'])
        self.instance_status.pack(anchor=tk.NW, fill=tk.Y, expand=True)

        self.instance_release = tk.Label(self, text=instance['release'])
        self.instance_release.pack(anchor=tk.NW, fill=tk.Y, expand=True)
