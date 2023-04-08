<img src="assets/BMI.jpg" alt="BMI.jpg" style="zoom:10%;" />


# <p align="center">TAFA-LAMS</p>

## Installation

To install TAFA-LAMS, you can use the following command:

```bash
pip install -r requirements.txt
```

## Uasge

### 1. Data prepare

You need prepare a mzML format data

### 2.Rewrite TAFA-LAMS/config.py

This file contents the config of TAFA-LAMS, you need rewrite the config file according to your data.
You can build your config file according to the following template:

```python
params = [
    {
        'filePath': 'The mzML data path',
        'savePath': 'Processed data save path
        'saveName': 'Processed data save name, prefix must be xlsx',
        'mz': [
            mz num list
        ],
        'loss': offset float num,
        'timePoints': [[0.0, 1, 1.37, 1.46], [0.0, 1, 1.62, 1.68], [0.0, 1, 1.98, 2.04], [0.0, 1, 2.36, 2.44],
                       [0.0, 1, 2.57, 2.60], [0.0, 1, 2.78, 2.84], [0.0, 1, 3.01, 3.10], [0.0, 1, 3.24, 3.31],
                       [0.0, 1, 3.49, 3.57], [0.0, 1, 3.69, 3.74],
                       [0.0, 1, 3.86, 3.92], [0.0, 1, 4.26, 4.29], [0.0, 1, 5.02, 5.04], [0.0, 1, 5.20, 5.24],
                       [0.0, 1, 5.43, 5.50], [0.0, 1, 5.69, 5.75],
                       [0.0, 1, 6.14, 6.19], [0.0, 1, 6.81, 6.85], [0.0, 1, 7.15, 7.22], [0.0, 1, 8.05, 8.13],
        'tags': [
            '22:6/16:0/14:0', '22:5/16:0/14:0', '22:6/16:0/15:0', '22:5/16:0/15:0',
            '22:6/16:0/16:0', '22:5/16:0/16:0', '22:6/22:6/14:0', '22:6/22:5/14:0',
            '22:6/22:6/15:0', '22:6/22:5/15:0', '22:6/22:6/16:0', '22:6/22:5/16:0',
            '22:6/22:6/22:6', '22:6/22:6/22:5'
        ],
        'elementNames': ['14:0', '15:0', '16:0', '22:5', '22:6'],
        'ratios': [0, 0.1955, 0, 0.20321, 0, 0.2093, 0, 0.2371, 0, 0.24541, 0, 0.2522, 0, 0.2994]
    },
    {
        
    }
]
```


## License

TAFA-LAMS is licensed under the MIT License. See [LICENSE](LICENSE) for the full license text.

## Citing TAFA-LAMS

If you use TAFA-LAMS in your research, please cite the following paper:

``` 
@article{kirillov2023segany,
    title={An Efficient High-throughput Screening Method for Fatty Acid Producing Strains Using in Situ LA-naonoESI-MS with A TAFA-LEMS Python Package}, 
    author={Huan Liu, Tianlun Cui, Wei Gao, Sen Wang, Xiaojin Song, Zhuojun Wang, Huidan Zhang, Shiming Li, Qiu Cui1},
    journal={arXiv:2304.02643},
    year={2023}
}
```
