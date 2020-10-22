# necessary imnports
from dt import DecisionTree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

"""
### Accuracy Score: pred, act ###
Accuracy score shows how well the model is working, its calculated by, the number of correct
predictions divided by the total number predictions made.
"""
def acc_score(pred, act): # accuracy score funtion
    correct = 0 # set the correct equal to 0
    pred_len = len(pred) # set the pred_len equal to the length of the pred input
    for i in range(pred_len): # for loop, i in range of the pred_len
        if int(pred[i]) == act[i]: # if the pred value is eqaul to the actual value
            correct += 1 # add 1 to the correct
    return correct/pred_len # return the correct divded by the pred_len
"""
### Decicsion Tree Models: ###
Models function loads the wanted data, and executes both the Scratch and SKlearn Decision Trees.
"""
def models(): # models function
    iris = load_iris() # load the sklearn iris data set
    feature = iris.data[:,:2] # set the features of the data
    label = iris.target # set the label as the target
    X_train, X_test, y_train, y_test = train_test_split(feature, label, random_state= 42) # split the data into train and test
    """
    ### Created Decision Tree Model ###
    """
    scratch_dt_model =  DecisionTree(max_depth = 2, # create our decision tree model with params
                                min_splits = 10)
    scratch_dt_model.fit(X_train, y_train) # fit the model
    scratch_dt_model_pred = scratch_dt_model.pred(X_test) # create predicitons from the model
    """
    ### Sklearn Decision Tree Model ###
    """
    sk_dt_model = DecisionTreeClassifier(max_depth= 2, # use the decision tree model from Sklearn with params
                                         min_samples_split= 10)
    sk_dt_model.fit(X_train, y_train) # fit the model
    sk_dt_model_pred = sk_dt_model.predict(X_test) # create predicitons from the model
    """
    ### Results ###
    """
    print("Scratch Model Accuracy : {0}".format(acc_score(scratch_dt_model_pred, y_test))) # print the scratch models accuracy score
    print("SK-Learn Model Accuracy : {0}".format(acc_score(sk_dt_model_pred, y_test))) # print the sklearn models accuracy score
    print(list(zip(scratch_dt_model_pred, sk_dt_model_pred, y_test))) # print the scratch models prediction, sklearn models prediction, and the actual value

if  __name__ == "__main__":
    models()
