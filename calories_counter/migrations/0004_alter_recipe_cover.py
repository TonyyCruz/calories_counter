# Generated by Django 4.1.7 on 2023-02-23 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calories_counter", "0003_alter_recipe_author_alter_recipe_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="cover",
            field=models.ImageField(
                upload_to="recipes/recipes/covers/%Y/%m/%d"),
        ),
    ]
