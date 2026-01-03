from AppOpener import open, close

def open_app(*appName):
    appname=",".join(appName)
    open(appname, match_closest=True)

def close_app(*appName):
    appname=",".join(appName)
    close(appname, match_closest=True)