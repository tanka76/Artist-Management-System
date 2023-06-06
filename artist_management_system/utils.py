
from django.db import models
from django.forms import Textarea
from django.forms.fields import BooleanField, DateField, DateTimeField
from django.forms.widgets import DateInput


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class BaseForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if type(self.fields[field]) != BooleanField:
                self.fields[field].widget.attrs[
                    "class"
                ] = "form-control form-control-solid"

            if type(self.fields[field]) == BooleanField:
                self.fields[field].widget.attrs.update(
                    {"class": "form-check-input", "type": "checkbox"}
                )

            if type(self.fields[field]) == DateTimeField:
                self.fields[field].widget = DateInput(
                    attrs={
                        "class": "form-control datetimepicker-input form-control-solid",
                        "type": "datetime-local",
                    }
                )
            if type(self.fields[field]) == DateField:
                self.fields[field].widget = DateInput(
                    attrs={
                        "class": "form-control datetimepicker-input col-2 form-control-solid",
                        "type": "date",
                    }
                )
            if type(self.fields[field]) == Textarea:
                self.fields[field].widget.attrs["id"] = "kt_docs_ckeditor_classic"