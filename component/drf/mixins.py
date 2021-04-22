# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.response import Response


class ApiGenericMixin(object):
    """API视图类通用函数"""

    # permission_classes = ()

    def finalize_response(self, request, response, *args, **kwargs):
        """统一数据返回格式"""
        # 文件导出时response {HttpResponse}
        if not isinstance(response, Response):
            return response
        # 返回的数据格式
        response_data = {"result": True, "code": "OK", "message": "success", "data": []}
        # response.data 为list和tuple 或者 为字典但没有同时满足’code‘和’result‘
        if (
                response.data is None
                or (isinstance(response.data, (list, tuple)))
                or (isinstance(response.data, dict) and not ("code" in response.data and "result" in response.data))
        ):
            response_data["data"] = response.data
            response.data = response_data
        if response.status_code in [status.HTTP_201_CREATED, status.HTTP_204_NO_CONTENT]:
            response.status_code = status.HTTP_200_OK
        return super(ApiGenericMixin, self).finalize_response(request, response, *args, **kwargs)
