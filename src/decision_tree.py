import random
import operator

class Decision_Tree_Node:

    def __init__(self, index, value, op_index):
        self.index = index
        self.value = value
        self.op_index = op_index

    def decide(self, data_point, operators):
        return operators[self.op_index](data_point[self.index], self.value)
    
class Decision_Tree:
    def __init__(self, operators):
        self.operators = operators
        self.root = None

    def learn(self, data):
        """Build a decision tree from training data.
        
        Args:
            data: List of data points where each point is [class_label, feature1, feature2, ...]
        """
        if not data:
            return None
        
        self.root = self._build_tree(data)
        return self.root
    
    def _build_tree(self, data):
        """Recursively build the decision tree.
        
        Args:
            data: Subset of training data for this node
            
        Returns:
            Decision_Tree_Node or class label (leaf node)
        """
        if not data:
            return None
        
        # Check if all data points have the same class (pure node)
        classes = [point[0] for point in data]
        if len(set(classes)) == 1:
            return classes[0]  # Return class label as leaf
        
        # If only one data point or no features, return majority class
        if len(data) == 1 or len(data[0]) == 1:
            return max(set(classes), key=classes.count)
        
        # Find the best split
        best_split = self._find_best_split(data)
        
        if best_split is None:
            # No good split found, return majority class
            return max(set(classes), key=classes.count)
        
        index, value, op_index = best_split
        
        # Create decision node
        node = Decision_Tree_Node(index, value, op_index)
        
        # Split data based on the decision
        op = self.operators[op_index]
        left_data = [point for point in data if op(point[index], value)]
        right_data = [point for point in data if not op(point[index], value)]
        
        # If split doesn't separate data, return majority class
        if not left_data or not right_data:
            return max(set(classes), key=classes.count)
        
        # Recursively build subtrees
        node.left = self._build_tree(left_data)
        node.right = self._build_tree(right_data)
        
        return node
    
    def _find_best_split(self, data):
        """Find the best split point using information gain or similar metric.
        
        Args:
            data: Training data subset
            
        Returns:
            Tuple of (feature_index, threshold_value, operator) or None
        """
        if len(data[0]) <= 1:  # No features
            return None
        
        best_gain = -1
        best_split = None
        num_features = len(data[0]) - 1  # Exclude class label
        
        # Try each feature
        for feature_idx in range(1, len(data[0])):
            # Get unique values for this feature
            values = sorted(set(point[feature_idx] for point in data))
            
            # Try split points between consecutive values
            for i in range(len(values) - 1):
                threshold = (values[i] + values[i + 1]) / 2
                
                # Try each operator
                for op_idx, op in enumerate(self.operators):
                    # Split data
                    left = [point for point in data if op(point[feature_idx], threshold)]
                    right = [point for point in data if not op(point[feature_idx], threshold)]
                    
                    # Skip if split doesn't separate data
                    if not left or not right:
                        continue
                    
                    # Calculate information gain
                    gain = self._information_gain(data, left, right)
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_split = (feature_idx, threshold, op_idx)
        
        return best_split
    
    def _information_gain(self, parent, left, right):
        """Calculate information gain of a split.
        
        Args:
            parent: Parent dataset
            left: Left child dataset
            right: Right child dataset
            
        Returns:
            Information gain value
        """
        def entropy(data):
            if not data:
                return 0
            classes = [point[0] for point in data]
            class_counts = {}
            for c in classes:
                class_counts[c] = class_counts.get(c, 0) + 1
            
            total = len(data)
            ent = 0
            for count in class_counts.values():
                if count > 0:
                    prob = count / total
                    ent -= prob * (prob and (prob * 0.69314718056 + 0) or 0)  # log2 approximation
            return ent
        
        parent_entropy = entropy(parent)
        n = len(parent)
        n_left = len(left)
        n_right = len(right)
        
        weighted_child_entropy = (n_left / n) * entropy(left) + (n_right / n) * entropy(right)
        
        return parent_entropy - weighted_child_entropy
    
    def predict(self, data_point):
        """Predict class for a single data point.
        
        Args:
            data_point: Feature vector (without class label)
            
        Returns:
            Predicted class label
        """
        # Add placeholder for class label at index 0 to match training data format
        data_with_placeholder = [None] + list(data_point)
        return self._predict_recursive(self.root, data_with_placeholder)
    
    def _predict_recursive(self, node, data_point):
        """Recursively traverse tree to make prediction."""
        # Leaf node
        if not isinstance(node, Decision_Tree_Node):
            return node
        
        # Decision node
        if node.decide(data_point, self.operators):
            return self._predict_recursive(node.left, data_point)
        else:
            return self._predict_recursive(node.right, data_point)

n = 30
classes = 5
d = 4
data = [ ['class' + str(random.randrange(classes))] + 
        [random.random() for _ in range(d)] for _ in range(n) ]

operators = [
    operator.lt,
    lambda x, y: x**2 < y**2,
    lambda x, y: x%0.1 < y%0.1
]

decision_tree = Decision_Tree(operators)
decision_tree.learn(data)

# Test predictions
print("Training data:")
for i, point in enumerate(data):
    prediction = decision_tree.predict(point[1:])  # Predict without class label
    actual = point[0]
    print(f"{i:3} class={point[0]}, {prediction == actual}")
print('done')