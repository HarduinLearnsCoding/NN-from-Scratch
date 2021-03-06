import numpy as np
import collections.abc

# Don't modify this code block!


class Data:
    """Stores an input array of training data, and hands it to the next layer."""

    def __init__(self, data):
        self.data = data
        # self.out_dims is the shape of the output of this layer
        self.out_dims = data.shape

    def set_data(self, data):
        self.data = data

    def forward(self):
        return self.data

    def backward(self, dwnstrm):
        pass


class Linear:
    """Given an input matrix X, with one feature vector per row,
    this layer computes XW, where W is a linear operator."""

    def __init__(self, in_layer, num_out_features):
        assert len(
            in_layer.out_dims) == 2, "Input layer must contain a list of 1D linear feature data."

        self.in_layer = in_layer
        num_data, num_in_features = in_layer.out_dims

        # TODO: Set out_dims to the shape of the output of this linear layer as a numpy array e.g. self.out_dims = np.array([x, y])
        self.out_dims = np.array([num_data, num_out_features])

        # TODO: Declare the weight matrix. Be careful how you initialize the matrix.

        self.W = np.random.randn(
            num_in_features, num_out_features) / np.sqrt(num_in_features)

    def forward(self):
        """This function computes XW"""
        self.in_array = self.in_layer.forward()

        # TODO: Compute the result of linear layer with weight W, and store it as self.out_array
        self.out_array = self.in_array @ self.W

        return self.out_array

    def backward(self, dwnstrm):

        #  TODO: Compute the gradient of the loss with respect to W, and store it as G

        self.G = self.in_array[:, :, None] * dwnstrm[:, None]

    #     TODO: Compute grad of loss with respect to inputs, and hand this gradient backward to the layer behind

        # input_grad = dwnstrm @ np.transpose(self.W)

        input_grad = self.W @ dwnstrm[:, :, None]

        input_grad = input_grad.squeeze(axis=-1)

    #     hand this gradient backward to the layer behind
        self.in_layer.backward(input_grad)


class Relu:
    """Given an input matrix X, with one feature vector per row,
    this layer computes maximum(X,0), where the maximum operator is coordinate-wise."""

    def __init__(self, in_layer):
        self.in_layer = in_layer
        self.in_dims = in_layer.out_dims

        # TODO: Set out_dims to the shape of the output of this relu layer as a numpy array e.g. self.out_dims = np.array([...])
        self.out_dims = self.in_dims

    def forward(self):
        self.in_array = self.in_layer.forward()

        # TODO: Compute the result of Relu function, and store it as self.out_array
        self.out_array = np.maximum(self.in_array, 0)
        return self.out_array

    def backward(self, dwnstrm):

        # TODO: Compute grad of loss with respect to inputs, and hand this gradient backward to the layer behind

        input_grad = dwnstrm * (self.in_array > 0).astype(int)

        # hand this gradient backward to the layer behind
        self.in_layer.backward(input_grad)
        pass
    pass


class Bias:
    """Given an input matrix X, add a trainable constant to each entry."""

    def __init__(self, in_layer):
        self.in_layer = in_layer
        num_data, num_in_features = in_layer.out_dims
        # TODO: Set out_dims to the shape of the output of this linear layer as a numpy array.
        self.out_dims = np.array([num_data, num_in_features])
        # TODO: Declare the weight matrix. Be careful how you initialize the matrix.
        self.W = np.random.randn(1, num_in_features)

    def forward(self):
        self.in_array = self.in_layer.forward()
        # TODO: Compute the result of Bias layer, and store it as self.out_array
        self.out_array = self.in_array + self.W
        return self.out_array

    def backward(self, dwnstrm):
        # TODO: Compute the gradient of the loss with respect to W, and store it as G

        self.G = dwnstrm

        # TODO: Compute grad of loss with respect to inputs, and hand this gradient backward to the layer behind
        input_grad = dwnstrm
        # hand this gradient backward to the layer behind
        self.in_layer.backward(input_grad)
        pass
    pass


class SquareLoss:
    """Given a matrix of logits (one logit vector per row), and a vector labels,
    compute the sum of squares difference between the two"""

    def __init__(self, in_layer, labels):
        self.in_layer = in_layer
        self.labels = labels

    def set_data(self, labels):
        self.labels = labels

    def forward(self):
        """Loss value is (1/2M) || X-Y ||^2"""
        self.in_array = self.in_layer.forward()
        self.num_data = self.in_array.shape[0]

        # TODO: Compute the result of mean squared error, and store it as self.out_array
        self.out_array = (np.linalg.norm(
            self.in_array - self.labels)**2) / (2 * self.num_data)

        return self.out_array

    def backward(self):
        """Gradient is (1/M) (X-Y), where N is the number of training samples"""

        # TODO: Compute grad of loss with respect to inputs, and hand this gradient backward to the layer behind
        self.pass_back = (self.in_array - self.labels) / self.num_data

        # hand this gradient backward to the layer behind
        self.in_layer.backward(self.pass_back)
        pass
    pass


class Sigmoid:

    # FIX NUMERICAL STABILITY

    def __init__(self, in_layer):
        self.in_layer = in_layer

    def forward(self):
        self.in_array = self.in_layer.forward()

        # TODO: Compute the result of sigmoid function, and store it as self.out_array. Be careful! Don't exponentiate an arbitrary positive number as it may overflow.
        self.out_array = 1 / (1 + np.exp(-self.in_array))

        return self.out_array

    def backward(self, dwnstrm):
        # TODO: Compute grad of loss with respect to inputs, and hand this gradient backward to the layer behind. Be careful! Don't exponentiate an arbitrary positive number as it may overflow.

        # Stability

        input_grad = dwnstrm * np.exp(-1 * (np.maximum(self.in_array, 0))) / (
            (1 + np.exp(-self.in_array)) * (1 + np.exp(-np.abs(self.in_array))))

        self.in_layer.backward(input_grad)


