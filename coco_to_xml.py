import argparse

parser = argparse.ArgumentParser(description='Coco Json to Pascal VOC XML Converter.')

parser.add_argument('--coco_json', required=True, help='Target json file to convert to csv.')
parser.add_argument('--coco_folder', required=False, default='', help='Target folder to find images.')
parser.add_argument('--save_xml', required=True, help='The folder to save annotations xmls.')
parser.add_argument('--database_name', required=False, default='', help='The name of database.')
parser.add_argument('--no_skip_background', dest='skip_background', action='store_false', help='Do not skip \'background\' category.')
parser.set_defaults(skip_background=True)

args = parser.parse_args()

from pycocotools.coco import COCO
from PIL import Image
from pathlib import Path
import os

def write_to_xml(image_name, bboxes, image_folder_name, data_folder, save_folder, database_name):
    
    with Image.open(os.path.join(data_folder, image_name)) as img:
        width, height = img.size
        if img.mode == 'YCbCr':
            depth = 3
        else:
            depth = len(img.mode)
    
    objects = ''
    
    for bbox in bboxes:
        objects = objects + '''
	<object>
		<name>{category_name}</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>{xmin}</xmin>
			<ymin>{ymin}</ymin>
			<xmax>{xmax}</xmax>
			<ymax>{ymax}</ymax>
		</bndbox>
	</object>'''.format(
            category_name = bbox[0],
            xmin = bbox[1],
            ymin = bbox[2],
            xmax = bbox[3],
            ymax = bbox[4]
        )
    
    xml = '''<annotation>
	<folder>{image_folder_name}</folder>
	<filename>{image_name}</filename>
	<source>
		<database>{database_name}</database>
	</source>
	<size>
		<width>{width}</width>
		<height>{height}</height>
		<depth>{depth}</depth>
	</size>
	<segmented>0</segmented>{objects}
</annotation>'''.format(
        image_folder_name = image_folder_name,
        image_name = image_name,
        database_name = database_name,
        width = width,
        height = height,
        depth = depth,
        objects = objects
    )
    
    anno_path = os.path.join(save_folder, os.path.splitext(image_name)[0] + '.xml')
    
    with open(anno_path, 'w') as file:
        file.write(xml)
    
Path(args.save_xml).mkdir(parents=True, exist_ok=True)

image_folder_name = os.path.basename(os.path.abspath(args.coco_folder))

coco = COCO(args.coco_json)

imgIds = coco.getImgIds()

if not args.database_name:
    args.database_name = image_folder_name

print('Write annotations file...')

total = len(imgIds)
now = 1

for imgId in imgIds:
    
    img = coco.loadImgs(imgId)[0]
    
    if not os.path.isfile(os.path.join(args.coco_folder, img['file_name'])):
        print('The image {} is not exist.'.format(img['file_name']))
        exit()
    
    anno_list = []
        
    annIds = coco.getAnnIds(imgIds=imgId)

    for annId in annIds:
        ann = coco.loadAnns(annId)[0]
        cat = coco.loadCats(ann['category_id'])[0]
        
        if cat['name'] == 'background' and args.skip_background == True:
            continue
        
        box = ann['bbox']
        anno_list.append([cat['name'], int(box[0]), int(box[1]), int(box[0]+box[2]), int(box[1]+box[3])])

    write_to_xml(img['file_name'], anno_list, image_folder_name, args.coco_folder, args.save_xml, args.database_name)
    print('Write xml files ({} / {})'.format(now, total))
    now = now + 1

print('Annotations file was written!')
