# from django.db.models import F
#
# from api.models import User
# from api.utils.validators import datetime_check_and_convert
#
#
# def query_filter(request, queryset):
#     """Фильтрует queryset по query параметрам"""
#
#     query_params = request.query_params
#     query_kwargs = {}
#     order_args = []
#     step = 1
#     for key, value in query_params.items():
#         if key == 'step':
#             step = int(value)
#             continue
#         value = str(value)
#         if key == 'page':
#             continue
#         if key == 'ordering':
#             order_args.extend(value.split(','))
#             continue
#         action = 'eq'
#         if value.startswith('start'):
#             action = 'range'
#             value = value.replace("T"," ").replace('start', '',1).split('stop')
#         elif value.startswith('in'):
#             action = 'in'
#             value = [value.replace('in', '',1)]
#         elif value.startswith('contains'):
#             action = 'in'
#             value = [value.replace('in', '',1)]
#         elif value.startswith('gte'):
#             action = 'gte'
#             value = [value.replace('gte', '',1)]
#         elif value.startswith('lte'):
#             action = 'lte'
#             value = [value.replace('lte', '',1)]
#         elif value.startswith('gt'):
#             action = 'gt'
#             value = [value.replace('gt', '',1)]
#         elif value.startswith('lt'):
#             action = 'lt'
#             value = [value.replace('lt', '',1)]
#         else:
#             value = [value]
#
#         if all(datetime_check_and_convert(i) for i in value):
#             value = [datetime_check_and_convert(i) for i in value]
#         else:
#             pass
#
#         if action != 'range':
#             value = value[0]
#         if action != 'eq':
#             query_kwargs[f'{key}__{action}'] = value
#         else:
#             query_kwargs[f'{key}'] = value
#     try:
#         return queryset.annotate(idmod4=F('id') % step).filter(**query_kwargs,idmod4=0).order_by(*order_args).reverse()
#     except:
#         return User.objects.none()
