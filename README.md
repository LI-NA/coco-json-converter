# Coco json converter.

This is the set of tiny python scripts to convert coco json to other format. The following formats are supported:

* [Convert to XML](#coco-to-xml) used by [Pascal VOC](http://host.robots.ox.ac.uk/pascal/VOC/)
* [Convert to CSV](#coco-to-csv) used by [keras-retinanet](https://github.com/fizyr/keras-retinanet#csv-datasets)

## Requirement

Python 3.6, [cocoapi](https://github.com/cocodataset/cocoapi) (pycocotools), [pillow](https://pypi.org/project/Pillow/) (coco_to_xml)

## Usage

```text
project
│   coco_to_csv.py
│   coco_to_xml.py
│   train.json 
│   val.json 
│
└───train
│   │   image001.jpg
│   │   image002.jpg
│   │  ...
│   
└───val
    │   image001.jpg
    │   image002.jpg
    │   ...
```

The directory structure described below is the same as above (train.json and the image files in train folder).

### COCO to XML

`coco_to_xml.py` script can convert coco json to xml files. AND IT IS FAST (a few seconds for thousands of images)!

```shell
python coco_to_xml.py --coco_json=train.json --coco_folder=train --save_xml=train_xml --database_name=Database
```

By default, this script skip background category (class) because usually it is not required. If you want to add background category, use this flag.

```shell
python coco_to_xml.py .... --no_skip_background
```

Also you can check the help.

```shell
python coco_to_xml.py --help
```

#### XML Result format

The annotations xml file format is:

```xml
<annotation>
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
  <segmented>0</segmented>
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
  </object>
</annotation>
```

And the xml file was saved like this:

```text
project
│   coco_to_xml.py
│   train.json 
│   val.json 
│
└───train
│   │   image001.jpg
│   │   image002.jpg
│   │  ...
│   
└───train_xml
    │   image001.xml
    │   image002.xml
    │   ...
```

### COCO to CSV

`coco_to_xml.py` script can convert coco json to single csv file.

```shell
python coco_to_csv.py --coco_json=train.json --coco_folder=train --save_ann=train.csv --save_cat=class.csv
```

By default, this script skip background category (class) because usually it is not required. If you want to add background category, use this flag.

```shell
python coco_to_csv.py .... --no_skip_background
```

And this script will check image file is exist, you can ignore that using this flag.

```shell
python coco_to_csv.py .... --no_check_file
```

Also you can check the help.

```shell
python coco_to_csv.py --help
```

#### CSV Result format

The annotations csv file format is:

```text
path/to/image.jpg,x1,y1,x2,y2,class_name
```

The classes csv file format is:

```text
class_name,id
```

## License

[MIT License](LICENSE)
