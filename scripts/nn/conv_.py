import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch
import pandas as pd
import numpy as np
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        # self.norm = nn.BatchNorm2d(1)
        self.conv1 = nn.Conv2d(1, 32, 7)
        self.conv2 = nn.Conv2d(32, 64, 7)

        self.conv3 = nn.Conv2d(64, 256, 7)
        self.conv4 = nn.Conv2d(256, 128, 7)

        self.conv5 = nn.Conv2d(128, 512, 7)
        self.conv6 = nn.Conv2d(512, 32, 7)

        self.fc1 = nn.Linear(6272, 1)
        # self.fc2 = nn.Linear(100, 1)
        self.dropout1 = nn.Dropout(0.25)
        # self.dropout2 = nn.Dropout(0.3)
        # self.dropout3 = nn.Dropout(0.3)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = F.max_pool2d(x, (2, 2))
        # x = self.dropout1(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = F.max_pool2d(x, (2, 2))
        # x = self.dropout2(x)
        x = self.conv5(x)
        x = self.conv6(x)
        x = F.max_pool2d(x, (2, 2))
        # x = self.dropout3(x)

        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = self.dropout1(x)
        x = F.sigmoid(x)
        return x


column = 'height_dtm'

df = pd.read_pickle('../save.pkl').reset_index()

def normalize(row):
    height = row[column]
    nans = height>1000
    height[nans] = np.nan
    height = (height-np.nanmean(height))/np.nanstd(height)
    height[np.isnan(height)] = 3
    return height

def reshape(arr):
    result = np.reshape(arr[column], (1,200,200))
    return result

df[column] = df.apply(normalize, axis=1)
df[column] = df.apply(reshape, axis=1)


Y = np.asarray(df['target'])
X = np.asarray(df[column].values.tolist())


accs = []
for d in range(20):
    trn_x,val_x,trn_y,val_y = train_test_split(X,Y,test_size=0.10)

    trn_x_torch = torch.from_numpy(trn_x).type(torch.FloatTensor)
    trn_y_torch = torch.from_numpy(trn_y).type(torch.FloatTensor)

    val_x_torch = torch.from_numpy(val_x).type(torch.FloatTensor)
    val_y_torch = torch.from_numpy(val_y).type(torch.FloatTensor)

    trn = TensorDataset(trn_x_torch,trn_y_torch)
    val = TensorDataset(val_x_torch,val_y_torch)


    trn_dataloader = torch.utils.data.DataLoader(trn,batch_size=64,shuffle=False, num_workers=0)
    val_dataloader = torch.utils.data.DataLoader(val,batch_size=64,shuffle=False, num_workers=0)

    def binary_acc(y_pred, y_test):
        y_pred_tag = torch.round(y_pred)

        correct_results_sum = (y_pred_tag == y_test).sum().float()
        acc = correct_results_sum/y_test.shape[0]
        acc = torch.round(acc * 100)
        
        return acc




    net = Net().to(device)
    criterion = nn.BCELoss()

    optimizer = optim.Adam(net.parameters(), lr=0.0002)


    print(net)
    for epoch in range(1500):  # loop over the dataset multiple times
        total_loss = 0
        val_loss_total = 0
        count = 0
        count_val = 0
        running_loss = 0.0
        for i, data in enumerate(trn_dataloader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data

            inputs = inputs.to(device)
            labels = labels.to(device)

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels.unsqueeze(1))
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            acc = binary_acc(outputs, labels.unsqueeze(1))
            total_loss += loss.item()
            count += 1

            # val_loss

        with torch.no_grad():
            for X_batch,y in val_dataloader:
                inputs = X_batch.to(device)
                labels = y.to(device)

                # forward + backward + optimize
                outputs = net(inputs)
                loss = criterion(outputs, labels.unsqueeze(1))
                val_loss_total += loss.item()
                count_val +=1



        avg_loss_train = total_loss/count
        avg_val_loss = val_loss_total/count_val


        print("train_loss: {}, val_loss: {}".format(avg_loss_train, avg_val_loss))

    print('Finished Training')

    y_pred_list = []
    y_truth = []
    net.eval()
    with torch.no_grad():
        for X_batch,y in val_dataloader:
            X_batch = X_batch.to(device)
            y_test_pred = net(X_batch)
            y_test_pred = y_test_pred
            y_pred_tag = torch.round(y_test_pred)
            y_pred_list.append(y_pred_tag.cpu().numpy())
            y_truth.append(y.cpu().numpy())

    y_pred_list = [a.squeeze().tolist() for a in y_pred_list]
    y_truth = [a.squeeze().tolist() for a in y_truth]


    cm = (confusion_matrix(val_y_torch, y_pred_list))
    print(cm)


    print(classification_report(val_y_torch, y_pred_list))
    accurac = (cm[0,0]+cm[1,1])/(np.sum(cm))
    print(accurac)
    accurac2 = 1-np.mean(np.absolute(np.asarray(y_pred_list)-np.asarray(y_truth)))
    # print(accurac2)
    accs.append(accurac)

print(accs)

