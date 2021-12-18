import colorsys
from collections import Counter
from math import sqrt, inf

import cv2
from sklearn.cluster import KMeans

from config.celery import app as celery_app
from drops.models import Drop

color_list = [
    {
        'hex':'E8E8E8',
        'rgb':[232, 232, 232]
    },
    {
        'hex':'E72525',
        'rgb':[231, 37, 37,]
    },
    {
        'hex':'F48700',
        'rgb':[244, 135, 0]
    },
    {
        'hex':'FFBD38',
        'rgb':[255, 189, 56]
    },
    {
        'hex':'F1F129',
        'rgb':[241, 241, 41]
    },
    {
        'hex':'A9E418',
        'rgb':[169, 228, 24]
    },
    {
        'hex':'06D506',
        'rgb':[6, 213, 6]
    },
    {
        'hex':'0ECB9B',
        'rgb':[14, 203, 155]
    },
    {
        'hex':'1AE0E0',
        'rgb':[26, 224, 224]
    },
    {
        'hex':'0BBBF5',
        'rgb':[11, 187, 245]
    },
    {
        'hex':'1F55F8',
        'rgb':[31, 85, 248]
    },
    {
        'hex':'0000FF',
        'rgb':[0, 0, 255]
    },
    {
        'hex':'7F00FF',
        'rgb':[127, 0, 255]
    },
    {
        'hex':'BF00FF',
        'rgb':[191, 0, 255]
    },
    {
        'hex':'EA06B1',
        'rgb':[234, 6, 177]
    },
]

list_of_rgb = []
list_of_hex = []

for color in color_list:
    list_of_rgb.append(color['rgb'])
    list_of_hex.append(color['hex'])

list_of_hsv = list(map(lambda x: colorsys.rgb_to_hsv(*x), list_of_rgb))


def prep_image(raw_img):
    modified_img = cv2.resize(raw_img, (900, 600), interpolation=cv2.INTER_AREA)
    modified_img = modified_img.reshape(modified_img.shape[0] * modified_img.shape[1], 3)
    return modified_img


def color_analysis(img):
    clf = KMeans(n_clusters=1)
    color_labels = clf.fit_predict(img)
    center_colors = clf.cluster_centers_
    counts = Counter(color_labels)
    ordered_colors = [center_colors[i] for i in counts.keys()]
    return colorsys.rgb_to_hsv(*ordered_colors[0])


def closest_colour(selected_colour):
    shortest_distance, closest_color_number = inf, None

    for i, colour in enumerate(list_of_hsv):
        current_distance = sqrt(pow(colour[0] - selected_colour[0], 2) + pow(colour[1] - selected_colour[1], 2) + pow(
            colour[2] - selected_colour[2], 2))

        if current_distance < shortest_distance:
            shortest_distance = current_distance
            closest_color_number = i

    return list_of_hex[closest_color_number]


@celery_app.task(name='api.task.find_closest_color', queue='image_converter', routing_key='image_converter')
def find_closest_color(drop_pk,image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    modified_image = prep_image(image)
    hsv = color_analysis(modified_image)
    set_closest_color.delay(drop_pk,closest_colour(hsv))


@celery_app.task(name='api.task.set_closest_color', queue='solo_task', routing_key='solo_task')
def set_closest_color(drop_pk, hex_color):
    drop = Drop.objects.get(pk=drop_pk)
    drop.color = hex_color
    drop.save()

