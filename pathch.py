import os

def pathch(path, default=None, force=False):
    """
    Patch a path. Determine if a provided filename is a path with no filename, 
    a path with a filename, a path with a filename with the wrong extension, 
    etc., and make necessary corrections.
    """
      
    if path is None:
        path = './'

    if default is None:
        # The user just wants to format a path properly.
        if os.path.isdir(path):
            if path[-1] != '/':
                path += '/'
            return path
        else:
            return path
            
    elif os.path.splitext(default)[1] == '': # Only extension in default arg
        # The user may specify any filename, but an extension is forced. Remove
        # any extensions provided by the user and replace with the default.

        if os.path.isdir(path):
            raise ValueError('A path and extension were provided, but with no filename.')

        path = os.path.splitext(path)[0]+default
        return path

    else: #Filename and extension in default arg
        if force is True:
            # Force default filename but preserve path.
            if os.path.isdir(path):
                path = os.path.dirname(path+'/')+'/'+os.path.basename(default)
            else:
                path = os.path.dirname(path)+'/'+os.path.basename(default)
            return path

        else:
            # User may overwrite a default filename if they wish, or provide a
            # path and the default filename will be used.
            if os.path.isdir(path):
                path = os.path.dirname(path+'/')+'/'+os.path.basename(default)
            elif os.path.splitext(path)[1] == '': # User provided no extension
                # Keep user's filename but add an extension
                path = path + os.path.splitext(default)[1]
            else: # User provided filename with extension
                # Force extension
                path = os.path.splitext(path)[0]+os.path.splitext(default)[1]
            return path
