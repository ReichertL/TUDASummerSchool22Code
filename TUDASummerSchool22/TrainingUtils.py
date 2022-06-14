from torch.nn.functional import cross_entropy
import torch
import torch.nn as nn
import time
from TUDASummerSchool22.Utils import *
from TUDASummerSchool22.ModelUtils import *

def train_benign_client(global_model_state_dict, local_model, local_training_data, COMPUTATION_DEVICE, local_epochs, lr=0.2, printing_prefix='', ):

    local_model.copy_params(global_model_state_dict)
    
    local_model.train()
    local_model.requires_grad_(True)
    optimizer = torch.optim.SGD(local_model.parameters(), lr=lr, momentum=0.9, weight_decay=0.0005)
    
    start_time = time.time()
    
    local_training_data = [(data.to(COMPUTATION_DEVICE), targets.to(COMPUTATION_DEVICE)) for data, targets in local_training_data]

    for local_epoch in range(local_epochs):
        
        epoch_loss = 0
        for batch_id, (data, targets) in enumerate(local_training_data):
            optimizer.zero_grad()
            output = local_model(data)
            loss = nn.functional.cross_entropy(output, targets)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.detach().cpu()

        epoch_loss = float(epoch_loss)
        elapsed = time.time() - start_time
        # lr: learning rate
        print_timed(f'{printing_prefix}local_epoch {local_epoch:3d}'
                    f' | lr {lr} | ms/batch {elapsed * 1000:5.2f}'
                    f'| loss {epoch_loss:5.2f}')
        start_time = time.time()
    trained_local_weights = {name: param.detach().cpu() for name, param in local_model.state_dict().items()}    
    local_training_data = [(data.cpu(), targets.cpu()) for data, targets in local_training_data]
    return trained_local_weights

def train_malicious_client(global_model_state_dict, local_model, local_training_data, COMPUTATION_DEVICE, local_epochs, NAMES_OF_AGGREGATED_PARAMETERS,
                           lr=0.2, printing_prefix='', alpha=0.6,):

    local_model.copy_params(global_model_state_dict)
    
    local_model.train()
    local_model.requires_grad_(True)
    optimizer = torch.optim.SGD(local_model.parameters(), lr=lr, momentum=0.9, weight_decay=0.0005)
    
    start_time = time.time()
    
    local_training_data = [(data.to(COMPUTATION_DEVICE), targets.to(COMPUTATION_DEVICE)) for data, targets in local_training_data]

    for local_epoch in range(local_epochs):
        
        epoch_loss = 0
        for batch_id, (data, targets) in enumerate(local_training_data):
            optimizer.zero_grad()
            output = local_model(data)
            class_loss = nn.functional.cross_entropy(output, targets)
            ### IMPLEMENTATION START ###
            loss = class_loss
            anomaly_evasion_loss = model_dist_norm(global_model_state_dict, local_model.state_dict(), NAMES_OF_AGGREGATED_PARAMETERS)
            loss = alpha * class_loss + (1-alpha) * anomaly_evasion_loss
            ### IMPLEMENTATION END ###
            loss.backward()
            optimizer.step()
            epoch_loss += loss.detach().cpu()

        epoch_loss = float(epoch_loss)
        elapsed = time.time() - start_time
        print_timed(f'{printing_prefix}local_epoch {local_epoch:3d}'
                    f' | lr {lr} | ms/batch {elapsed * 1000:5.2f}'
                    f'| loss {epoch_loss:5.2f}')
        start_time = time.time()
    trained_local_weights = {name: param.detach().cpu() for name, param in local_model.state_dict().items()}    
    local_training_data = [(data.cpu(), targets.cpu()) for data, targets in local_training_data]
    return trained_local_weights