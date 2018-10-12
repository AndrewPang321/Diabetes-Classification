# Diabetes-Classification
A course project - using gradient boost to perform multi-class classification on diabetes

## Frameworks
- CatBoost
- Numpy
- Scikit-learn

## To generate data
`python generate_data.py {datasize}`

For example, `python generate_data.py 1000`

## To train the model
`python medical_train.py {datasize to use}`

For example, `python medical_train.py 1000`

If you would like to read the logging details during training process, add `verbose` at the end.

For example, `python medical_train.py 1000 verbose`
