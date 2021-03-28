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

        self.instances_canvas.focus_set()

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
        self.instance_info = None

    def load_instance_info(self, instance_name):
        if self.instance_info:
            self.instance_info.pack_forget()
            self.instance_info.destroy()

        _instance_info = self.multipass_client.instance_info(instance_name)

        self.instance_info = VMInstanceInfo(self, _instance_info, self.multipass_client)
        self.instance_info.pack(anchor=tk.NW)


class ListVMInstance(tk.Frame):
    def __init__(self, master, instance, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._create_layout(instance)

        self.bind("<Button-1>", self._on_click)

    def _create_layout(self, instance):
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

    def _on_click(self, event):
        instance_name = event.widget.instance_name.cget('text')

        instance_info_frame = event.widget.master.master.master.master.children['!instanceinfoframe']

        instance_info_frame.load_instance_info(instance_name)


class VMInstanceInfo(tk.Frame):
    def __init__(self, master, instance_info, multipass_client, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.multipass_client = multipass_client
        self._create_layout(instance_info)

    def _create_layout(self, instance_info):
        self._create_buttons(instance_info)
        self._create_form(instance_info)

    def _create_buttons(self, instance_info):
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=1)

        instance_name = instance_info['name']

        if instance_info['status'] == 'STOPPED':
            start_btn = tk.Button(frame, text='Start', command=lambda:self.multipass_client.start_instance(instance_name))
            start_btn.pack(anchor=tk.W)
        elif instance_info['status'] == 'RUNNING':
            stop_btn = tk.Button(frame, text='Stop', command=lambda:self.multipass_client.stop_instance(instance_name))
            stop_btn.pack(anchor=tk.W)

    def _create_form(self, instance_info):
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=1)

        row = 0

        name_lbl = tk.Label(frame, text='Name')
        name_lbl.grid(row=row, column=0, ipadx="10", sticky=tk.E)

        self.name_var = tk.StringVar()

        name_field = tk.Entry(frame, textvariable=self.name_var, width=5)
        name_field.grid(row=row, column=1, ipadx="100", sticky=tk.W)

        row += 1

        release_lbl = tk.Label(frame, text='Release')
        release_lbl.grid(row=row, column=0, ipadx="10", sticky=tk.E)

        self.release_var = tk.StringVar()

        release_field = tk.Entry(frame, textvariable=self.release_var, width=5)
        release_field.grid(row=row, column=1, ipadx="100", sticky=tk.W)

        row += 1

        cpu_lbl = tk.Label(frame, text='CPU')
        cpu_lbl.grid(row=row, column=0, ipadx="10", sticky=tk.E)

        self.cpu_var = tk.StringVar()

        cpu_field = tk.Entry(frame, textvariable=self.cpu_var, width=5)
        cpu_field.grid(row=row, column=1, ipadx="100", sticky=tk.W)

        row += 1

        memory_lbl = tk.Label(frame, text='Memory')
        memory_lbl.grid(row=row, column=0, ipadx="10", sticky=tk.E)

        self.memory_var = tk.StringVar()

        memory_field = tk.Entry(frame, textvariable=self.memory_var, width=5)
        memory_field.grid(row=row, column=1, ipadx="100", sticky=tk.W)

        row += 1

        disk_lbl = tk.Label(frame, text='Disk')
        disk_lbl.grid(row=row, column=0, ipadx="10", sticky=tk.E)

        self.disk_var = tk.StringVar()

        disk_field = tk.Entry(frame, textvariable=self.disk_var, width=5)
        disk_field.grid(row=row, column=1, ipadx="100", sticky=tk.W)

        row += 1

        load_lbl = tk.Label(frame, text='Load')
        load_lbl.grid(row=row, column=0, ipadx="10", sticky=tk.E)

        self.load_var = tk.StringVar()

        load_field = tk.Entry(frame, textvariable=self.load_var, width=5)
        load_field.grid(row=row, column=1, ipadx="100", sticky=tk.W)
        load_field.configure(state=tk.DISABLED)

        row += 1

        mac_lbl = tk.Label(frame, text='Mac Addr')
        mac_lbl.grid(row=row, column=0, ipadx="10", sticky=tk.E)

        self.mac_var = tk.StringVar()

        mac_field = tk.Entry(frame, textvariable=self.mac_var, width=5)
        mac_field.grid(row=row, column=1, ipadx="100", sticky=tk.W)
        mac_field.configure(state=tk.DISABLED)

        row += 1

        ipv4_lbl = tk.Label(frame, text='IPV4')
        ipv4_lbl.grid(row=row, column=0, ipadx="10", sticky=tk.E)

        self.ipv4_var = tk.StringVar()

        ipv4_field = tk.Entry(frame, textvariable=self.ipv4_var, width=5)
        ipv4_field.grid(row=row, column=1, ipadx="100", sticky=tk.W)
        ipv4_field.configure(state=tk.DISABLED)

        row += 1

        ipv6_lbl = tk.Label(frame, text='IPV6')
        ipv6_lbl.grid(row=row, column=0, ipadx="10", sticky=tk.E)

        self.ipv6_var = tk.StringVar()

        ipv6_field = tk.Entry(frame, textvariable=self.ipv6_var, width=5)
        ipv6_field.grid(row=row, column=1, ipadx="100", sticky=tk.W)
        ipv6_field.configure(state=tk.DISABLED)

        if instance_info:
            self.name_var.set(instance_info['name'])
            self.release_var.set(instance_info['release'])
            self.cpu_var.set(instance_info['cpu'])
            self.load_var.set(instance_info['load'])
            self.memory_var.set(instance_info['memory'])
            self.disk_var.set(instance_info['disk'])
            self.mac_var.set(instance_info['mac_addr'])
            self.ipv4_var.set(instance_info['ipv4'])
            self.ipv6_var.set(instance_info['ipv6'])

            name_field.configure(state=tk.DISABLED)
            release_field.configure(state=tk.DISABLED)

            if instance_info['status'] == 'RUNNING':
                cpu_field.configure(state=tk.DISABLED)
                memory_field.configure(state=tk.DISABLED)
                disk_field.configure(state=tk.DISABLED)

            row += 1

            status_lbl = tk.Label(frame, text='Status')
            status_lbl.grid(row=row, column=0, ipadx="10", sticky=tk.E)

            self.status_var = tk.StringVar()
            self.status_var.set(instance_info['status'])

            status_field = tk.Entry(frame, textvariable=self.status_var, width=5)
            status_field.grid(row=row, column=1, ipadx="100", sticky=tk.W)
            status_field.configure(state=tk.DISABLED)

