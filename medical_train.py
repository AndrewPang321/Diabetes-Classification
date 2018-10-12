## PANG TSZ HIM ANDREW - Data Mining CI6227 - Assignment: Model Training Script
##
## Run the script with 4 parameters: number of records for training, logging of the trainning process;
##          > python medical_train.py 1000 verbose
##

import sys
import sqlite3
import numpy as np
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score

def db_connect():
    try:
        connection = sqlite3.connect("data_gen/medical_records_{}.db".format(sys.argv[1]))
        return connection
    except:
        raise

def select_all_records(table_name):
    try:
        cursor = db_connect().cursor()
        query = "SELECT * FROM patient_info_{}".format(table_name)

        cursor.execute(query)
        rows = cursor.fetchall()

        all_data = np.array(rows)
        data = np.delete(all_data, 10, axis=1)
        label = all_data[:,10]
        
        # Change data labels from categorical to numerical
        # 0 = Not Diabetic, 1 = Pre-Diabetes, 2 = Diabetic
        label[label == "Not Diabetic"] = 0
        label[label == "Pre-Diabetes"] = 1
        label[label == "Diabetic"] = 2

        label = label.astype('float64')

        return data, label
    except:
        raise

if __name__ == "__main__":
    # Initialize data
    train_data, train_label = select_all_records("train")
    eval_data, eval_label = select_all_records("dev")
    test_data, test_label = select_all_records("test")

    if len(sys.argv) == 3 and sys.argv[2] == "verbose":
        # Using MultiClass as loss function is a must for multiclass classification with verbose
        # Setting 'logging_level='Verbose'' will return the following during training:
        # learn error, test error, best error
        model = CatBoostClassifier(depth=6, loss_function='MultiClass', eval_metric='HingeLoss', l2_leaf_reg=0.2, random_seed=42, logging_level='Verbose')
    else:
        print("Training in progress...")
        model = CatBoostClassifier(depth=6, loss_function='MultiClass', l2_leaf_reg=0.2, random_seed=42, logging_level='Silent')

    
    # Train the model
    model.fit(train_data, train_label, cat_features=[0,6,8], eval_set=(eval_data, eval_label), plot=True)

    # Save the model in catboost format, cbm = CatBoost Binary Format
    model.save_model("medical.mlmodel", format="cbm")

    # Prediction
    preds_class = model.predict(eval_data)
    preds_proba = model.predict_proba(eval_data)
    print("class = ", preds_class)
    # print("proba = ", preds_proba)

    acc = accuracy_score(eval_label, preds_class.flatten())
    print("accuracy = ", acc)
