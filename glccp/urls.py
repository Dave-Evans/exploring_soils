from django.urls import re_path, path
from glccp import views as glccp_views


urlpatterns = [
    re_path(
        r"^get_glccp_data$",
        glccp_views.get_glccp_data,
        name="get_glccp_data",
    ),
    re_path(r"^glccp/map$", glccp_views.glccp_map, name="glccp_map"),
]
