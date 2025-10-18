from django.test import TestCase
from django.contrib.auth import get_user_model

from kitchen.forms import (
    CookCreationForm,
    CookExperienceUpdateForm,
    DishForm,
    CookSearchForm,
    DishSearchForm,
    DishTypeSearchForm,
    IngredientSearchForm,
)
from kitchen.models import DishType, Ingredient, Dish

User = get_user_model()


class CookCreationFormTests(TestCase):
    def test_form_has_correct_fields(self):
        form = CookCreationForm()
        expected_fields = {
            "username",
            "password1",
            "password2",
            "years_of_experience",
            "first_name",
            "last_name",
        }
        self.assertEqual(set(form.fields.keys()), expected_fields)

    def test_form_valid_data(self):
        form_data = {
            "username": "testchef",
            "password1": "testpass123",
            "password2": "testpass123",
            "first_name": "John",
            "last_name": "Doe",
            "years_of_experience": 5,
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_password_mismatch(self):
        form_data = {
            "username": "testchef",
            "password1": "testpass123",
            "password2": "differentpass",
            "first_name": "John",
            "last_name": "Doe",
            "years_of_experience": 5,
        }
        form = CookCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)


# ===== COOK EXPERIENCE UPDATE FORM TESTS =====
class CookExperienceUpdateFormTests(TestCase):
    def setUp(self):
        self.cook = User.objects.create_user(
            username="testcook", password="testpass123", years_of_experience=5
        )

    def test_form_has_correct_fields(self):
        form = CookExperienceUpdateForm()
        expected_fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
        ]
        self.assertEqual(list(form.fields.keys()), expected_fields)

    def test_form_valid_data(self):
        form_data = {
            "username": "testcook",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "years_of_experience": 10,
        }
        form = CookExperienceUpdateForm(data=form_data, instance=self.cook)
        self.assertTrue(form.is_valid())

    def test_form_invalid_negative_experience(self):
        form_data = {
            "username": "testcook",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "years_of_experience": -5,
        }
        form = CookExperienceUpdateForm(data=form_data, instance=self.cook)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)
        self.assertIn("cannot be negative", str(form.errors))

    def test_form_invalid_experience_exceeds_limit(self):
        form_data = {
            "username": "testcook",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "years_of_experience": 55,
        }
        form = CookExperienceUpdateForm(data=form_data, instance=self.cook)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)
        self.assertIn("cannot exceed 50", str(form.errors))


# ===== DISH FORM TESTS =====
class DishFormTests(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Main Course")
        self.ingredient1 = Ingredient.objects.create(name="Tomato")
        self.ingredient2 = Ingredient.objects.create(name="Cheese")
        self.cook1 = User.objects.create_user(username="cook1", password="pass")
        self.cook2 = User.objects.create_user(username="cook2", password="pass")

    def test_form_has_correct_fields(self):
        form = DishForm()
        expected_fields = [
            "name",
            "description",
            "price",
            "dish_type",
            "cooks",
            "ingredients",
        ]
        self.assertEqual(list(form.fields.keys()), expected_fields)

    def test_form_widgets(self):
        form = DishForm()
        self.assertEqual(
            form.fields["cooks"].widget.__class__.__name__, "CheckboxSelectMultiple"
        )
        self.assertEqual(
            form.fields["ingredients"].widget.__class__.__name__,
            "CheckboxSelectMultiple",
        )

    def test_form_required_fields(self):
        form = DishForm()
        self.assertFalse(form.fields["cooks"].required)
        self.assertFalse(form.fields["ingredients"].required)

    def test_form_valid_data(self):
        form_data = {
            "name": "Test Dish",
            "description": "Test description",
            "price": 15.50,
            "dish_type": self.dish_type.id,
            "cooks": [self.cook1.id],
            "ingredients": [self.ingredient1.id, self.ingredient2.id],
        }
        form = DishForm(data=form_data)
        self.assertTrue(form.is_valid())


# ===== SEARCH FORMS TESTS =====
class CookSearchFormTests(TestCase):
    def test_form_has_correct_field(self):
        form = CookSearchForm()
        self.assertIn("username", form.fields)

    def test_form_field_attributes(self):
        form = CookSearchForm()
        field = form.fields["username"]
        self.assertFalse(field.required)
        self.assertEqual(field.label, "")
        self.assertEqual(field.widget.attrs["placeholder"], "Search by username")

    def test_form_valid_data(self):
        form_data = {"username": "test"}
        form = CookSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_empty_data(self):
        form_data = {}
        form = CookSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class DishSearchFormTests(TestCase):
    def test_form_has_correct_field(self):
        form = DishSearchForm()
        self.assertIn("name", form.fields)

    def test_form_field_attributes(self):
        form = DishSearchForm()
        field = form.fields["name"]
        self.assertFalse(field.required)
        self.assertEqual(field.label, "")
        self.assertEqual(field.widget.attrs["placeholder"], "Search by dish name")

    def test_form_valid_data(self):
        form_data = {"name": "pasta"}
        form = DishSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class DishTypeSearchFormTests(TestCase):
    def test_form_has_correct_field(self):
        form = DishTypeSearchForm()
        self.assertIn("name", form.fields)

    def test_form_field_attributes(self):
        form = DishTypeSearchForm()
        field = form.fields["name"]
        self.assertFalse(field.required)
        self.assertEqual(field.label, "")
        self.assertEqual(field.widget.attrs["placeholder"], "Search by dish type")

    def test_form_valid_data(self):
        form_data = {"name": "main"}
        form = DishTypeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class IngredientSearchFormTests(TestCase):
    def test_form_has_correct_field(self):
        form = IngredientSearchForm()
        self.assertIn("name", form.fields)

    def test_form_field_attributes(self):
        form = IngredientSearchForm()
        field = form.fields["name"]
        self.assertFalse(field.required)
        self.assertEqual(field.label, "")
        self.assertEqual(field.widget.attrs["placeholder"], "Search by ingredient")

    def test_form_valid_data(self):
        form_data = {"name": "tomato"}
        form = IngredientSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
