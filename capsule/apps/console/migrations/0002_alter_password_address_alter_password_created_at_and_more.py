# Generated by Django 4.2.4 on 2023-09-08 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("console", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="password",
            name="address",
            field=models.CharField(
                blank=True, max_length=64, null=True, verbose_name="آدرس ایمیل"
            ),
        ),
        migrations.AlterField(
            model_name="password",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد"),
        ),
        migrations.AlterField(
            model_name="password",
            name="difficulty",
            field=models.CharField(
                choices=[("h", "سخت"), ("g", "خوب"), ("w", "ضعیف")],
                default="g",
                max_length=8,
                verbose_name="سختی",
            ),
        ),
        migrations.AlterField(
            model_name="password",
            name="melli",
            field=models.CharField(
                blank=True, max_length=10, null=True, verbose_name="کد ملی"
            ),
        ),
        migrations.AlterField(
            model_name="password",
            name="title",
            field=models.CharField(
                blank=True, max_length=64, null=True, verbose_name="عنوان"
            ),
        ),
        migrations.AlterField(
            model_name="password",
            name="type",
            field=models.CharField(
                choices=[("e", "ایمیل"), ("p", "تلفن")],
                default="e",
                max_length=8,
                verbose_name="نوع نام کاربری",
            ),
        ),
        migrations.AlterField(
            model_name="password",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش"),
        ),
        migrations.AlterField(
            model_name="password",
            name="username",
            field=models.CharField(max_length=128, verbose_name="نام کاربری"),
        ),
        migrations.CreateModel(
            name="Card",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bank", models.CharField(max_length=64, verbose_name="بانک")),
                (
                    "c_number",
                    models.CharField(max_length=16, verbose_name="شماره کارت"),
                ),
                ("cvv2", models.CharField(max_length=4, verbose_name="کد اعتبار سنجی")),
                ("exp_month", models.CharField(max_length=2, verbose_name="ماه انقضا")),
                ("exp_year", models.CharField(max_length=2, verbose_name="سال انقضا")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cards",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="کاربر",
                    ),
                ),
            ],
            options={
                "verbose_name": "کارت",
                "verbose_name_plural": "کارت ها",
            },
        ),
    ]