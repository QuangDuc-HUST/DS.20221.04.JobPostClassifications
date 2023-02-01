
from sklearn.metrics import f1_score, confusion_matrix

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
    