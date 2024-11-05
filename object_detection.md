# Object detection 

The inference results are provided in the eCAL topic `object_detection` as JSON data. The following example show how an object could look like:

```json
{
    "iso_time": "2024-11-05T14:23:07.263719",
    // Class labels for each bounding box
    "class_ids": [
        0.0 // person
    ],
    // Confidence scores for each box
    "confidences": [
        0.944169819355011 // confidence person
    ],
    // Boxes in [x1, y1, x2, y2] format
    "xyxy": [
        [
            141.6815185546875,  // x1
            182.14732360839844, // y1
            564.3827514648438,  // x2
            479.19677734375     // y2
        ]
    ],
    // Boxes in [x, y, width, height] format
    "xywh": [
        [
            353.0321350097656,  // x center of bounding box
            330.67205810546875, // y center of bounding box
            422.70123291015625, // width
            297.0494384765625   // height
        ]
    ],
    // Normalized [x1, y1, x2, y2] boxes relative to original image size (height: 480, width: 640)
    "xyxyn": [
        [
            0.22137737274169922, // x1
            0.37947359681129456, // y1
            0.8818480372428894, // x2
            0.9983266592025757 // y2
        ]
    ],
    // Normalized [x, y, width, height] boxes relative to original image size (height: 480, width: 640)
    "xywhn": [
        [
            0.5516127347946167, // x center of bounding box
            0.6889001727104187, // y center of bounding box
            0.6604706645011902, // width
            0.6188530325889587  // height
        ]
    ]
}
```

**Note:** The original image size is 480x640 (width x height).

The following table describes the class ids with the corresponding lables:

| class_id | label          |
|----------|----------------|
| 0        | person         |
| 1        | bicycle        |
| 2        | car            |
| 3        | motorcycle     |
| 4        | airplane       |
| 5        | bus            |
| 6        | train          |
| 7        | truck          |
| 8        | boat           |
| 9        | traffic light  |
| 10       | fire hydrant   |
| 11       | stop sign      |
| 12       | parking meter  |
| 13       | bench          |
| 14       | bird           |
| 15       | cat            |
| 16       | dog            |
| 17       | horse          |
| 18       | sheep          |
| 19       | cow            |
| 20       | elephant       |
| 21       | bear           |
| 22       | zebra          |
| 23       | giraffe        |
| 24       | backpack       |
| 25       | umbrella       |
| 26       | handbag        |
| 27       | tie            |
| 28       | suitcase       |
| 29       | frisbee        |
| 30       | skis           |
| 31       | snowboard      |
| 32       | sports ball    |
| 33       | kite           |
| 34       | baseball bat   |
| 35       | baseball glove |
| 36       | skateboard     |
| 37       | surfboard      |
| 38       | tennis racket  |
| 39       | bottle         |
| 40       | wine glass     |
| 41       | cup            |
| 42       | fork           |
| 43       | knife          |
| 44       | spoon          |
| 45       | bowl           |
| 46       | banana         |
| 47       | apple          |
| 48       | sandwich       |
| 49       | orange         |
| 50       | broccoli       |
| 51       | carrot         |
| 52       | hot dog        |
| 53       | pizza          |
| 54       | donut          |
| 55       | cake           |
| 56       | chair          |
| 57       | couch          |
| 58       | potted plant   |
| 59       | bed            |
| 60       | dining table   |
| 61       | toilet         |
| 62       | tv             |
| 63       | laptop         |
| 64       | mouse          |
| 65       | remote         |
| 66       | keyboard       |
| 67       | cell phone     |
| 68       | microwave      |
| 69       | oven           |
| 70       | toaster        |
| 71       | sink           |
| 72       | refrigerator   |
| 73       | book           |
| 74       | clock          |
| 75       | vase           |
| 76       | scissors       |
| 77       | teddy bear     |
| 78       | hair drier     |
| 79       | toothbrush     |

**Note:** Ignore the class ids you are not interested in in your application.