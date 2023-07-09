from unittest.mock import patch

from .recipe_api_test_base import RecipeApiTestBase


# flake8: noqa
class RecipeAPIv2Test(RecipeApiTestBase):
    def test_recipe_api_list_returns_status_code_200(self):
        self.assertAlmostEqual(
            self.get_recipe_list_response().status_code, 200
        )

    @patch("recipes.views.api.RecipeAPIv2Pagination.page_size", new=3)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        total_number_of_recipes = 7
        max_number_of_recipes_per_Page = 3
        wanted_recipes_in_third_page = 1

        self.make_multiples_recipes(quantity=total_number_of_recipes)

        qty_of_loaded_recipes_first_page = len(
            self.get_recipe_list_response().data.get("results")
        )
        qty_of_loaded_recipes_second_page = len(
            self.get_recipe_list_response(page=2).data.get("results")
        )
        qty_of_loaded_recipes_third_page = len(
            self.get_recipe_list_response(page=3).data.get("results")
        )

        self.assertEqual(
            max_number_of_recipes_per_Page,
            qty_of_loaded_recipes_first_page,
        )
        self.assertEqual(
            max_number_of_recipes_per_Page,
            qty_of_loaded_recipes_second_page,
        )
        self.assertEqual(
            wanted_recipes_in_third_page,
            qty_of_loaded_recipes_third_page,
        )

    def test_recipe_api_list_do_not_show_not_published_recipes(self):
        expected_recipes_found = 2

        # Make 3 not published recipes
        self.make_multiples_recipes(
            is_published=False,
            title="Not published",
            quantity=3,
            stack_name="Not published",
        )

        # Make 2 published recipes
        self.make_multiples_recipes(
            is_published=True,
            title="Published",
            quantity=2,
            stack_name="Published",
        )

        self.assertEqual(
            self.get_recipe_list_response().data["count"],
            expected_recipes_found,
        )

    def test_recipe_api_list_can_loads_recipes_by_category_id(self):
        category_1 = self.make_category(name="category 1")
        category_2 = self.make_category(name="category 2")

        self.make_multiples_recipes(
            stack_name="category 1",
            quantity=2,
            category=category_1,
        )
        self.make_multiples_recipes(
            stack_name="category 2",
            quantity=3,
            category=category_2,
        )

        response_category_1 = self.get_recipe_list_response(
            url_query=f"category_id={category_1.id}"
        )
        response_category_2 = self.get_recipe_list_response(
            url_query=f"category_id={category_2.id}"
        )

        self.assertEqual(response_category_1.data["count"], 2)
        self.assertEqual(response_category_2.data["count"], 3)

    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        response = self.client.post(self.recipe_api_list_url)

        self.assertEqual(response.status_code, 401)

    def test_jwt_login(self):
        jwt_access_token = self.get_jwt_token().get("access", "")

        jwt_login = self.client.post(
            self.recipe_api_token_verify,
            {"token": jwt_access_token},
        )
        self.assertEqual(jwt_login.status_code, 200)
