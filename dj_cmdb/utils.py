from drf_yasg.generators import OpenAPISchemaGenerator


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    """重写 OpenAPISchemaGenerator 实现每个tag的说明文本"""

    def get_schema(self, request=None, public=False):
        swagger = super().get_schema(request, public)

        swagger.tags = [
            {
                "name": "cmdb",
                "description": "资源配置数据库",
            },
            {
                "name": "relation",
                "description": "配置项关系",
            },
        ]

        return swagger
