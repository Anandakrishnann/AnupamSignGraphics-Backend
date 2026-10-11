from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import SiteSettings, Location, Service, Blog


class Command(BaseCommand):
    help = 'Seed default site content and create admin user'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@anupam.local', 'anupam@vaikom')
            self.stdout.write(self.style.SUCCESS('Created admin / anupam@vaikom'))
        else:
            user = User.objects.get(username='admin')
            user.set_password('anupam@vaikom')
            user.save()
            self.stdout.write(self.style.SUCCESS('Updated admin password to anupam@vaikom'))

        settings = SiteSettings.get_solo()
        settings.business_name = 'Anupam Signgraphics'
        settings.tagline = 'With the latest and most modern machinery'
        settings.about_text = (
            'Anupam Flex Printing and Wedding Cards, operating as Anupam Signgraphics, '
            'is a full-service print and signage studio based in Vaikom, Kottayam, Kerala. '
            'We specialise in advertising flex printing, flex boards, invitation and wedding '
            'card design, and screen printing - backed by modern machinery for UV flatbed '
            'printing, CNC routing, aluminium channel bending, high-speed digital printing, '
            '3D LED letter making, laser cutting, and label scoring.\n\n'
            'From shop boards and LED channel letters to wedding invitations that feel personal, '
            'our team designs and produces work that stands out on the street and on the table. '
            'We also serve clients from Cherthala and Thalayolaparambu, with clear maps and '
            'direct WhatsApp support so you can reach us quickly.'
        )
        settings.phone_1 = '9447869398'
        settings.phone_2 = '7025858611'
        settings.phone_3 = '8129411991'
        settings.whatsapp = '9447869398'
        settings.address = 'Vaikom, Kottayam, Kerala'
        settings.save()

        locations = [
            {
                'name': 'Vaikom',
                'maps_url': 'https://maps.app.goo.gl/CTn7n6QYj3KqAWTDA',
                'address': 'Vaikom, Kottayam, Kerala',
                'is_primary': True,
                'order': 0,
            },
            {
                'name': 'Cherthala',
                'maps_url': 'https://maps.app.goo.gl/hknxeseMuAdBvTgo7',
                'address': 'Cherthala, Alappuzha, Kerala',
                'is_primary': False,
                'order': 1,
            },
            {
                'name': 'Thalayolaparambu',
                'maps_url': 'https://maps.app.goo.gl/1hVDzf4jwA4JXGr89',
                'address': 'Thalayolaparambu, Kottayam, Kerala',
                'is_primary': False,
                'order': 2,
            },
        ]
        for loc in locations:
            Location.objects.update_or_create(name=loc['name'], defaults=loc)

        services = [
            ('UV Flatbed Printing', 'Large-format UV printing on rigid and specialty surfaces.'),
            ('CNC Router', 'Precise cutting and shaping for boards, acrylic, and wood.'),
            ('Aluminium Channel Bending', 'Clean channel letter profiles for illuminated signage.'),
            ('High-Speed Digital Printing', 'Fast turnaround for flex, posters, and promotional print.'),
            ('3D LED Letter Making', 'Dimensional letters with LED lighting for shopfronts.'),
            ('Laser Cutting', 'Fine detail cutting for acrylic, MDF, and decorative panels.'),
            ('Label Scoring', 'Accurate scoring and finishing for labels and packaging.'),
            ('Flex Boards & Advertising', 'Outdoor flex, hoardings, and advertising displays.'),
            ('Wedding & Invitation Cards', 'Custom invitation design and print for weddings and events.'),
            ('Screen Printing', 'Durable screen print for textiles, boards, and promotional items.'),
        ]
        for i, (title, desc) in enumerate(services):
            Service.objects.update_or_create(
                title=title,
                defaults={'description': desc, 'order': i, 'is_active': True},
            )

        if not Blog.objects.exists():
            Blog.objects.create(
                title='Why modern machinery matters for your signboard',
                excerpt='Cleaner edges, richer colour, and faster delivery - what our UV, CNC, and LED setup means for your next board.',
                content=(
                    'A good signboard is more than vinyl on a frame. With UV flatbed printing, '
                    'colours stay sharp on acrylic and foam board. CNC routing and laser cutting '
                    'give letters and panels crisp edges. Aluminium channel bending and 3D LED '
                    'letter making turn shopfronts into night-time landmarks.\n\n'
                    'At Anupam Signgraphics in Vaikom, we pair design and production under one roof - '
                    'so your flex board, LED letters, or wedding invitations move from sketch to finish '
                    'without handoffs. Visit us in Vaikom, or reach out if you are in Cherthala or '
                    'Thalayolaparambu. Call or WhatsApp and we will help you choose the right finish.'
                ),
                is_published=True,
            )
            Blog.objects.create(
                title='Wedding cards that feel like the day itself',
                excerpt='From first draft to printed invite - how we design invitation cards that match your celebration.',
                content=(
                    'Invitation cards set the tone before guests arrive. We design and print wedding '
                    'and event cards with care - typography, paper feel, and colour that match your '
                    'ceremony. Whether you need a classic Malayalam-English layout or a modern minimal '
                    'invite, our digital and screen printing options cover small runs and larger sets.\n\n'
                    'Bring a reference or start from scratch. We will draft, revise, and print so your '
                    'cards arrive ready to send.'
                ),
                is_published=True,
            )

        self.stdout.write(self.style.SUCCESS('Seed data ready.'))
