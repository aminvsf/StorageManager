from django.forms import inlineformset_factory, BaseInlineFormSet

from .models import Input, InputDetail, Output, OutputDetail


class CustomFormSet(BaseInlineFormSet):
    def clean(self):
        selected_products = [form.cleaned_data.get('product') for form in self.forms]
        for index, form in enumerate(self.forms):
            product = form.cleaned_data.get('product')
            if product in selected_products[:index]:
                form.add_error('product', 'این محصول تکراری است.')


InputDetailCreateFormSet = inlineformset_factory(Input, InputDetail, extra=1, fields=('product', 'value'),
                                                 can_delete=False, formset=CustomFormSet)
OutputDetailCreateFormSet = inlineformset_factory(Output, OutputDetail, extra=1, fields=('product', 'value'),
                                                  can_delete=False, formset=CustomFormSet)

InputDetailUpdateFormSet = inlineformset_factory(Input, InputDetail, extra=1, fields=('product', 'value'),
                                                 can_delete=False, formset=CustomFormSet)
OutputDetailUpdateFormSet = inlineformset_factory(Output, OutputDetail, extra=1, fields=('product', 'value'),
                                                  can_delete=False, formset=CustomFormSet)
