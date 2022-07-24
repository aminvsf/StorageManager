from django.test import TestCase

from .models import SiteSettings, BackgroundImage


class SiteSettingsTests(TestCase):
    def setUp(self) -> None:
        self.settings = SiteSettings.objects.create(
            title='title',
            site_url='site url',
            short_des='short_des',
            email='email',
            about_us='about_us',
            copy_right='copy_right',
            logo_image='logo-image.svg',
            fav_icon='fav-icon.fav',
        )
        self.background_image = BackgroundImage.objects.create(
            settings=self.settings,
            image='image.jpeg'
        )

    def test_settings_listing(self):
        self.assertEqual(self.settings.title, 'title')
        self.assertEqual(self.settings.site_url, 'site url')
        self.assertEqual(self.settings.short_des, 'short_des')
        self.assertEqual(self.settings.email, 'email')
        self.assertEqual(self.settings.about_us, 'about_us')
        self.assertEqual(self.settings.copy_right, 'copy_right')
        self.assertEqual(self.settings.logo_image, 'logo-image.svg')
        self.assertEqual(self.settings.fav_icon, 'fav-icon.fav')
        self.assertEqual(len(self.settings.backgroundimage_set.all()), 1)
        self.assertEqual(self.settings.backgroundimage_set.first().image, 'image.jpeg')
        self.assertEqual(self.background_image.image, 'image.jpeg')
