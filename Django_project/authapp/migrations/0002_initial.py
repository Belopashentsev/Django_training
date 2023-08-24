import authapp.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="shopclient",
            options={
                "ordering": ["-is_active", "-is_superuser", "-is_staff", "username"]
            },
        ),
        migrations.AddField(
            model_name="shopclient",
            name="activation_key",
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name="shopclient",
            name="activation_key_expires",
            field=models.DateTimeField(
                default=authapp.models.get_activation_key_expires
            ),
        ),
    ]
