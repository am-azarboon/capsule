from django.shortcuts import redirect


# LogoutRequired Mixin
class LogoutRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        """ Only unauthenticated users can access the view """
        if request.user.is_authenticated:
            return redirect("console:dashboard")

        return super().dispatch(request, *args, **kwargs)


# VerifyPreviousUrl Mixin
class VerifyPreviousUrlMixin:
    def dispatch(self, request, *args, **kwargs):
        """ Prevent user to access verify-email url manually """
        if "code" not in request.session or "user_id" not in request.session:
            return redirect("account:login")

        return super().dispatch(request, *args, **kwargs)
