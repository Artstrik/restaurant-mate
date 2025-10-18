from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from kitchen.models import DishType, Ingredient, Dish


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
        )
        self.client.force_login(self.admin_user)
        self.cook = get_user_model().objects.create_user(
            username="cook",
            password="testcook",
            years_of_experience=10,
        )

        self.dish_type = DishType.objects.create(name="testdishtype")

        self.ingredient = Ingredient.objects.create(name="testingredient")

        self.dish = Dish.objects.create(
            name="testdish",
            description="testdescription",
            price=15,
            dish_type=self.dish_type,
        )

        self.dish.cooks.add(self.cook)
        self.dish.ingredients.add(self.ingredient)

    def test_cook_years_of_experience_listed(self):
        """
        Test that cook's years of experience listed is in list display on cook admin page.
        """
        url = reverse("admin:kitchen_cook_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.cook.years_of_experience)

    def test_cook_detail_years_of_experience_listed(self):
        """
        Test that cook's years of experience is on cook detail admin page
        """
        url = reverse("admin:kitchen_cook_change", args=[self.cook.id])
        res = self.client.get(url)
        self.assertContains(res, self.cook.years_of_experience)

    def test_cook_additional_info_fieldsets(self):
        """
        Test that additional info fieldsets with years_of_experience is present in cook admin.
        """
        url = reverse("admin:kitchen_cook_change", args=[self.cook.id])
        res = self.client.get(url)
        self.assertContains(res, "Additional info")
        self.assertContains(res, "years_of_experience")

    def test_cook_add_page_contains_experience_field(self):
        """
        Test that cook add page contains years_of_experience field in additional info.
        """
        url = reverse("admin:kitchen_cook_add")
        res = self.client.get(url)
        self.assertContains(res, "years_of_experience")

    def test_dish_display_cooks_method(self):
        """
        Test that custom display_cooks method works in dish admin list display.
        """
        url = reverse("admin:kitchen_dish_changelist")
        res = self.client.get(url)
        self.assertContains(
            res, self.cook.username
        )  # Проверяем, что имя повара отображается
        self.assertContains(res, "Cooks")  # Проверяем заголовок кастомного столбца

    def test_dish_search_by_name(self):
        """
        Test that dish admin page supports search by name.
        """
        url = reverse("admin:kitchen_dish_changelist") + "?q=" + self.dish.name
        res = self.client.get(url)
        self.assertContains(res, self.dish.name)

    def test_dish_filter_horizontal_widgets(self):
        """
        Test that dish admin uses filter_horizontal for cooks and ingredients.
        """
        url = reverse("admin:kitchen_dish_change", args=[self.dish.id])
        res = self.client.get(url)
        # Проверяем наличие filter_horizontal виджетов
        self.assertContains(res, "cooks")
        self.assertContains(res, "ingredients")

    def test_dish_type_search_by_name(self):
        """
        Test that dish type admin page supports search by name.
        """
        url = reverse("admin:kitchen_dishtype_changelist") + "?q=" + self.dish_type.name
        res = self.client.get(url)
        self.assertContains(res, self.dish_type.name)

    def test_ingredient_search_by_name(self):
        """
        Test that ingredient admin page supports search by name.
        """
        url = (
            reverse("admin:kitchen_ingredient_changelist")
            + "?q="
            + self.ingredient.name
        )
        res = self.client.get(url)
        self.assertContains(res, self.ingredient.name)

    def test_dish_list_display_contains_all_custom_fields(self):
        """
        Test that dish admin list_display contains all custom fields: name, price, dish_type, display_cooks.
        """
        url = reverse("admin:kitchen_dish_changelist")
        res = self.client.get(url)

        # Проверяем наличие всех кастомных полей в list_display
        self.assertContains(res, self.dish.name)
        self.assertContains(res, self.dish.price)
        self.assertContains(res, self.dish.dish_type.name)
        self.assertContains(res, self.cook.username)  # Из display_cooks метода

    def test_cook_list_display_contains_experience(self):
        """
        Test that cook admin list_display contains years_of_experience.
        """
        url = reverse("admin:kitchen_cook_changelist")
        res = self.client.get(url)
        self.assertContains(res, "years_of_experience")

    def test_dish_type_list_display_contains_name(self):
        """
        Test that dish type admin list_display contains name.
        """
        url = reverse("admin:kitchen_dishtype_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.dish_type.name)

    def test_ingredient_list_display_contains_name(self):
        """
        Test that ingredient admin list_display contains name.
        """
        url = reverse("admin:kitchen_ingredient_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.ingredient.name)
