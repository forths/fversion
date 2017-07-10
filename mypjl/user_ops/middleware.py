# coding=utf-8


class UrlPathMiddleware:
    # 处理请求前
    def process_request(self, request):
        # 如果当前请求的路径与用户登录、注册相关，则不需要记录
        if request.path not in ['/user/register/',
                                '/user/register_handle/',
                                '/user/register_valid/',
                                '/user/login/',
                                '/user/login_handle/',
                                '/user/logout/', ]:
            request.session['url_path'] = request.get_full_path()
            print request.session['url_path']
        print '执行了'
'''
http://www.itcast.cn/python?a=100
get_full_path():/python?a=100
path:/python
'''
