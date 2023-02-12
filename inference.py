from transformers import logging
from model import PhoBertModel, ComPhoBERTModel
from config import Config
import os
import torch
import utils
import preprocess
logging.set_verbosity_error()


def predict(input_dict, weight_folder, config_file, **kwargs):
    """
    Input:

    input_dict: dictionary like input_dict = {"description" : "duc dep trai", "title": "hehe", "salary": 100000, ...}

    Only predict on CPU

    """

    config = Config(config_file)

    processed_text_field, processed_numeric_field = preprocess.process_input(input_dict, config("MAX_LEN"))

    if processed_numeric_field is None:

        model = PhoBertModel(num_classes=config("NUM_CLASSES"), **kwargs)

        weight_path = os.path.join(weight_folder, "BERTweights.pth")

        features = processed_text_field

    else:

        in_dimension = processed_numeric_field.shape[1]

        model = ComPhoBERTModel(in_dimensions=in_dimension,
                                dense_size=config("DENSE_SIZE_COM"),
                                num_classes=config("NUM_CLASSES"),
                                **kwargs)

        weight_path = os.path.join(weight_folder, "COMBERTweights.pth")

        features = processed_text_field, processed_numeric_field

    utils.load_checkpoint(weight_path, model, map_location=torch.device('cpu'))

    model.eval()

    with torch.no_grad():

        logit = model(features).squeeze()

        output = torch.softmax(logit, dim=0)

    return output.detach().cpu().numpy()


if __name__ == '__main__':
    test_input = {
        "description": "- Am hiểu phần mềm Misa - Ưu tiên các ứng viên mới ra trường , chịu khó , có đào tạo thêm nghiệp vụ chuyên môn - Làm việc toàn thời gian tại công ty , môi trường thông thoáng - Thành thạo  nghiệp vụ kế toán tổng hợp - Ưu tiên nhà ở Củ Chi hoặc Hóc Môn để tiện di chuyển - Chế độ làm việc rõ ràng , chăm sóc đời sống nhân viên và gia đình",
        "title": "cần tuyển kế toán liên hệ gấp 0354191503"}

    test_input_2 = {'title': 'Nhân Viên Tư Vấn Tuyển Sinh',
                    'description': '- Tìm kiếm, xây dựng & phát triển nguồn khách hàng tiềm năng\n- Ghi nhận và tìm hiểu nhu cầu của học viên theo quy trình tư vấn\n- Tư vấn chương trình đào tạo phù hợp\n- Theo dõi tình hình học tập của học viên và thực hiện các dịch vụ chăm sóc học viên\n- Ghi nhận, xử lý và báo cáo với cấp quản lý trực tiếp về các phát sinh liên quan đến học viên/ phụ huynh\n- Thông báo cho học viên và phụ huynh các hoạt động ngoại khóa, hội thảo và thông tin du học nhằm thu hút học viên mới và chăm sóc học viên đang học',
                    'min_salary': 8000000,
                    'max_salary': 10000000,
                    'age_range': '20-',
                    'gender': 'Nữ',
                    'benefits': 'Phụ cấp, tham gia BHXH, tăng lương',
                    'job_location': 'Xã An Ninh Đông, Huyện Đức Hòa, Long An',
                    'salary_type': 'Theo tháng',
                    'region': 'Long An',
                    'skills': 'Không yêu cầu',
                    'contract_type': 'Làm theo ca',
                    'education_requirements': 'Cấp 3',
                    'experience_requirements': '< 1 năm'
                    }

    output = predict(test_input_2, 'weights/', "config.json")

    idx2label = utils.get_idx2label()

    print(output, output.argmax(), idx2label[output.argmax()])
