from django.shortcuts import render
from django.views import View
from .models import Student, Teacher, LunchItem, LunchItemOrder
from django.core.exceptions import ValidationError
from .generate_report import populate_pdf_response
from collections import defaultdict
from decimal import Decimal
import logging  #noqa


def index(request):
  return render(request, 'index.html')


def _get_lunch_items_from_request(request):
  lunch_item_names = ",".join(request.GET.getlist('lunch_items'))
  lunch_item_names = lunch_item_names.split(",")
  lunch_item_model_list = list(
      LunchItem.objects.filter(name__in=lunch_item_names))
  if len(lunch_item_model_list) <= 0:
    return list(LunchItem.objects.all())
  return lunch_item_model_list

# Author : Dias
# Date : 2024-6-13
# Desc : Get specific lunch data from the list of request.
def _get_specific_lunch_data(lunch_item_model_list):
    lunch_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for item in lunch_item_model_list:
        orders = LunchItemOrder.objects.filter(lunch_item=item)
        for order in orders:
            if order.student:
                teacher = order.student.teacher
                teacher_name = teacher.name if teacher else '-'
                orderer_name = order.student.name
            else:
                teacher_name = order.teacher.name
                orderer_name = teacher_name
            lunch_data[item.name][teacher_name][orderer_name] += order.quantity
    return lunch_data

# Author : Dias
# Date : 2024-6-13
# Desc : Get combined lunch data from the list of request.
def _get_combined_lunch_data(lunch_item_model_list):
    lunch_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    orders = LunchItemOrder.objects.filter(lunch_item__in=lunch_item_model_list)
    for order in orders:
        if order.student:
            teacher = order.student.teacher
            teacher_name = teacher.name if teacher else '-'
            orderer_name = order.student.name
        else:
            teacher_name = order.teacher.name
            orderer_name = teacher_name
        lunch_data[teacher_name][orderer_name][order.lunch_item.name] += order.quantity
    return lunch_data

# Author : Dias
# Date : 2024-6-13
# Desc : Convert default to regular dictionary.
def _default_to_regular_dict(d):
    if isinstance(d, defaultdict):
        d = {k: _default_to_regular_dict(v) for k, v in d.items()}
    return d


def lunch_report(request):
  lunch_item_model_list = _get_lunch_items_from_request(request)
  lunch_data = _get_specific_lunch_data(lunch_item_model_list)
  
  return populate_pdf_response(
      report_title="Lunch Order Report by Item",
      report_template="lunchreports/templates/lunch_order_report.html",
      lunch_data=_default_to_regular_dict(lunch_data),
  )  


def combined_lunch_report(request):
  lunch_item_model_list = _get_lunch_items_from_request(request)
  lunch_data = _get_combined_lunch_data(lunch_item_model_list)
  items_list = [item.name for item in lunch_item_model_list]

  return populate_pdf_response(
      report_title="Combined Lunch Order Report",
      report_template="lunchreports/templates/combined_order_report.html",
      lunch_data=_default_to_regular_dict(lunch_data),
      items_list=items_list
  )

