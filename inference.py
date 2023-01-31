
import torch

from transformers import logging
logging.set_verbosity_error()

from model import BERTJob

import utils
import preprocess


def predict(input_dict, weight_path, **kwargs):
    """
    Input:

    input_dict: dictionary like input_dict = {"description" : "duc dep trai", "title": "hehe", "salary": 100000, ...}

    Only predict on CPU
    
    """

    NUM_CLASSES = 37
    MAX_LEN = 125


    model = BERTJob(num_classes=NUM_CLASSES, **kwargs)

    utils.load_checkpoint(weight_path, model, map_location=torch.device('cpu'))

    features = preprocess.process_input(input_dict, MAX_LEN)

    model.eval()

    with torch.no_grad():   
        
        logit = model(features).squeeze()
        output = torch.softmax(logit, dim=0)
    
    return output.detach().cpu().numpy()


if __name__ == '__main__':
    test_input_description_only = {"description": "- Am hiểu phần mềm Misa - Ưu tiên các ứng viên mới ra trường , chịu khó , có đào tạo thêm nghiệp vụ chuyên môn - Làm việc toàn thời gian tại công ty , môi trường thông thoáng - Thành thạo  nghiệp vụ kế toán tổng hợp - Ưu tiên nhà ở Củ Chi hoặc Hóc Môn để tiện di chuyển - Chế độ làm việc rõ ràng , chăm sóc đời sống nhân viên và gia đình"}
    output = predict(test_input_description_only, 'weights/BERTweights.pth')

    idx2label = utils.get_idx2label()

    print(output, output.argmax(), idx2label[output.argmax()])