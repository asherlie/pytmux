import os
import importlib
import time
import tmux

def reload():
    importlib.reload(tmux)
    s = session('finder')
    np = s.focused_window.new_pane(True)
    # np.focus()
    np.up.focus()
    # print(f'left: {np.left}, right: {np.right}, up: {np.up}, down: {np.down}')

class pane:
    navigation = []
    left = None
    right = None
    up = None
    down = None
    running = None
    # creates a new pane, splitting the focused pane of the parent window
    def __init__(self, idx, parent_window, vertical, exists=False):
        self.parent_window = parent_window
        if not exists:
            if vertical:
                # parent_window.focused_pane.right = self
                # self.left = parent_window.focused_pane

                parent_window.focused_pane.down = self
                self.up = parent_window.focused_pane
                # print(f'self.left = {parent_window.focused_pane}')
                self.split_vert()
                # we're put on the left
                # we must go to the left one to get to prev
            else:
                parent_window.focused_pane.right = self
                self.left = parent_window.focused_pane
                # print(f'self.up= {parent_window.focused_pane}')
                self.split_hori()
            parent_window.panes.append(self)
            parent_window.focused_pane = self
        self.idx = idx

    # not meant to be called by user
    def split_vert(self):
        self.parent_window.focus()
        os.popen('tmux split -t ' + self.parent_window.parent_session.name + ' -v')

    def split_hori(self):
        self.parent_window.focus()
        os.popen('tmux split -t ' + self.parent_window.parent_session.name + ' -h')

    def run(self, cmd):
        self.running = cmd
        self.parent_window.parent_session.send_keys(cmd)

    def move_direction(self, d):
        os.popen('tmux select-pane -' + d.upper())

    def focus(self):
        def find_path(pane, path):
            if not pane: return
            if(pane == self):
                return path
            tmp = find_path(pane.left, path+['l'])
            if tmp: return tmp
            tmp = find_path(pane.right, path+['r'])
            if tmp: return tmp
            tmp = find_path(pane.up, path+['u'])
            if tmp: return tmp
            tmp = find_path(pane.down, path+['d'])
            if tmp: return tmp

        # self.parent_window.focused_pane
        # go through all panes in all windows, 
        for i in find_path(self.parent_window.focused_pane, []):
            print('moving to dir ' + str(i))
            self.move_direction(i)
        # print('path: ' + str(ret))
        # for win in self.parent_window.parent_session.windows:
            # for p in win.panes:
                # print(p)
        # self.parent_window.
        # self.parent_window.focused_pane = self

        

class window:
    pane_idx = 0
    def __init__(self, idx, parent_session, exists=False):
        self.parent_session = parent_session
        self.idx = idx
        if not exists: os.popen('tmux new-window -t ' + parent_session.name + ' -t ' + str(idx))
        self.panes = [pane(self.pane_idx, self, False, True)]
        self.focused_pane = self.panes[0]
        # self, up, down, left, right
        self.pane_navigation = ['s']
        self.pane_idx += 1
        # parent_session.send_keys('C-b :new-window -t ' + str(self.idx))

    def focus(self):
        os.popen('tmux select-window -t ' + self.parent_session.name + ':' + str(self.idx))
        self.parent_session.focused_window = self
        # parent_session.send_keys('C-b ' + str(self.idx))
    
    # creates a new pane that's split off of the currently focused pane
    def new_pane(self, vertical):
        p = pane(self.pane_idx, self, vertical, False)
        self.pane_idx += 1
        return p


#TODO: wait for popen instead of sleep
class session:
    window_idx = 1
    def __init__(self, name):
        self.name = name
        os.popen('tmux new-session -s ' + name + ' -n 0 -d')
        time.sleep(.1)
        self.windows = [window(0, self, True)]
        self.focused_window = self.windows[0]

    def send_keys(self, keys):
        os.popen('tmux send-keys -t ' + self.name + ' "' + keys + '" C-m')
        time.sleep(.1)
    
    def new_window(self):
        self.windows.append(window(self.window_idx, self))
        self.window_idx += 1
        return self.windows[self.window_idx-1]
