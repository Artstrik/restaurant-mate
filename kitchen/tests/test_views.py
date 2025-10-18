from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from kitchen.models import DishType, Ingredient, Dish

User = get_user_model()


# ===== INGREDIENT TESTS =====
INGREDIENT_URL = reverse("kitchen:ingredient-list")


class PublicIngredientTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(INGREDIENT_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateIngredientTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client = Client()
        self.client.force_login(self.user)

    def test_retrieve_ingredients(self):
        Ingredient.objects.create(name="tomato")
        Ingredient.objects.create(name="cheese")
        response = self.client.get(INGREDIENT_URL)
        self.assertEqual(response.status_code, 200)
        ingredients = Ingredient.objects.all()
        self.assertEqual(
            list(response.context["ingredient_list"]),
            list(ingredients),
        )
        self.assertTemplateUsed(response, "kitchen/ingredient_list.html")

    def test_ingredient_ordering(self):
        Ingredient.objects.create(name="cheese")
        Ingredient.objects.create(name="tomato")
        response = self.client.get(INGREDIENT_URL)
        ingredients = list(response.context["ingredient_list"])
        self.assertEqual(ingredients[0].name, "cheese")
        self.assertEqual(ingredients[1].name, "tomato")

    def test_search_form_in_context(self):
        response = self.client.get(INGREDIENT_URL)
        self.assertIn("search_form", response.context)

    def test_pagination(self):
        for i in range(10):
            Ingredient.objects.create(name=f"ingredient{i}")
        response = self.client.get(INGREDIENT_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["ingredient_list"]), 5)

    def test_search_functionality(self):
        Ingredient.objects.create(name="tomato")
        Ingredient.objects.create(name="potato")
        response = self.client.get(INGREDIENT_URL + "?name=tomato")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["ingredient_list"]), 1)
        self.assertEqual(response.context["ingredient_list"][0].name, "tomato")


# ===== DISH TESTS =====
DISH_URL = reverse("kitchen:dish-list")


class PublicDishTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(DISH_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDishTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client = Client()
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(name="Main Course")

    def test_retrieve_dishes(self):
        Dish.objects.create(
            name="Pasta",
            description="Test pasta",
            price=15.00,
            dish_type=self.dish_type
        )
        Dish.objects.create(
            name="Pizza",
            description="Test pizza",
            price=20.00,
            dish_type=self.dish_type
        )
        response = self.client.get(DISH_URL)
        self.assertEqual(response.status_code, 200)
        dishes = Dish.objects.all()
        self.assertEqual(
            list(response.context["dish_list"]),
            list(dishes),
        )
        self.assertTemplateUsed(response, "kitchen/dish_list.html")

    def test_dish_ordering(self):
        Dish.objects.create(
            name="Pizza",
            description="Test pizza",
            price=20.00,
            dish_type=self.dish_type
        )
        Dish.objects.create(
            name="Pasta",
            description="Test pasta",
            price=15.00,
            dish_type=self.dish_type
        )
        response = self.client.get(DISH_URL)
        dishes = list(response.context["dish_list"])
        self.assertEqual(dishes[0].name, "Pasta")
        self.assertEqual(dishes[1].name, "Pizza")

    def test_search_form_in_context(self):
        response = self.client.get(DISH_URL)
        self.assertIn("search_form", response.context)

    def test_pagination(self):
        for i in range(10):
            Dish.objects.create(
                name=f"Dish {i}",
                description=f"Description {i}",
                price=10.00 + i,
                dish_type=self.dish_type
            )
        response = self.client.get(DISH_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["dish_list"]), 5)

    def test_search_functionality(self):
        Dish.objects.create(
            name="Pasta Carbonara",
            description="Creamy pasta",
            price=15.00,
            dish_type=self.dish_type
        )
        Dish.objects.create(
            name="Margherita Pizza",
            description="Classic pizza",
            price=18.00,
            dish_type=self.dish_type
        )
        response = self.client.get(DISH_URL + "?name=Pizza")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["dish_list"]), 1)
        self.assertEqual(response.context["dish_list"][0].name, "Margherita Pizza")


# ===== COOK TESTS =====
COOK_URL = reverse("kitchen:cook-list")


class PublicCookTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(COOK_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCookTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client = Client()
        self.client.force_login(self.user)

    def test_retrieve_cooks(self):
        User.objects.create_user(username="cook1", password="pass1")
        User.objects.create_user(username="cook2", password="pass2")
        response = self.client.get(COOK_URL)
        self.assertEqual(response.status_code, 200)
        cooks = User.objects.all()
        self.assertEqual(
            list(response.context["cook_list"]),
            list(cooks),
        )
        self.assertTemplateUsed(response, "kitchen/cook_list.html")

    def test_cook_ordering(self):
        User.objects.create_user(username="bcook", password="pass1")
        User.objects.create_user(username="acook", password="pass2")
        response = self.client.get(COOK_URL)
        cooks = list(response.context["cook_list"])
        self.assertEqual(cooks[0].username, "acook")
        self.assertEqual(cooks[1].username, "bcook")
        self.assertEqual(cooks[2].username, "testuser")

    def test_search_form_in_context(self):
        response = self.client.get(COOK_URL)
        self.assertIn("search_form", response.context)

    def test_pagination(self):
        for i in range(10):
            User.objects.create_user(username=f"cook{i}", password=f"pass{i}")
        response = self.client.get(COOK_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["cook_list"]), 5)

    def test_search_functionality(self):
        User.objects.create_user(username="chef_john", password="pass1")
        User.objects.create_user(username="baker_mary", password="pass2")
        response = self.client.get(COOK_URL + "?username=chef")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["cook_list"]), 1)
        self.assertEqual(response.context["cook_list"][0].username, "chef_john")


# ===== DISH DETAIL TESTS =====
class PublicDishDetailTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.dish_type = DishType.objects.create(name="Main Course")
        self.dish = Dish.objects.create(
            name="Test Dish",
            description="Test description",
            price=15.00,
            dish_type=self.dish_type
        )

    def test_login_required(self):
        response = self.client.get(reverse("kitchen:dish-detail", args=[self.dish.id]))
        self.assertNotEqual(response.status_code, 200)


class PrivateDishDetailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client = Client()
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(name="Main Course")
        self.dish = Dish.objects.create(
            name="Test Dish",
            description="Test description",
            price=15.00,
            dish_type=self.dish_type
        )

    def test_retrieve_dish_detail(self):
        response = self.client.get(reverse("kitchen:dish-detail", args=[self.dish.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["dish"], self.dish)
        self.assertTemplateUsed(response, "kitchen/dish_detail.html")


# ===== COOK DETAIL TESTS =====
class PublicCookDetailTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.cook = User.objects.create_user(
            username="testcook",
            password="test123",
        )

    def test_login_required(self):
        response = self.client.get(reverse("kitchen:cook-detail", args=[self.cook.id]))
        self.assertNotEqual(response.status_code, 200)


class PrivateCookDetailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client = Client()
        self.client.force_login(self.user)
        self.cook = User.objects.create_user(
            username="testcook",
            password="test123",
            years_of_experience=5
        )

    def test_retrieve_cook_detail(self):
        response = self.client.get(reverse("kitchen:cook-detail", args=[self.cook.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["cook"], self.cook)
        self.assertTemplateUsed(response, "kitchen/cook_detail.html")