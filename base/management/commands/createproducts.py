from django.core.management.base import BaseCommand
from base.factories import ProductFactory
from base.models import Product


class Command(BaseCommand):
  help = 'This command creating fake products data using FactoryBoy and Faker'

  def add_arguments(self, parser):
    parser.add_argument('times', type=int, default=1, help='Number of products to create')
  
  def handle(self, *args, **options):

    self.stdout.write('creating...')
    times = options['times']
    self.stdout.write(self.style.WARNING(f'current products count {Product.objects.count()} '))
    done = ProductFactory.create_batch(times)  
    if done:
      self.stdout.write(self.style.SUCCESS(f'{times} Products created successfully! '))
      self.stdout.write(self.style.WARNING(f'current products count {Product.objects.count()} '))
    else:
      self.stdout.write(self.style.ERROR('Something Went Wrong!'))
