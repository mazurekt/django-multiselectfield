# -*- coding: utf-8 -*-
# Copyright (c) 2012 by Pablo Martín <goinnn@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this programe.  If not, see <http://www.gnu.org/licenses/>.

from django import forms
from django.forms.widgets import CheckboxSelectMultiple, SelectMultiple

from ..utils import get_max_length
from ..validators import (MaxChoicesValidator, MaxValueMultiFieldValidator,
                          MinChoicesValidator)


# class CustomRadioSelect(RadioSelect):
#     # This custom_multiple_input uses the original django template but add html breaks (<br>).
#     template_name = 'multiselectfield/forms/widgets/custom_multiple_input.html'


class CustomRadioSelect(CheckboxSelectMultiple):
    # This custom_multiple_input uses the original django template but add html breaks (<br>).
    allow_multiple_selected = False
    template_name = 'multiselectfield/forms/widgets/custom_multiple_input.html'
    input_type = 'radio'
    # template_name = 'django/forms/widgets/radio.html'
    option_template_name = 'django/forms/widgets/radio_option.html'


class CustomSelect(SelectMultiple):
    """
    This is mostly same code of the SelectMultiple widget.
    The only difference is the allow_multiple_selected attribute is False.
    Treat the SelectMultiple as a single Select so the database has the same
    datatype as MultiSelectFormField.
    """
    allow_multiple_selected = False


class CustomCheckboxSelectMultiple(CheckboxSelectMultiple):
    pass


class MultiSelectFormField(forms.MultipleChoiceField):
    widget = forms.CheckboxSelectMultiple

    def __init__(self, *args, **kwargs):
        self.min_choices = kwargs.pop('min_choices', None)
        self.max_choices = kwargs.pop('max_choices', None)
        self.max_length = kwargs.pop('max_length', None)
        super(MultiSelectFormField, self).__init__(*args, **kwargs)
        self.max_length = get_max_length(self.choices, self.max_length)
        self.validators.append(MaxValueMultiFieldValidator(self.max_length))
        if self.max_choices is not None:
            self.validators.append(MaxChoicesValidator(self.max_choices))
        if self.min_choices is not None:
            self.validators.append(MinChoicesValidator(self.min_choices))


class SingleSelectFormField(forms.MultipleChoiceField):
    """
    The reason that I am inheriting from MultipleChoiceField is to make the
    data types the same in the database so I can easily switch from this
    SingleSelectFormField to a MultiSelectFormField.
    """
    widget = None
    max_choices = 1

    def __init__(self, *args, **kwargs):
        self.max_length = kwargs.pop('max_length', None)
        self.widget = kwargs.pop('widget', None)
        super(SingleSelectFormField, self).__init__(*args, **kwargs)
        self.max_length = get_max_length(self.choices, self.max_length)
        self.validators.append(MaxValueMultiFieldValidator(self.max_length))
        self.validators.append(MaxChoicesValidator(self.max_choices))
