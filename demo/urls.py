from django.urls import path
from rest_framework.routers import DefaultRouter

# ||router = DefaultRouter()
# ||#router.register(<prefix>, <viewset>, <basename>)
# ||
# ||urlpatterns = [
# ||   #path(<route>, <view>),
# ||]
# ||urlpatterns += router.urls
# ||
from django.urls import re_path

from . import views

urlpatterns = [
    path('articlesx/2003/', views.special_case_2003),
    # re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
    path('articles/<int:year>/', views.year_archive),
    # path('<year>/articles/', views.year_archive),
    # re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    # path('<year>--<month>/articles/', views.month_archive),
    path('<year>--<month>/articles:watch/', views.month_archive),
    path('<year>--<month>/articles:reboot/', views.month_archive),
    path('<year>--<month>/articles:sendmail/', views.month_archive),
    path('<year>--<month>/articles:clear/', views.month_archive),
    path('<year>--<month>/articles:batch/', views.month_archive),
    # re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$', views.article_detail),
]

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#router.register(r'nujnus_record', ReocrdViewSet, basename='nujnus_record')
router.register(r'files',  views.FileInfoSet, basename='FileInfoSet')
#router.register(r'FileInfoDateSet',  views.FileInfoDateSet, basename='FileInfoDateSet')
#router.register(r'FileInfoHasGroupSet',  views.FileInfoHasGroupSet, basename='FileInfoHasGroupSet')
router.register(r'groups', views.FileGroupSet , basename='FileGroup2Set')
router.register(r'search_jobs', views.GroupSearchResultSet , basename='GroupSearchResultSet')
# --------------------------------------------------------
urlpatterns = [
#    # post
#    path('files/', view.create_file_info),  # create_file_info
#    # patch
#    path('files/<file_id>/increase', view.update_file_info_edit_time, ),  # update_file_info_edit_time
#    # get
#    path('files/', view.filename_search),  # ?name_contains=123
#    # get
#    path('files/', view.file_date_search),  # ?date=2020-1-1
#    # get
#    path('files/', view.file_date_range_search),  # ?date_between=[2020-1-1, 2020-2-1]
#    # get
#    path('files/', view.file_tag_search),  # ?tag_contains=456
#    # get
#    path('files/', view.get_all_file),
#    # --------------------------------------------------------
#    # action:
#    # patch
#    path('files/<file_id>/partial', view.tag_file),
#    # patch
#    path('files/<file_id>/partial', view.description_file),
#    # get  #可以用自定义routes作为alias  #还是独立一个action
#    path('files/<file_id>/statistics_date', statistics_a_file_all_date, {"statistics_date": True}),
#    path('files/<file_id>/sum_edit', statistics_a_file_all_edit_time_orderby, {"sum_edit": True}),
#    # --------------------------------------------------------
#    # post
#    path('file_groups/', create_file_group),
#    # get
#    path('file_groups/', get_all_file_groups),
#
#    # --------------------------------------------------------
#    # post
#    path('search_jobs/', search_file_group),  # {"file_groups": "xxx"}
#    # get
#    path('search_jobs/', get_search_results),  # ?group=xxxx
#    # get
#    path('search_jobs/', get_search_results),
#    # get
#    path('search_jobs/<search_job_id>', get_search_results),
#    # get
#    path('search_jobs/search', search_in_all_search_results),  # ?search=xxxx
]
# --------------------------------------------------------

# urlpatterns = [
#    path('<page_slug>-<page_id>/', include([
#        path('history/', views.history),
#        path('edit/', views.edit),
#        path('discuss/', views.discuss),
#        path('permissions/', views.permissions),
#    ])),
# ]

urlpatterns += router.urls
