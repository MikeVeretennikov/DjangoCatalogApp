import django.contrib.admin

import feedback.models


class StatusLog(django.contrib.admin.TabularInline):
    model = feedback.models.StatusLog


class FeedbackAuthor(django.contrib.admin.TabularInline):
    model = feedback.models.FeedbackAuthor
    fields = (
        feedback.models.FeedbackAuthor.name.field.name,
        feedback.models.FeedbackAuthor.mail.field.name,
    )
    can_delete = False


class FeedbackFiles(django.contrib.admin.TabularInline):
    model = feedback.models.FeedbackFile
    fields = (feedback.models.FeedbackFile.file.field.name,)


@django.contrib.admin.register(feedback.models.Feedback)
class FeedbackAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.text.field.name,
        feedback.models.Feedback.created_on.field.name,
        feedback.models.Feedback.status.field.name,
    )
    list_editable = (feedback.models.Feedback.status.field.name,)
    inlines = [
        StatusLog,
        FeedbackAuthor,
        FeedbackFiles,
    ]

    def save_model(self, request, obj, form, change):
        if change:
            old_status = feedback.models.Feedback.objects.get(pk=obj.pk).status

            if old_status != obj.status:

                feedback.models.StatusLog.objects.create(
                    feedback=obj,
                    user=request.user,
                    from_status=old_status,
                    to_status=obj.status,
                )

        super().save_model(request, obj, form, change)


django.contrib.admin.site.register(feedback.models.StatusLog)


__all__ = ()
