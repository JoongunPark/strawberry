from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'strawberry.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'strawberry.views.home', name='home'),
                       url(r'^reserve/', 'strawberry.views.reserve'),
                       url(r'^modify/', 'strawberry.views.modify'),
                       url(r'^print/', 'strawberry.views.printEx'),
                       url(r'^master/', 'strawberry.views.master'),

                       )
