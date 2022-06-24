import tmux

def test():
    s = tmux.session('test')
    s.focused_window.focused_pane.run('vim tst')
    s.focused_window.new_pane(True)

# [[dir, [a, b, c]], [/home, [x, y]], [pwd, [z]]]
def open_files(session_name, files):
    s = tmux.session(session_name)
    for vim_session in files:
        s.focused_window.focused_pane.run('cd ' + vim_session[0])
        s.focused_window.focused_pane.run('vim')
        for file in vim_session[1]:
            # print(f'running :e {file}')
            s.focused_window.focused_pane.run(':e ' + file)
            s.focused_window.focused_pane.run(':vspl')
            # print(f'running :tabe')
            s.focused_window.focused_pane.run(':tabe')
        # print(f'running :q')
        s.focused_window.focused_pane.run(':q')
        s.focused_window.new_pane(True)
        s.focused_window.focused_pane.run('cd ' + vim_session[0])
        s.new_window().focus()
    s.focused_window.focused_pane.run('exit')
# s.focused_window.new_pane(True)

open_files('cashnetdrop', [['~/cashnet', ['nc.c']], ['~/ashdrop', ['ad.c', 'fs.h', 'kq.c']], ['~/libashnet', ['ashnetd.c']], ['~/stdash', ['ex.c']], ['~/persistent_map', ['ph.c']]])
