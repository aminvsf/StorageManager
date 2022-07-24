from settings.models import SiteSettings


def load_settings(request):
    return {'settings': SiteSettings.load()}
