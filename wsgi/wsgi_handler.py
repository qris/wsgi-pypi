"""
WSGI config for  project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
from os import path
import sys
import site

vcs_root_dir = path.abspath(path.join(path.dirname(__file__), '..'))

# add deploy dir to path so we can import project_settings
sys.path.append(path.join(vcs_root_dir, 'deploy'))
from project_settings import relative_django_dir, relative_ve_dir

# ensure the virtualenv for this instance is added
python = 'python%d.%d' % (sys.version_info[0], sys.version_info[1])
site.addsitedir(
    path.join(vcs_root_dir, relative_ve_dir, 'lib', python, 'site-packages'))

sys.path.append(path.join(vcs_root_dir, relative_django_dir))

class Config(object):
	debug = True
	reload = False
	prefix = '/var/cache/pypicache'
args = Config()

import logging
loglevel = logging.DEBUG if args.debug else logging.INFO

logging.basicConfig(
    level=loglevel,
    format="%(asctime)s [%(levelname)s] [%(processName)s-%(threadName)s] [%(name)s] [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S%z"
)
logging.info("Debugging: {0!r}".format(args.debug))
logging.info("Reloading: {0!r}".format(args.reload))

from pypicache import cache, disk, pypi, server
pypi_server = pypi.PyPI()
package_store = disk.DiskPackageStore(args.prefix)
package_cache = cache.PackageCache(package_store, pypi_server)
application = server.configure_app(pypi_server, package_store, package_cache, debug=args.debug)
