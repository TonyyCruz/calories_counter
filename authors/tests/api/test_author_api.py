# import json

from parameterized import parameterized

from .author_api_test_base import AuthorApiTestBase

# from unittest.mock import patch


# flake8:noqa
class AuthorAPIv2Test(AuthorApiTestBase):
    def test_author_api_anonymous_user_cannot_get_any_user_data(self):
        response = self.get_author_response()
        self.assertAlmostEqual(response.status_code, 401)

    def test_author_api_logged_user_cannot_get_data_of_another_user(self):
        # cria o primeiro usuario (id = 1)
        user_auth = self.get_author_and_token()
        # pega o token do user
        user_token = user_auth.get("access", "")

        # cria o segundo usuario (id = 2)
        another_user = self.get_author_and_token(
            username="usr",
            password="Myp4s.s3",
        ).get("author")

        # tenta acessar as informacoes do another_user com o token do user
        response = self.get_author_response(
            token=user_token, id=another_user.id
        )
        self.assertAlmostEqual(response.status_code, 404)

    def test_author_api_authenticated_user_can_get_own_data(self):
        user_auth = self.get_author_and_token()
        user = user_auth.get("author", "")
        user_token = user_auth.get("access", "")

        response = self.get_author_response(token=user_token, id=user.id)
        self.assertAlmostEqual(response.status_code, 200)

    def test_author_api_me_route_get_data_from_authenticated_user(self):
        user_auth = self.get_author_and_token()
        user = user_auth.get("author", "")
        user_token = user_auth.get("access", "")

        response = self.get_author_response(token=user_token, id="me")
        self.assertAlmostEqual(response.status_code, 200)
        self.assertAlmostEqual(response.data.get("username"), user.username)

    def test_author_api_is_possible_register_an_user_with_correct_data(self):
        data = self.mock_author_dict
        response = self.post_author_response(data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("username"), data.get("username"))

    @parameterized.expand(
        [
            ("first_name", "a", "First name must have at least 2 characters."),
            ("first_name", " ", "First name must not be empty."),
            ("last_name", " ", "Last name must not be empty."),
            ("username", "abc", "Username must have at least 4 characters."),
            ("email", " ", "E-mail must not be empty."),
            ("email", "test@email.com", "This email is already in use."),
            (
                "password",
                "Abcde9*",
                "Password must have at least 8 characters.",
            ),
            (
                "password",
                "abcdef8.",
                "Password must have at least one uppercase letter.",
            ),
            (
                "password",
                "Abcdefgh9",
                "Password must have at least one special character.",
            ),
            (
                "password",
                "ABCDEF9%",
                "Password must have at least one lowercase letter.",
            ),
            (
                "password",
                "aBCDEFG#",
                "Password must have at least one number.",
            ),
        ]
    )
    def test_author_api_raise_an_expected_error_if_created_with_invalid_field_data(
        self, field, value, expect_error
    ):
        # cria um usuario com o email que sera usado no teste de email unico
        self.make_author(email="test@email.com")

        data = self.mock_author_dict
        data[field] = value

        jwt_access_token = self.get_author_and_token().get("access", "")
        response = self.post_author_response(data=data, token=jwt_access_token)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get(field)[0], expect_error)

    @parameterized.expand(
        [
            ("first_name", "MyName"),
            ("last_name", "MyLast"),
            ("username", "MyUserName"),
            ("email", "myemail@email.com"),
        ]
    )
    def test_author_api_is_possible_update_an_authenticated_user_data(
        self, field, new_value
    ):
        # dados para criação de um autor
        data = self.mock_author_dict
        # cria um autor com os dados mockados
        author = self.make_author(**data)
        token = self.get_token(**data).get("access", "")

        # campo a ser alterado
        new_data = {field: new_value}
        updated_author = self.patch_author_response(
            data=new_data,
            token=token,
            id=author.id,
        )

        self.assertEqual(updated_author.status_code, 200)
        self.assertEqual(updated_author.data.get(field), new_value)

    def test_author_api_user_can_delete_himself(self):
        # dados para criação de um autor
        data = self.mock_author_dict

        # cria um autor com os dados mockados
        author_data = self.get_author_and_token(**data)
        token = author_data.get("access", "")
        author = author_data.get("author", "")

        delete_response = self.delete_author_response(
            id=author.id, token=token
        )

        try_auth = self.get_token(**data)

        self.assertEqual(delete_response.status_code, 204)
        self.assertEqual(
            try_auth.get("detail"),
            "No active account found with the given credentials",
        )
