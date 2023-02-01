import os
import time

import shutil
import torch

from tqdm.notebook import tqdm


class RunningAverage():

    """A simple class that maintains the running average of a quantity
    Example:
    ```
    loss_avg = RunningAverage()
    loss_avg.update(2)
    loss_avg.update(4)
    loss_avg() = 3
    ```
    """

    def __init__(self):
        self.steps = 0
        self.total = 0

    def update(self, val):
        self.total += val
        self.steps += 1

    def __call__(self):
        return self.total / float(self.steps)


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
          new_vari.append(to_device(ten, device,  **kwargs))
        return new_vari

    return vari.to(device, **kwargs)


def save_checkpoint(state, is_best, checkpoint):
    """Saves model and training parameters at checkpoint + 'last.pth'. If is_best==True, also saves
    checkpoint + 'best.pth'
    Args:
        state: (dict) contains model's state_dict, may contain other keys such as epoch, optimizer state_dict
            (epoch, state_dict, optimizer)
        is_best: (bool) True if it is the best model seen till now
        checkpoint: (string) folder where parameters are to be saved
    """
    file_path = os.path.join(checkpoint, 'last.pth')

    if not os.path.exists(checkpoint):
        print("Checkpoint Directory does not exist! Making directory {}".format(checkpoint))
        os.makedirs(checkpoint)

    print(f"Saving checkpoint...")
    torch.save(state, file_path)

    if is_best:
        shutil.copyfile(file_path, os.path.join(checkpoint, 'best.pth'))


def load_checkpoint(checkpoint, model, optimizer=None):
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

    checkpoint = torch.load(checkpoint)

    model.load_state_dict(checkpoint['state_dict'])  # maybe epoch as well

    if optimizer:
        optimizer.load_state_dict(checkpoint['optim_dict'])

    return checkpoint



def train_model(model, device, train_dataloader, val_dataloader, metrics, criteria, optimizer, num_epochs, checkpoint_dir, scheduler=None):

    start_training_time = time.time()    

    model.to(device) 

    best_f1_metric = 0
    best_cf_metric = None

    for epoch in range(num_epochs):
        
        print(f"Training epoch {epoch + 1} ...")

        model.train()

        loss_train_avg = RunningAverage()

        with tqdm(total=len(train_dataloader)) as t:
            for step, batch in enumerate(train_dataloader):

                x_batch, label_batch = batch
                x_batch = to_device(x_batch, device, non_blocking=True)
                label_batch = to_device(label_batch, device, non_blocking=True)

                y_pred = model(x_batch) 

                loss = criteria(y_pred, label_batch)

                loss.backward()

                optimizer.step()

                if scheduler is not None:
                  scheduler.step()

                optimizer.zero_grad()

                loss_train_avg.update(loss.item())

                t.set_postfix(loss='{:05.3f}'.format(loss_train_avg()))
                t.update()
        
        # Evaluate step

        print(f"Evaluating ...")

        model.eval()

        loss_val_sum = 0
        preds_list = []
        label_list = []

        with torch.no_grad():
            with tqdm(total=len(val_dataloader)) as t:
                for step, batch in enumerate(val_dataloader):

                    x_batch, label_batch = batch

                    x_batch = to_device(x_batch, device, non_blocking=True)
                    label_batch = to_device(label_batch, device, non_blocking=True)

                    # forward
                    y_pred = model(x_batch) 

                    loss = criteria(y_pred, label_batch)

                    loss_val_sum += loss.item()

                    y_pred_label = list(y_pred.argmax(1).detach().cpu().numpy())

                    label_batch = list(label_batch.detach().cpu().numpy())

                    preds_list.extend(y_pred_label)
                    label_list.extend(label_batch)


                    t.update()
                    
                
                f1_score, cfm = metrics(preds_list, label_list)

                t.set_postfix(loss='{:05.3f}'.format(loss_val_sum / len(val_dataloader)))
                

                is_best = f1_score > best_f1_metric
                if is_best:
                    best_f1_metric = f1_score
                    best_cf_metric = cfm
                    print("- Found new best accuracy performance")
                
                if checkpoint_dir:
                    save_checkpoint({
                                     'state_dict': model.state_dict(),
                                     },
                                      is_best=is_best,
                                      checkpoint=checkpoint_dir)


    print("----- DONE ------")

    training_time = time.time() - start_training_time

    print(f'Time to train: {training_time} second(s)')

    return training_time, best_f1_metric, best_cf_metric


def evaluate_model(model_architecure, state_file, device, dataloader, metrics):


    print(f"Evaluating on test set ...")
  
    
    eval_model = model_architecure

    load_checkpoint(state_file, eval_model)

    eval_model.to(device)

    eval_model.eval()


    preds_list = []
    label_list = []

    start_inference_time = time.time()    

    with torch.no_grad():
        with tqdm(total=len(dataloader)) as t:
            for step, batch in enumerate(dataloader):

                x_batch, label_batch = batch

                x_batch = to_device(x_batch, device, non_blocking=True)
                label_batch = to_device(label_batch, device, non_blocking=True)

                # forward
                y_pred = eval_model(x_batch) 

                y_pred_label = list(y_pred.argmax(1).detach().cpu().numpy())

                label_batch = list(label_batch.detach().cpu().numpy())

                preds_list.extend(y_pred_label)
                label_list.extend(label_batch)

                t.update()
                
            
            inference_time = time.time() - start_inference_time

            f1_score, cfm = metrics(preds_list, label_list)
            

    print("----- DONE ------")


    print(f'Time to predict: {inference_time} second(s)')


    return inference_time, f1_score, cfm