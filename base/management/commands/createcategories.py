from django.core.management.base import BaseCommand
from base.models import Category


class Command(BaseCommand):
  help = 'This command creating categories'

  def add_arguments(self, parser):
    parser.add_argument('--new', type=str, default=None, help='create new category over the default categorys')
  
  def handle(self, *args, **options):
    categories = ['smartphones', 'laptops', 'accessories' , 'cameras']
    for category in categories:
      getted, created = Category.objects.get_or_create(name=category)

      if getted:  
        self.stdout.write(self.style.WARNING(f'{category} Already Excist!'))
      if created:
        self.stdout.write(self.style.SUCCESS(f'{category} Created Successfully!'))

    new_category = options['new']

    if new_category != None:
      getted, created = Category.objects.get_or_create(name=new_category)
  
      if getted:  
        self.stdout.write(self.style.WARNING(f'{new_category} Already Excist!'))
      if created:
        self.stdout.write(self.style.SUCCESS(f'{new_category} Created Successfully!'))
