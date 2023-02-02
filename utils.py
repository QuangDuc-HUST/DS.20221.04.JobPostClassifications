import os
import json
import shutil

from sklearn.metrics import f1_score, confusion_matrix

import torch


def get_training_device(display=True):
    """Get the training device
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if display:
        print("We are on", device, "..")

    return device

def to_device(vari, device, **kwargs):
    """
    Get the variable to device even if this is a collection of tensor
    """

    if isinstance(vari, dict):
        for key in vari.keys():
            vari[key] = vari[key].to(device, **kwargs)   
        return vari

    elif isinstance(vari, list):
        new_vari = []
        for ten in vari:
          new_vari.append(ten.to(device, **kwargs))
        
        return new_vari

    return vari.to(device, **kwargs)



def get_eval_metrics(preds_label, targets):  

    """Get F1 Score and Confusion Matrix
    
    return and display (f1_score, confusion_matrix_numpy) 

    """

    f1_result =  f1_score(targets, preds_label, average='macro')

    cfm_result = confusion_matrix(targets, preds_label)

    print('-' * 20)
    print(f"F1 Score {f1_result:0.5f}")
    print("Confusion matrix")
    print(cfm_result)   # Display option

    print('-' * 20)

    return f1_result, cfm_result


def load_checkpoint(checkpoint, model, optimizer=None, **kwargs):
    """Loads model parameters (state_dict) from file_path. If optimizer is provided, loads state_dict of
    optimizer assuming it is present in checkpoint.
    Args:
        checkpoint: (string) filename which needs to be loaded
        model: (torch.nn.Module) model for which the parameters are loaded
        optimizer: (torch.optim) optional: resume optimizer from checkpoint
    """

    if not os.path.exists(checkpoint):
        raise("File doesn't exist {}".format(checkpoint))

    print(f"Load checkpoint from {checkpoint}")

    checkpoint = torch.load(checkpoint, **kwargs)

    model.load_state_dict(checkpoint['state_dict'],)  # maybe epoch as well

    if optimizer:
        optimizer.load_state_dict(checkpoint['optim_dict'])

    return checkpoint



def get_idx2label(json_file_path=os.path.join("idx2label", "job_type_idx2label.json")):

    with open(json_file_path) as f:
        idx2label = json.load(f)

    converted_idx2label = {}

    for idx, label in idx2label.items():
        converted_idx2label[int(idx)] = label

    return converted_idx2label