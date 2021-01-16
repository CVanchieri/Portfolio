# necessary imports
import numpy as np

"""
### Decision Tree Class ###
Decision trees are one way to display an algorithm that only contains conditional control statements,
commonly used in operations research, specifically in decision analysis, to help identify a strategy
most likely to reach a goal, but are also a popular tool in machine learning.
"""
class DecisionTree(object): # create a decision tree class 'CART'
    def __init__(self, max_depth, min_splits): # init constructor method
        self.max_depth = max_depth # set the self.max_depth equal to the max_depth value
        self.min_splits = min_splits # set the self.mon_splits equal to _min_splits value
    """
    ### Fit: feature, label ###
    Model fitting is a measure of how well a machine learning model generalizes to similar data to that
    on which it was trained. A model that is well-fitted produces more accurate outcomes. A model that is
    overfitted matches the data too closely. A model that is underfitted doesn't match closely enough.
    """
    def fit(self, feature, label): # fit method
        self.feature = feature # set the self.feature equal to the feature value
        self.label = label # set the self.label equal to the label value
        self.train_data = np.column_stack((self.feature,self.label)) # set the self.train_data with column stack from numpy on the self.feature & self.label
        self.build_tree() # build the tree
    """
    ### Gini Impurity: groups, class labels ###
    Gini Impurity tells us what is the probability of misclassifying an observation and is used in calculation
    of the split, the lower the gini score the better the split is.
    """
    def gini(self, groups, class_labels): # compute gini similiarity method
        number_sample = sum([len(group) for group in groups]) # set the num_sample equal to the sum of the length of group in groups
        gini_score = 0 # set the gini_score equal to 0

        for group in groups: # for loop, group in groups
            size = float(len(group)) # set the size equal to the length of group as a float

            if size == 0: # if the size is equal to 0
                continue # continue
            score = 0.0 # set the score equal to 0.0

            for label in class_labels: # for loop, label in class_labels
                porportion = (group[:,-1] == label).sum() / size # set the proprotion equal to the all but the last item in the group labels sum divided by the size
                score += porportion * porportion # add proprotion times proprotion to the score
            gini_score += (1.0 - score) * (size/number_sample) # add 1 minus the score times the size divided by the num_sample

        return gini_score # return the gini_score
    """
    ### Terminal Node: _group ###
    Terminal nodes (leaf nodes) are the final nodes that do not split further.
    """
    def term_node(self, group): # terminal node method
        class_labels, count = np.unique(group[:,-1], return_counts= True) # set a class_labels count equal to the unique count of all class_labels but the last
        return class_labels[np.argmax(count)] # return the class_labels count
    """
    ### Split: index, val, data ###
    Splitting a node into two sub-nodes is called splitting. It happens at all nodes except leaf nodes (terminal nodes).
    """
    def split(self, index, val, data): # split method
        data_l = np.array([]).reshape(0,self.train_data.shape[1]) # set the data_l equal the reshaped train data array
        data_r = np.array([]).reshape(0, self.train_data.shape[1]) # set the data_r equal the reshaped train data array

        for row in data: # for loop, row in data
            if row[index] <= val:  # if the row index value is less than or equal to the val
                data_l = np.vstack((data_l,row)) # set the data_left equal to the vertial stack of the data_l and row

            if row[index] > val: # if the row index value is greater than the val
                data_r = np.vstack((data_r, row)) # set the data_right equal to the vertial stack of the data_r and row

        return data_l, data_r # return the data_l value and data_r value
    """
    ### Best Split: data ###
    Best split uses the gini score and initial split to check all the values of each attribute and calculates the cost
    of the split to find the best possible split.
    """
    def best_split(self, data): # best split method
        class_labels = np.unique(data[:,-1]) # set the class_labels equal to all the unique values of data but the last
        best_index = 999 # set the best_index to equal 999
        best_val = 999 # set the best_val to equal 999
        best_score = 999 # set the best_score equal to 999
        best_groups = None # set the best_groups equal to None

        for i in range(data.shape[1]-1): # for loop, i in the range of the data reshaped
            for row in data: # for loop, row in data
                groups = self.split(i, row[i], data) # set groups equal to the split function on i , row[i], and data
                gini_score = self.gini(groups,class_labels) # set the gini_score equal the the gini function on groups and class labels

                if gini_score < best_score: # if gini_score is less than the best_score
                    best_index = i # set the best_index equal to i value
                    best_val = row[i] # set the best_val equal to row[i] value
                    best_score = gini_score # set the best_score equal to gini_score
                    best_groups = groups # set the best_groups equal to groups
        result = {} # create an empty dictionary
        result['index'] = best_index # set the result index equal to the best_index
        result['val'] = best_val # set the result val equal to the best_val
        result['groups'] = best_groups # set the result groups equal to the best_groups
        return result # return the result
    """
    ### Recursive Split: node, depth ###
    Recursively split the data and check for early stop arguments to create terminal node.
    """
    def rec_split(self, node, depth): # split branch method
        l_node , r_node = node['groups'] # split node groups into l_node and r_node
        del(node['groups']) # deleted the node groups

        if not isinstance(l_node,np.ndarray) or not isinstance(r_node,np.ndarray): # if its not in the left_node or right_node ndoe array
            node['left'] = self.term_node(l_node + r_node) # set the left node equal to the terminal_node on the left_node and the right_node
            node['right'] = self.term_node(l_node + r_node) # set the right node equal to the terminal_node on the left_node and the right_node
            return

        if depth >= self.max_depth: # if the depth is greater than or equal to the max_depth
            node['left'] = self.term_node(l_node) # set the left node equal to the terminal_node on the left_node
            node['right'] = self.term_node(r_node) # set the right node equal to the terminal_node ob the right_node
            return

        if len(l_node) <= self.min_splits: # if the length of the left_node is less than or equal to the min_splits
            node['left'] = self.terminal_node(l_node) # set the left node equal to the terminal_node on the left_node
        else: # else
            node['left'] = self.best_split(l_node) # set the left node equal to the best_split on the left_node
            self.rec_split(node['left'],depth + 1) # split_branch on the left node with depth and 1

        if len(r_node) <= self.min_splits: # if the length of the right is less than or equal to the min_splits
            node['right'] = self.terminal_node(r_node) # set the right node equal to the terminal_node on the right_node
        else:
            node['right'] = self.best_split(r_node) # set the right node equal to the best_split of the right_node
            self.rec_split(node['right'],depth + 1) # split_branch on the right node with depth and 1
    """
    ### Build Tree: ###
    Build the tree starts at the root node, then uses the best split on itself recursively to construct the entire tree.
    """
    def build_tree(self): # build tree method
        self.root = self.best_split(self.train_data) # set the root equal to the best_split on the train_data
        self.rec_split(self.root, 1) # split_branch on the root with 1
        return self.root  # return the root
    """
    ### Predict: node, row ###
    Node prediction checks if the node is either a terminal value to be returned as the prediction, or if it is a dictionary
    node containing another level to be checked.
    """
    def pred_(self, node, row): # predict method
        if row[node['index']] < node['val']: # if the row node index is less tha nthe node val
            if isinstance(node['left'], dict): # if the node left is dictionary
                return self.pred_(node['left'], row) # return the _predict of the node left and row
            else: # else
                return node['left'] # return the node left

        else: # else
            if isinstance(node['right'],dict): # if the node right is dictionary
                return self.pred_(node['right'],row) # return the _predict of the node right and row
            else: # else
                return node['right'] # return the node right

    def pred(self, test_data): # predict method
        self.pred_label = np.array([]) # set the predicted_label to an empty array
        for i in test_data: # for loop, idx in test_data
            self.pred_label = np.append(self.pred_label, self.pred_(self.root,i)) # append the predicted_label and _predict of the root with idx to the predicted_label

        return self.pred_label # return the predicted_label
