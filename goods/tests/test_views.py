from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from goods.models import Product, Category, Review, FavoriteProduct

User = get_user_model()


class CatalogViewTest(TestCase):

    def test_catalog_view_with_products(self):
        category = Category.objects.create(
            name="Test",
            slug="test"
        )
        Product.objects.create(
            name="Product 1", description="Description 1", category=category
        )
        Product.objects.create(
            name="Product 2", description="Description 2", category=category
        )

        response = self.client.get(reverse("catalog:index", args=[category.slug]))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Product 1")
        self.assertContains(response, "Product 2")

        self.assertTemplateUsed(response, "goods/catalog.html")

    def test_catalog_view_without_products(self):
        category = Category.objects.create(
            name="Test",
            slug="test"
        )

        response = self.client.get(reverse("catalog:index", args=[category.slug]))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "No products available", count=0)

        self.assertTemplateUsed(response, "goods/catalog.html")


class ProductViewTest(TestCase):

    def test_product_view_with_valid_product(self):
        category = Category.objects.create(name="Test", slug="test")

        product = Product.objects.create(
            name="Test Product", description="Test Description", category=category
        )

        response = self.client.get(reverse("catalog:product", args=[product.slug]))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Test Product")
        self.assertContains(response, "Test Description")

        self.assertTemplateUsed(response, "goods/product.html")

    def test_product_view_with_invalid_product(self):

        response = self.client.get(reverse("catalog:product", args=["invalid-slug"]))

        self.assertEqual(response.status_code, 404)


class CategoryCreateViewTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@user.com",
            password="adminpass"
        )
        self.admin_user.is_staff = True
        self.admin_user.save()

        self.client.force_login(self.admin_user)

    def test_category_create_view_with_valid_data(self):
        response_get = self.client.get(reverse("catalog:create_category"))
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "goods/category_create.html")

        form_data = {
            "name": "Test Category",
            "slug": "test-category"
        }

        response = self.client.post(reverse("catalog:create_category"), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("main:index"))

        created_category = Category.objects.get(name="Test Category")

        self.assertEqual(created_category.slug, "test-category")

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Category successfully created")

    def test_category_create_view_with_invalid_data(self):
        form_data = {
            "name": "",
            "slug": "test-category"
        }
        response = self.client.post(reverse("catalog:create_category"), data=form_data)

        self.assertEqual(response.status_code, 200)

    def test_category_create_view_without_admin_permission(self):
        self.client.logout()
        user = User.objects.create_user(
            username="regular_user",
            email="regular@user.com",
            password="userpass")
        self.client.force_login(user)

        response = self.client.post(reverse("catalog:create_category"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("main:index"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You do not have permission to create categories.")


class ProductCreateViewTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@user.com",
            password="adminpass"
        )
        self.admin_user.is_staff = True
        self.admin_user.save()
        self.client.force_login(self.admin_user)
        self.category = Category.objects.create(name="Test", slug="test")

    def test_product_create_view_with_admin_permission(self):
        response_get = self.client.get(reverse("catalog:create_product"))
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "goods/product_create.html")

        form_data = {
            "name": "Test Product",
            "description": "Test Description",
            "price": 50.25,
            "discount": 5.0,
            "quantity": 1,
            "category": self.category.id
        }

        response_post_valid = self.client.post(
            reverse("catalog:create_product"), data=form_data
        )

        self.assertEqual(response_post_valid.status_code, 302)
        self.assertRedirects(response_post_valid, reverse("main:index"))

        messages = list(get_messages(response_post_valid.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Product successfully created")

        created_product = Product.objects.get(name="Test Product")
        self.assertIsNotNone(created_product)

    def test_product_create_view_without_admin_permission(self):
        self.client.logout()
        user = User.objects.create_user(
            username="regular_user",
            email="regular@user.com",
            password="userpass")
        self.client.force_login(user)

        response = self.client.get(reverse("catalog:create_product"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You do not have permission to create products.")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("main:index"))


class ProductUpdateViewTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@user.com",
            password="adminpass"
        )
        self.admin_user.is_staff = True
        self.admin_user.save()
        self.client.force_login(self.admin_user)

        self.category = Category.objects.create(name="Test", slug="test")

        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=50.25,
            discount=2.0,
            quantity=2,
            category=self.category
        )

    def test_product_update_view_with_admin_permission(self):
        response_get = self.client.get(
            reverse("catalog:product_update", args=[self.product.slug])
        )
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "goods/product_update.html")

        form_data = {
            "name": "Updated Product",
            "description": "Updated Description",
            "price": 75.50,
            "discount": 5.0,
            "quantity": 1,
            "category": self.category.id
        }

        response_post_valid = self.client.post(
            reverse("catalog:product_update", args=[self.product.slug]), data=form_data
        )

        self.assertEqual(response_post_valid.status_code, 302)
        self.assertRedirects(response_post_valid, self.product.get_absolute_url())

        self.product.refresh_from_db()

        messages = list(get_messages(response_post_valid.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Product successfully updated")

        self.assertEqual(self.product.name, "Updated Product")
        self.assertEqual(self.product.description, "Updated Description")
        self.assertEqual(self.product.price, 75.50)

    def test_product_update_view_without_admin_permission(self):
        self.client.logout()
        user = User.objects.create_user(
            username="regular_user",
            email="regular@user.com",
            password="userpass")
        self.client.force_login(user)

        response_get = self.client.get(
            reverse("catalog:product_update", args=[self.product.slug])
        )

        self.assertEqual(response_get.status_code, 302)
        self.assertRedirects(response_get, self.product.get_absolute_url())

        messages = list(get_messages(response_get.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You do not have permission to update products.")


class ProductDeleteViewTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@user.com",
            password="adminpass"
        )
        self.admin_user.is_staff = True
        self.admin_user.save()
        self.client.force_login(self.admin_user)

        self.category = Category.objects.create(name="Test", slug="test")

        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=50.25,
            discount=2.0,
            quantity=2,
            category=self.category
        )

    def test_product_delete_view_with_admin_permission(self):
        response_get = self.client.get(
            reverse("catalog:product_delete", args=[self.product.slug])
        )
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "goods/product_confirm_delete.html")

        response_post = self.client.post(
            reverse("catalog:product_delete", args=[self.product.slug])
        )

        self.assertRedirects(response_post, reverse("main:index"))
        messages = list(get_messages(response_post.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Product successfully removed")

        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=self.product.id)

    def test_product_delete_view_without_admin_permission(self):
        self.client.logout()
        user = User.objects.create_user(
            username="regular_user",
            email="regular@user.com",
            password="userpass")
        self.client.force_login(user)

        response_get = self.client.get(
            reverse("catalog:product_delete", args=[self.product.slug])
        )

        self.assertEqual(response_get.status_code, 302)

        self.assertRedirects(response_get, self.product.get_absolute_url())

        messages = list(get_messages(response_get.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You do not have permission to remove products.")


class ReviewCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            image_user="uploads/default.jpg"
        )
        self.client.force_login(self.user)

        self.category = Category.objects.create(name="Test Category", slug="test-category")

        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=50.25,
            discount=2.0,
            quantity=2,
            category=self.category
        )

    def test_create_review_view_with_valid_data(self):
        form_data = {
            "text": "Test review text",
            "product": self.product.id,
            "user": self.user.id,
        }

        response = self.client.post(
            reverse("catalog:review-create", args=[self.product.id]), data=form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.product.get_absolute_url())

        created_review = Review.objects.get(text="Test review text")

        self.assertEqual(created_review.product, self.product)
        self.assertEqual(created_review.user, self.user)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Review successfully added.")

    def test_create_review_view_with_invalid_data(self):
        form_data = {
            "text": "",
            "product": self.product.id,
            "user": self.user.id,
        }

        response = self.client.post(
            reverse("catalog:review-create", args=[self.product.id]), data=form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.product.get_absolute_url())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Failed to add the review. Please check the form.")

        with self.assertRaises(Review.DoesNotExist):
            Review.objects.get()

    def test_create_review_view_without_login(self):
        self.client.logout()

        form_data = {
            "text": "Test review text",
            "product": self.product.id,
            "user": self.user.id,
        }

        response = self.client.post(
            reverse("catalog:review-create", args=[self.product.id]), data=form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"/user/login/?next={reverse('catalog:review-create', args=[self.product.id])}"
        )

        with self.assertRaises(Review.DoesNotExist):
            Review.objects.get(text="Test review text")


class FavoriteProductsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
        )
        self.client.force_login(self.user)

        self.category = Category.objects.create(name="Test Category", slug="test-category")

    def test_favorite_products_view(self):

        product1 = Product.objects.create(name="Product 1", price=10.0, category=self.category)
        product2 = Product.objects.create(name="Product 2", price=15.0, category=self.category)
        FavoriteProduct.objects.create(user=self.user, product=product1)
        FavoriteProduct.objects.create(user=self.user, product=product2)

        response = self.client.get(reverse("catalog:favorite_products"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "goods/favorite_products.html")

        self.assertContains(response, "Product 1")
        self.assertContains(response, "Product 2")


class ToggleFavoriteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
        )
        self.client.force_login(self.user)

        self.category = Category.objects.create(name="Test Category", slug="test-category")

        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=50.25,
            discount=2.0,
            quantity=2,
            category=self.category
        )

    def test_toggle_favorite_view_toggle_on(self):
        response = self.client.post(
            reverse("catalog:toggle_favorite"), {"product_id": self.product.id}
        )

        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertTrue(json_response["is_favorite"])
        self.assertEqual(json_response["favorites_count"], 1)

    def test_toggle_favorite_view_toggle_off(self):
        response_toggle_on = self.client.post(
            reverse("catalog:toggle_favorite"), {"product_id": self.product.id}
        )

        self.assertEqual(response_toggle_on.status_code, 200)
        json_response_toggle_on = response_toggle_on.json()
        self.assertTrue(json_response_toggle_on["is_favorite"])
        self.assertEqual(json_response_toggle_on["favorites_count"], 1)

        response_toggle_off = self.client.post(
            reverse("catalog:toggle_favorite"), {"product_id": self.product.id}
        )

        self.assertEqual(response_toggle_off.status_code, 200)
        json_response_toggle_off = response_toggle_off.json()
        self.assertFalse(json_response_toggle_off["is_favorite"])
        self.assertEqual(json_response_toggle_off["favorites_count"], 0)

    def test_toggle_favorite_view_invalid_product_id(self):
        response = self.client.post(
            reverse("catalog:toggle_favorite"), {"product_id": "invalid_id"}
        )

        self.assertEqual(response.status_code, 400)
        json_response = response.json()
        self.assertIn("error", json_response)
        self.assertEqual(json_response["error"], "Invalid product_id")

    def test_toggle_favorite_view_invalid_method(self):
        response = self.client.get(reverse("catalog:toggle_favorite"))

        self.assertEqual(response.status_code, 405)
        json_response = response.json()
        self.assertIn("error", json_response)
        self.assertEqual(json_response["error"], "Method not allowed")


class AddRatingViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
        )
        self.client.force_login(self.user)

        self.category = Category.objects.create(name="Test Category", slug="test-category")

        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=50.25,
            discount=2.0,
            quantity=2,
            category=self.category
        )

    def test_add_rating_view_success(self):

        response = self.client.post(reverse("catalog:add_rating", args=[self.product.id]), {"rating": 4})

        self.assertEqual(response.status_code, 200)

        json_response = response.json()

        self.assertTrue(json_response["success"])
        self.assertIn("average_rating", json_response)

        product = Product.objects.get(id=self.product.id)

        self.assertEqual(product.average_rating(), 4)

    def test_add_rating_view_product_not_found(self):
        response = self.client.post(reverse("catalog:add_rating", args=[999]), {"rating": 4})

        self.assertEqual(response.status_code, 404)

        json_response = response.json()

        self.assertFalse(json_response["success"])
        self.assertEqual(json_response["error"], "Product not found")

    def test_add_rating_view_invalid_method(self):
        response = self.client.get(reverse("catalog:add_rating", args=[self.product.id]))

        self.assertEqual(response.status_code, 405)
        json_response = response.json()
        self.assertFalse(json_response["success"])
        self.assertEqual(json_response["error"], "Invalid request method")
