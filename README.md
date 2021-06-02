# Coco json to CSV

The tiny python script to convert coco json to csv that use in [keras-retinanet](https://github.com/fizyr/keras-retinanet#csv-datasets).

## Requirement

Python 3.6, [cocoapi](https://github.com/cocodataset/cocoapi) (pycocotools).

## Usage

```text
project
│   coco_to_csv.py
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

If the directory is like above (train.json and the image files in train folder), you can use this script like this.

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

## Result format

The annotations csv file format is:

```text
path/to/image.jpg,x1,y1,x2,y2,class_name
```

The classes csv file format is:

```text
class_name,id
```