class CrossEntropy:

    def __init__(self, in_layer, labels):
        self.in_layer = in_layer
        self.labels = labels
        pass

    def set_data(self, labels):
        self.labels = labels

    def forward(self):
        self.in_array = self.in_layer.forward()
        self.num_data = self.in_array.shape[0]
       # TODO: Compute the result of cross entropy loss, and store it as self.out_array

        self.out_array = -(1 / self.num_data) * (np.log(self.in_array) * self.labels + (1 -
                                                                                        self.labels) * np.log(1 - self.in_array)).sum()
        return self.out_array

    def backward(self):
        # TODO: Compute grad of loss with respect to inputs, and hand this gradient backward to the layer behind
        input_grad = (1 / self.num_data) * ((1 - self.labels) / (1 - self.in_array) -
                                            (self.labels / self.in_array))

        self.in_layer.backward(input_grad)


class CrossEntropySoftMax:
    """Given a matrix of logits (one logit vector per row), and a vector labels,
    compute the cross entropy of the softmax.
    The labels must be a 1d vector"""

    def __init__(self, in_layer, labels=None):
        self.in_layer = in_layer
        # you don't have to pass labels if it is not known at class construction time. (e.g. if you plan to do mini-batches)
        if labels is not None:
            self.set_data(labels)

    def set_data(self,  labels):
        self.labels = labels
        self.ones_hot = np.zeros((labels.shape[0], labels.max() + 1))
        self.ones_hot[np.arange(labels.shape[0]), labels] = 1

    def forward(self):
        self.in_array = self.in_layer.forward()
        self.num_data = self.in_array.shape[0]
        # TODO: Compute the result of softmax + cross entropy, and store it as self.out_array. Be careful! Don't exponentiate an arbitrary positive number as it may overflow.

        element_max = self.in_array.max(axis=-1, keepdims=True)
        temp = element_max.squeeze(
            axis=-1) + np.log(np.exp(self.in_array - element_max).sum(axis=-1))
        self.out_array = (1 / self.num_data) * (
            (- (self.in_array * self.ones_hot).sum(axis=-1)) + temp).sum()

        return self.out_array

    def backward(self):
        # TODO: Compute grad of loss with respect to inputs, and hand this gradient backward to the layer behind. Be careful! Don't exponentiate an arbitrary positive number as it may overflow.
        element_max_back = self.in_array.max(axis=-1, keepdims=True)
        softmax_num = np.exp(self.in_array - element_max_back)
        softmax_out = softmax_num / softmax_num.sum(axis=-1, keepdims=True)
        input_grad = (softmax_out - self.ones_hot) / self.num_data
        self.in_layer.backward(input_grad)


class SGDSolver:
    def __init__(self, lr, modules):
        self.lr = lr
        self.modules = modules

    def step(self):
        for m in self.modules:
            # TODO: Update the weights of each module (m.W) with gradient descent. Hint1: remember we store the gradients for each layer in self.G during backward pass. Hint2: we can update gradient in place with -= or += operator.

            m.W -= (self.lr) * np.mean(m.G, axis=0)


def is_modules_with_parameters(value):
    return isinstance(value, Linear) or isinstance(value, Bias)

# DO NOT CHANGE ANY CODE IN THIS CLASS!


class ModuleList(collections.abc.MutableSequence):
    def __init__(self, *args):
        self.list = list()
        self.list.extend(list(args))
        pass

    def __getitem__(self, i):
        return self.list[i]

    def __setitem__(self, i, v):
        self.list[i] = v

    def __delitem__(self, i):
        del self.list[i]
        pass

    def __len__(self):
        return len(self.list)

    def insert(self, i, v):
        self.list.insert(i, v)
        pass

    def get_modules_with_parameters(self):
        modules_with_parameters = []
        for mod in self.list:
            if is_modules_with_parameters(mod):
                modules_with_parameters.append(mod)
                pass
            pass
        return modules_with_parameters
    pass


class BaseNetwork:
    def __init__(self):
        super().__setattr__("initialized", True)
        super().__setattr__("modules_with_parameters", [])
        super().__setattr__("output_layer", None)

    def set_output_layer(self, layer):
        super().__setattr__("output_layer", layer)
        pass

    def get_output_layer(self):
        return self.output_layer

    def __setattr__(self, name, value):
        if not hasattr(self, "initialized") or (not self.initialized):
            raise RuntimeError(
                "You must call super().__init__() before assigning any layer in __init__().")
        if is_modules_with_parameters(value) or isinstance(value, ModuleList):
            self.modules_with_parameters.append(value)
            pass

        super().__setattr__(name, value)
        pass

    def get_modules_with_parameters(self):
        modules_with_parameters_list = []
        for mod in self.modules_with_parameters:
            if isinstance(mod, ModuleList):

                modules_with_parameters_list.extend(
                    mod.get_modules_with_parameters())
                pass
            else:

                modules_with_parameters_list.append(mod)
                pass
            pass
        return modules_with_parameters_list

    def forward(self):
        return self.output_layer.forward()

    def backward(self, input_grad):
        self.output_layer.backward(input_grad)
        pass

    def state_dict(self):
        all_params = []
        for m in self.get_modules_with_parameters():
            all_params.append(m.W)
            pass
        return all_params

    def load_state_dict(self, state_dict):
        assert len(state_dict) == len(self.get_modules_with_parameters())
        for m, lw in zip(self.get_modules_with_parameters(), state_dict):
            m.W = lw
            pass
        pass
    pass
