import sys, os

def _make_writeable(filename):
    """ 
    Make sure that the file is writeable. Useful if our source is
    read-only.
    """
    if sys.platform.startswith('java'):
        # On Jython there is no os.access()
        return
    if not os.access(filename, os.W_OK):
        st = os.stat(filename)
        new_permissions = stat.S_IMODE(st.st_mode) | stat.S_IWUSR
        os.chmod(filename, new_permissions)

