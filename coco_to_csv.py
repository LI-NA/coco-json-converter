import argparse

parser = argparse.ArgumentParser(description='Coco Json to Keras RetinaNet CSV Converter.')

parser.add_argument('--coco_json', required=True, help='Target json file to convert to csv.')
parser.add_argument('--coco_folder', required=False, default='', help='Target folder to find images.')
parser.add_argument('--save_ann', required=True, help='The file name to save annotations csv.')
parser.add_argument('--save_cat', required=True, help='The file name to save categories csv.')
parser.add_argument('--no_skip_background', dest='skip_background', action='store_false', help='Do not skip \'background\' category.')
parser.set_defaults(skip_background=True)
parser.add_argument('--no_check_file', dest='check_file', action='store_false', help='Do not check image file is exist.')
parser.set_defaults(check_file=True)

args = parser.parse_args()

from pycocotools.coco import COCO
import csv
import os

abs_save_path = os.path.abspath(os.path.dirname(args.save_ann))
rel_coco_folder = os.path.relpath(args.coco_folder, abs_save_path)

coco = COCO(args.coco_json)

if args.check_file:
    imgIds = coco.getImgIds()
    for imgId in imgIds:
        img = coco.loadImgs(imgId)[0]
        if not os.path.isfile(os.path.join(args.coco_folder, img['file_name'])):
            print('The image {} is not exist. Please ignore this error, use --no_check_file flag.'.format(img['file_name']))
            exit()

csv_file = open(args.save_ann, 'w')
csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)

print('Write annotations file...')

annIds = coco.getAnnIds()
for annId in annIds:
    ann = coco.loadAnns(annId)[0]
    img = coco.loadImgs(ann['image_id'])[0]
    cat = coco.loadCats(ann['category_id'])[0]
    
    if cat['name'] == 'background' and args.skip_background == True:
        continue
        
    x1,y1,w,h = ann['bbox']
    x2 = x1 + w
    y2 = y1 + h
    
    x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
    
    csv_writer.writerow([os.path.join(rel_coco_folder, img['file_name']), str(x1), str(y1), str(x2), str(y2), cat['name']])

csv_file.close()

print('Annotations file was written!')

csv_class_file = open(args.save_cat, 'w')
csv_class_writer = csv.writer(csv_class_file, quoting=csv.QUOTE_MINIMAL)

print('Write classes file...')

catIds = coco.getCatIds()
nowId = 0
for catId in catIds:
    cat = coco.loadCats(catId)[0]
    
    if cat['name'] == 'background' and args.skip_background == True:
        continue
        
    csv_class_writer.writerow([cat['name'], str(nowId)])
    nowId = nowId + 1
    
csv_class_file.close()

print('Classes file was written!')
