from ckan.common import config
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


def nbviewer_host():
    '''Get nbviewer_host from the [app:main] section of your CKAN config file.'''
    host = config.get('ckan.nbview.nbviewer_host', 'http://localhost:8080');
    if (host.endswith('/')):
        host = host[:-1]
    
    return host


class NbviewPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IResourceView)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'nbview')

    def info(self):
        return {
            'name': 'nbview',
            'title': toolkit._('Notebook Preview'),
            'default_title': toolkit._('Preview'),
            'icon': 'book',
            'always_available': True,
            'iframed': False
        }

    def setup_template_variables(self, context, data_dict):
        from urlparse import urlparse
        url = data_dict['resource']['url']
        parts = urlparse(url)
        url = parts.netloc + parts.path
        return {
            'nbviewer_host': nbviewer_host(),
            'resource_url': url
        }

    def can_view(self, data_dict):
        supported_formats = ['ipynb']
        try:
            return data_dict['resource'].get('format', '').lower() in supported_formats
        except:
            return False

    def view_template(self, context, data_dict):
        return 'nbview/preview.html'

    def form_template(self, context, data_dict):
        return 'nbview/form.html'
