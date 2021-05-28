import json
import sys
import getopt
import time
import cv2 as cv
import numpy as np
# from matplotlib import pyplot as plt


# load image
def load_image(r_path):
    img = cv.imread(r_path)
    if img is None:
        print('Could not find the image')
        return None
    else:
        cv.imshow('image', img)
        key = cv.waitKey(0)
        cv.destroyAllWindows()
        return img


# load template
def load_template(r_path):
    template = cv.imread(r_path)
    return template


# search for template occurrences
def detect_template(img, template, threshold):
    img_green = img[:, :, 1]
    template = template[:, :, 1]
    counter = 0
    width, height = template.shape[::-1]
    # list of all tree coordinates
    coords = [(0, 0)]
    t0 = time.time()
    res = cv.matchTemplate(img_green, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        flag = True
        for coord in coords:
            if np.sqrt(np.power(pt[0]-coord[0], 2)+np.power(pt[1]-coord[1], 2)) < width:
                flag = False    # distance is too small
        if flag is True:
            counter += 1
            cv.rectangle(img, pt, (pt[0] + width, pt[1] + height), (0, 0, 255), 2)
            coords.append(tuple([pt[0], pt[1]]))
            # print(coords)
    t1 = time.time()
    print('Detecția a durat {timp}sec'.format(timp=t1 - t0))
    # show result of search
    print('{count} trees in image'.format(count=counter))
    cv.imshow('result', img)
    key = cv.waitKey(0)
    cv.imwrite('res.png', img)
    return counter


# read data from json
def read_data(r_path):
    with open(r_path) as json_file:
        data = json.load(json_file)
    return data


def show_data(data):
    for obj in data['forests']:
        print('Latitude:' + obj['latitude'])
        print('Longitude:' + obj['longitude'])
        print('Number:' + obj['count'])


def write_data(data, r_path):
    with open(r_path, 'w') as outfile:
        json.dump(data, outfile)


def save_result(data, count=0, lat=35, long=40):
    data['forests'].append({
        "latitude": lat,
        "longitude": long,
        "count": count
    })
    return data


def main(argv):
    img_input = 'images/forest2.png'
    temp_input = 'templates/tree3.png'
    source_path = dest_path = 'data.txt'
    threshold = 0.5
    opts, args = getopt.getopt(argv, "hi:t:p:s:d:")
    for opt, arg in opts:
        if opt == '-h':
            print('detect.py -i <inputimage> -t <templateimage> -p <threshold> -s <inputdata> -d <outputdata>')
            sys.exit()
        elif opt == '-i':
            img_input = arg
        elif opt == '-t':
            temp_input = arg
        elif opt == '-s':
            source_path = arg
        elif opt == '-d':
            dest_path = arg
        elif opt == '-p':
            threshold = float(arg)
    image = load_image(img_input)
    template = load_template(temp_input)
    num_of_occurrences = detect_template(image, template, threshold)
    data = read_data(source_path)
    write_data(save_result(data, num_of_occurrences), dest_path)


if __name__ == "__main__":
    main(sys.argv[1:])
