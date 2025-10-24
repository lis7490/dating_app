import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from users.models import User, UserPhoto
from interactions.models import UserView, Like, Match

class Command(BaseCommand):
    help = 'Генерация тестовых данных для dating приложения'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=50, help='Количество пользователей')
        parser.add_argument('--interactions', type=int, default=200, help='Количество взаимодействий')

    def handle(self, *args, **options):
        users_count = options['users']
        interactions_count = options['interactions']

        self.stdout.write('Создание пользователей...')
        
        # Создаем тестовых пользователей
        cities = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань']
        hobbies_list = [
            'Путешествия, музыка, спорт', 'Кино, книги, программирование', 
            'Фотография, искусство, танцы', 'Кулинария, вино, театр',
            'Спорт, автомобили, технологии', 'Йога, медитация, природа'
        ]
        
        users = []
        for i in range(users_count):
            gender = random.choice(['M', 'F'])
            first_name = f'Мужское_{i}' if gender == 'M' else f'Женское_{i}'
            last_name = f'Фамилия_{i}'
            
            user = User.objects.create_user(
                email=f'user_{i}@example.com',
                password='password123',
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                birth_date=timezone.now().date() - timedelta(days=random.randint(18*365, 40*365)),
                city=random.choice(cities),
                bio=f'Привет! Я {first_name}, ищу интересного собеседника.',
                hobbies=random.choice(hobbies_list),
                status=random.choice(['single', 'dating', 'complicated'])
            )
            users.append(user)
        
        self.stdout.write('Создание взаимодействий...')
        
        # Создаем просмотры и лайки
        for i in range(interactions_count):
            viewer = random.choice(users)
            viewed_user = random.choice([u for u in users if u != viewer])
            
            # Создаем просмотр
            UserView.objects.create(
                viewer=viewer,
                viewed_user=viewed_user,
                duration=random.randint(10, 300)
            )
            
            # С некоторой вероятностью создаем лайк
            if random.random() > 0.7:
                Like.objects.create(
                    from_user=viewer,
                    to_user=viewed_user,
                    like_type=random.choice(['like', 'dislike', 'superlike'])
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно создано: {users_count} пользователей, {interactions_count} взаимодействий'
            )
        )