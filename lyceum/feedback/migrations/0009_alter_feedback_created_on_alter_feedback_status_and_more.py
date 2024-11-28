# Generated by Django 4.2.16 on 2024-11-28 17:15

from django.db import migrations, models
import feedback.models


class Migration(migrations.Migration):

    dependencies = [
        (
            "feedback",
            "0007_remove_feedback_mail_remove_feedback_name_and_more_squashed_0008_alter_feedback_text_alter_feedbackauthor_name",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True,
                help_text="время создания",
                null=True,
                verbose_name="дата создания",
            ),
        ),
        migrations.AlterField(
            model_name="feedback",
            name="status",
            field=models.CharField(
                choices=[
                    ("received", "получено"),
                    ("in_process", "в обработке"),
                    ("replied", "ответ дан"),
                ],
                default="received",
                help_text="статус фидбека",
                max_length=20,
                verbose_name="статус",
            ),
        ),
        migrations.AlterField(
            model_name="feedback",
            name="text",
            field=models.TextField(
                help_text="Что вы хотели сообщить?",
                max_length=3000,
                verbose_name="текст",
            ),
        ),
        migrations.AlterField(
            model_name="feedbackauthor",
            name="name",
            field=models.CharField(
                blank=True,
                help_text="имя",
                max_length=150,
                null=True,
                verbose_name="имя",
            ),
        ),
        migrations.AlterField(
            model_name="feedbackfile",
            name="file",
            field=models.FileField(
                blank=True,
                help_text="файл",
                upload_to=feedback.models.FeedbackFile.get_upload_path,
                verbose_name="файл",
            ),
        ),
        migrations.AlterField(
            model_name="statuslog",
            name="from_status",
            field=models.CharField(
                db_column="from", max_length=20, verbose_name="статус до"
            ),
        ),
        migrations.AlterField(
            model_name="statuslog",
            name="timestamp",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="время создания"
            ),
        ),
        migrations.AlterField(
            model_name="statuslog",
            name="to",
            field=models.CharField(
                db_column="to", max_length=20, verbose_name="статус после"
            ),
        ),
    ]
