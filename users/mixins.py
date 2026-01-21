from django import forms


class StyleFormMixin:
    """
    Добавляет Bootstrap-классы к полям формы:
    - input/textarea/file -> form-control
    - select -> form-select
    - checkbox -> form-check-input
    """

    def _append_class(self, widget, css_class: str) -> None:
        existing = widget.attrs.get("class", "")
        classes = set(existing.split()) if existing else set()
        classes.add(css_class)
        widget.attrs["class"] = " ".join(sorted(classes))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.HiddenInput):
                continue

            if isinstance(widget, forms.CheckboxInput):
                self._append_class(widget, "form-check-input")
            elif isinstance(widget, forms.Select):
                self._append_class(widget, "form-select")
            else:
                self._append_class(widget, "form-control")
