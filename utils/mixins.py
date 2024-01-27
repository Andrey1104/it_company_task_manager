from django import forms
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy


class ModelDeleteMixin:
    @staticmethod
    def remove_object(
        model_id, object_id, attribute, main_model, object_model
    ):
        model = get_object_or_404(main_model, pk=model_id)
        obj = get_object_or_404(object_model, pk=object_id)

        if obj in getattr(model, attribute).all():
            getattr(model, attribute).remove(obj)
            model.save()

    @staticmethod
    def get_success_url(model_id=None):
        if model_id:
            return reverse_lazy("executor:team_detail", args=[model_id])
        return reverse_lazy("executor:project_list")


class SearchMixin:
    search_form_class = None
    search_fields = []

    def __init__(self):
        self.request = None

    @staticmethod
    def get_search_form_kwargs():
        return {}

    def get_search_query(self):
        return self.request.GET.get("name", "")

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.get_search_query()
        if search_query:
            for field in self.search_fields:
                queryset = queryset.filter(
                    **{f"{field}__icontains": search_query}
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_form = self.search_form_class(
            initial={"name": self.get_search_query()},
            **self.get_search_form_kwargs(),
        )
        context["search_form"] = search_form
        return context


class SearchFormMixin(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Enter name..."}),
        required=False,
        label="",
    )

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(SearchFormMixin, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "common-form-field-style"})


class StyleFormMixin(forms.ModelForm):
    class Meta:
        attrs = {
            "style": "background-color:rgba(220, 240, 220, 0.5);"
            "margin-bottom: 20px",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ != forms.CheckboxSelectMultiple:
                field.widget.attrs.update(self.Meta.attrs)
