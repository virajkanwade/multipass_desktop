import os
import tkinter as tk

from _widgets import InstancesListFrame, InstanceInfoFrame
from multipass_grpc.client import MutlipassGRpcClient


class MultipassDesktop():
    def __init__(self):
        self._create_grpc_client()
        self._create_root()
        self._create_layout()

    def _create_root(self):
        self.root = tk.Tk()
        self.root.title('Multipass Desktop')
        self.root.geometry("1280x720")

    def _create_layout(self):
        self._create_window()
        self._create_instances_list_frame()
        self._create_instance_info_frame()

    def _create_window(self):
        self.window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=4)
        self.window.pack(fill=tk.BOTH, expand=1)

    def _create_instances_list_frame(self):
        self.instances_list_frame = InstancesListFrame(self.window, self.multipass_client)
        self.window.add(self.instances_list_frame)

    def _create_instance_info_frame(self):
        self.instance_info_frame = InstanceInfoFrame(self.window, self.multipass_client)
        self.window.add(self.instance_info_frame)

    def _create_grpc_client(self):
        ini_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        self.multipass_client = MutlipassGRpcClient(ini_path)

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    MultipassDesktop().run()
