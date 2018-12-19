from django.http import HttpResponseRedirect,HttpResponse
from django.utils.deprecation import MiddlewareMixin

class CheckPower(MiddlewareMixin):
    def process_view(self,request,view_func,view_args,view_kwargs):
        try:
            url_name=request.resolver_match.url_name
            spacename=request.resolver_match.namespace
            if spacename=='manage':
                str=spacename+':'+url_name
                if str in request.session['url_list']:
                    return HttpResponse('你没有权限')
                else:
                    pass
        except:
            pass
