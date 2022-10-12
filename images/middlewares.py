from django.http import HttpResponseBadRequest


class AjaxMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        def is_ajax(self):
            return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

        request.is_ajax = is_ajax.__get__(request)
        response = self.get_response(request)
        return response


# def ajax_required(f):
#     def wrap(request, *args, **kwargs):
#         if not request.is_ajax():
#             return HttpResponseBadRequest()
#         return f(request, *args, **kwargs)
#     wrap.__doc__=f.__doc__
#     wrap.__name__=f.__name__
#     return wrap

