from flask import render_template
from . import main

@main.app_errorhandler(403)
def forbidden(e):
    return render_template('customError.html',errorCode="403",errorName="Not authorized!! Forbidden!",errorQuote="🤔 Looks like you have landed into wrong place!!⛔"), 403

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('customError.html',errorCode="404",errorName="Page Not Found",errorQuote="It looks like you found a glitch in the matrix... 😥",page404="active"), 500
    # return render_template('404.html',page404="active"), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('customError.html',errorCode="500",errorName="Internal Server Error",errorQuote="Lookslike We have issue on our side 😥"), 500
