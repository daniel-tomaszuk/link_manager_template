def is_logged(request):
    """
    Check if the user is logged.
    :param request: html
    :return: context
    """
    if request.user.is_authenticated:
        context = {
            "logged": True,
            "user": request.user.username
        }
    else:
        context = {
            "logged": False,
        }
    return context
