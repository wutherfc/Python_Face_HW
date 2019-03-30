import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import func
import cv2
import base64


#内部函数
def print_error(req_dict):
    """
    判断api调用是否出错，若出错打印错位结果返回1， 否则返回0
    :param req_dict:dict form
    :return:
    """
    if 'error_message' in req_dict:
        print(req_dict['error_message'])
        return 1
    else:
        return 0

def getinfo(req_dict):
    """
    从req_dict中得到文本信息
    :return: str
    """
    # show attributes
    face_attributes = []
    for face in req_dict['faces']:
        if 'attributes' in face.keys():
            face_attributes.append(face['attributes'])
    #print(face_attributes)
    text = ""
    for each in face_attributes:
        if 'gender' in each.keys():
            text += "Gender: " + str(each['gender']['value']) + " "
        if 'age' in each.keys():
            text += "Age: " + str(each['age']['value']) + "\n"
        if 'beauty' in each.keys():
            text += "Male_Score: " + str(each['beauty']['male_score']) + " "
            text += "Female_Score: " + str(each['beauty']['female_score']) + " "
    print(text)
    return text

def draw_rectangle(face_rectangles, origin_filepath, new_filepath):
    """
    从face_rectangles中画出矩形并保存./rectangle/"new_filename.jpg"下
    :return:
    """
    # draw rectangle and save img
    img = cv2.imread(origin_filepath)
    for i in face_rectangles:
        w = i['width']
        t = i['top']
        l = i['left']
        h = i['height']
        cv2.rectangle(img, (l, t), (w + l, h + t), (0, 0, 255), 2)
    cv2.imwrite(new_filepath, img)

def transfer_graph(filepath):
    img = cv2.imread(filepath, -1)

    #按高度等比例缩放图片
    height = img.shape[0]
    width = img.shape[1]
    fixed_width = int(width * 400/height)
    img = cv2.resize(img, (fixed_width, 400), interpolation=cv2.INTER_CUBIC)

    height, width, channel = img.shape
    bytesPerLine = 3 * width
    qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
    return qImg

class SignalObj(QObject):
    """
    定义一个信号类,发送变更窗口信息给MainWindow
    """
    sendMsg = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

    def run(self, choice):
        self.sendMsg.emit(choice)

class Welcome_Window(QWidget):
    """
    初始界面类：
    提供选项
    """
    def __init__(self, parent=None):
        super(Welcome_Window, self).__init__(parent)
        self.send = SignalObj()
        self.init_UI()

    def init_UI(self):
        # combobox init
        self.First_Select = QComboBox(self)
        self.First_Select.addItem('--Basic--')
        self.First_Select.addItems(['人脸识别', '场景识别', '人脸融合'])
        self.First_Select.currentIndexChanged.connect(self.Second_change)

        self.Second_Select = QComboBox(self)
        self.Second_Select.addItem('--Second--')
        # btn init
        self.confirm_btn = QPushButton('Confirm', self)
        self.confirm_btn.clicked.connect(self.Confirm)
        self.confirm_btn.setFixedSize(1000, 100)
        # layout
        self.grid = QGridLayout()
        self.grid.addWidget(self.First_Select, 1, 0, 2, 2)
        self.grid.addWidget(self.Second_Select, 2, 0, 2, 2)
        self.grid.addWidget(self.confirm_btn, 3, 0, 2, 2)
        self.setLayout(self.grid)

    def Second_change(self):
        """
        根据第一个下拉框的实时值改变第二个下拉框的值
        :return: none
        """
        option = self.First_Select.currentText()
        self.Second_Select.clear()
        if option == '人脸识别':
            self.Second_Select.addItems(['Face-Detect', 'Face-Compare'])
        elif option == '场景识别':
            self.Second_Select.addItems(['Scene-Detect'])
        elif option == '人脸融合':
            self.Second_Select.addItems(['Face-Merge'])

    def Confirm(self):
        """
        确认选择，调用self.send以dict形式发送option1，option2给MainWindow
        :return: none
        """
        option1 = self.First_Select.currentText()
        option2 = self.Second_Select.currentText()
        choice = {'option1': option1, 'option2': option2}
        self.send.run(choice)

class Detect_Window(QWidget):
    """
    Detect界面类：
    检测图片中包含最大人脸
    以对比图的形式呈现，并给出对人脸的分析数据（gender，age，beauty（可更改为其他参数））
    """
    def __init__(self, parent=None):
        super(Detect_Window, self).__init__(parent) #important
        #self.img_origin = np.ndarray(())
        #self.img_new = np.ndarray(())
        self.send = SignalObj()
        self.init_UI()

    def init_UI(self):
        #component
        self.graph_origin = QLabel()
        self.graph_new = QLabel()
        self.graph_info = QLabel()

        self.upload_btn = QPushButton("Upload", self)
        self.upload_btn.clicked.connect(self.upload)

        self.return_btn = QPushButton('Return', self)
        self.return_btn.clicked.connect(self.back)

        # layout
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.graph_origin, 0, 0, 3, 4)
        self.layout.addWidget(self.graph_new, 0, 4, 3, 4)
        self.layout.addWidget(self.graph_info, 4, 0, 1, 1)
        self.layout.addWidget(self.upload_btn, 5, 0, 2, 2)
        self.layout.addWidget(self.return_btn, 5, 8, 2, 2)
        self.setLayout(self.layout)

    def upload(self):
        """
        调用QFileDialog上传图片文件，并调用detect_api得到dict形式的response
        :return: none
        """
        #get file
        self.origin_filepath, filetype = QFileDialog.getOpenFileName(
            self, "选取文件", "./", "All Files (*);;JPG Files (*.jpg);;PNG Files (*.png)")  # 设置文件扩展名过滤,注意用双分号间隔
        print(self.origin_filepath)
        if self.origin_filepath is '':
            return

        #使用Detct api
        self.req_dict = func.detect(self.origin_filepath)
        if(print_error(self.req_dict)):
            return

        #analysis on req_dict
        self.detect_analyze()
        self.detect_show()

    def detect_analyze(self):
        """
        分析response,提取图片的人脸矩形框和信息,将画出的矩形框人脸照片以jpg保存
        信息保存在self.text, 照片存为./temp_images/images_detected.jpg
        :return:
        """
        self.text = getinfo(self.req_dict)

        self.new_filepath = './rectangles/images_detected.jpg'
        # get rectangles
        face_rectangles = []
        for face in self.req_dict['faces']:
            if 'face_rectangle' in face.keys():
                face_rectangles.append(face['face_rectangle'])

        draw_rectangle(face_rectangles, self.origin_filepath, self.new_filepath)

    def detect_show(self):
        # 显示文本信息
        self.graph_info.setText(self.text)

        #读取图片
        #self.img_origin = cv2.imread(self.origin_filepath, -1)
        #self.img_new = cv2.imread(self.new_filepath, -1)

        #print(self.img_origin.size, self.img_new.size)


        # 将Qimage显示出来
        self.graph_origin.setPixmap(QPixmap.fromImage(transfer_graph(self.origin_filepath)))
        self.graph_new.setPixmap(QPixmap.fromImage(transfer_graph(self.new_filepath)))

    def back(self):
        """
        回到welcome界面
        :return:
        """
        self.send.run({'option1': '0', 'option2': '0'})


class Compare_Window(QWidget):
    """
    比较两张人脸是否为同一个人，选取为图片中最大人脸，给出置信度，越大越可信
    """
    def __init__(self, parent=None):
        super(Compare_Window, self).__init__(parent) #important
        self.img_1 = np.ndarray(())
        self.img_2 = np.ndarray(())
        self.send = SignalObj()
        self.init_UI()

    def init_UI(self):
        #component
        self.graph_1 = QLabel()
        self.graph_2 = QLabel()
        self.graph_info = QLabel()

        self.upload_btn = QPushButton("Upload Two Files", self)
        self.upload_btn.clicked.connect(self.upload)

        self.return_btn = QPushButton('Return', self)
        self.return_btn.clicked.connect(self.back)

        # layout
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.graph_1, 0, 0, 3, 4)
        self.layout.addWidget(self.graph_2, 0, 4, 3, 4)
        self.layout.addWidget(self.graph_info, 4, 0, 1, 1)
        self.layout.addWidget(self.upload_btn, 5, 0, 2, 2)
        self.layout.addWidget(self.return_btn, 5, 8, 2, 2)
        self.setLayout(self.layout)

    def upload(self):
        """
        上传两张图片
        :return:
        """
        # get file
        #考虑边界！
        self.filepaths, filetype = QFileDialog.getOpenFileNames(self,
                  "多文件选择",
                  "./",
                  "All Files (*);;Text Files (*.txt)")
        #if len(self.filepaths) >= 3:

        print(self.filepaths)
        if len(self.filepaths) != 2:
            return

        # 使用Detct api
        self.req_dict = func.compare(self.filepaths[0], self.filepaths[1])
        if (print_error(self.req_dict)):
            return

        # analysis on req_dict
        self.compare_analyze()
        self.compare_show()

    def compare_analyze(self):
        # 读取confidence
        self.text = "Confidence: " + str(self.req_dict['confidence']) + " (该数值越大越像，范围[0, 100])"

        self.new_filepaths = ['./rectangles/compare_1.jpg', './rectangles/compare_2.jpg']
        #get rectangles
        face_rectangles = []
        for face in self.req_dict['faces1']:
            if 'face_rectangle' in face.keys():
                face_rectangles.append(face['face_rectangle'])
        draw_rectangle(face_rectangles, self.filepaths[0], self.new_filepaths[0])

        face_rectangles = []
        for face in self.req_dict['faces2']:
            if 'face_rectangle' in face.keys():
                face_rectangles.append(face['face_rectangle'])
        draw_rectangle(face_rectangles, self.filepaths[1], self.new_filepaths[1])
        print("done")

    def compare_show(self):
        #显示文本
        self.graph_info.setText(self.text)
        #显示图像
        self.graph_1.setPixmap(QPixmap.fromImage(transfer_graph(self.new_filepaths[0])))
        self.graph_2.setPixmap(QPixmap.fromImage(transfer_graph(self.new_filepaths[1])))

    def back(self):
        """
        回到welcome界面
        :return:
        """
        self.send.run({'option1': '0', 'option2': '0'})


class Scene_Window(QWidget):
    """
    场景检测：场景（置信度）+多个物体（置信度）
    """
    def __init__(self, parent=None):
        super(Scene_Window, self).__init__(parent) #important
        self.send = SignalObj()
        self.init_UI()

    def init_UI(self):
        #component
        self.graph = QLabel()
        self.graph_info = QLabel()

        self.upload_btn = QPushButton("Upload", self)
        self.upload_btn.clicked.connect(self.upload)

        self.return_btn = QPushButton('Return', self)
        self.return_btn.clicked.connect(self.back)

        # layout
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.graph, 0, 0, 3, 4)
        self.layout.addWidget(self.graph_info, 0, 4, 3, 4)
        self.layout.addWidget(self.upload_btn, 4, 0, 2, 2)
        self.layout.addWidget(self.return_btn, 4, 8, 2, 2)
        self.setLayout(self.layout)

    def upload(self):
        """
        上传场景图片，调用detect_scene_api
        :return:
        """
        # get file
        self.filepath, filetype = QFileDialog.getOpenFileName(
            self, "选取文件", "./", "All Files (*);;JPG Files (*.jpg);;PNG Files (*.png)")  # 设置文件扩展名过滤,注意用双分号间隔
        print(self.filepath)
        if self.filepath is '':
            return

        #使用api
        self.req_dict = func.detect_scence(self.filepath)

        self.scene_show()
        #analysis

    def scene_show(self):
        """
        show info
        :return:
        """
        if 'scenes' in self.req_dict:
            scenes = self.req_dict['scenes'][0]
            self.text = 'Scene: ' + scenes['value'] + '(' + str(scenes['confidence']) + ')' + '\n'
        else:
            self.text = 'Scene: None' + '\n'

        if 'objects' in self.req_dict:
            self.text += 'Objects: '
            objects_list = self.req_dict['objects']
            for each in objects_list:
                self.text += each['value'] + '(' + str(each['confidence']) + ')' + '\n'
        else:
            self.text += 'Objects: None' + '\n'
        print(self.text)

        #显示文本
        self.graph_info.setText(self.text)
        #显示图片
        self.graph.setPixmap(QPixmap.fromImage(transfer_graph(self.filepath)))

    def back(self):
        """
        回到welcome界面
        :return:
        """
        self.send.run({'option1': '0', 'option2': '0'})


class Merge_Window(QWidget):
    """
    Merge界面类
    传入template,merge图片
    显示人脸融合后的图片
    """
    def __init__(self, parent=None):
        super(Merge_Window, self).__init__(parent)
        self.send = SignalObj()
        self.template_filepath = ""
        self.merge_filepath = ""

        self.init_UI()

    def init_UI(self):
        #component
        self.graph_merge = QLabel()
        self.graph_template = QLabel()
        self.graph_result = QLabel()

        self.merge_info = QLabel()
        self.template_info = QLabel()
        self.result_info = QLabel()

        self.upload1_btn = QPushButton("Upload Template Graph", self)
        self.upload1_btn.clicked.connect(self.upload1)

        self.upload2_btn = QPushButton("Upload Merge Graph", self)
        self.upload2_btn.clicked.connect(self.upload2)

        self.return_btn = QPushButton('Return', self)
        self.return_btn.clicked.connect(self.back)

        # layout
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.graph_template, 0, 0, 3, 4)
        self.layout.addWidget(self.graph_result, 0, 4, 3, 4)
        self.layout.addWidget(self.graph_merge, 0, 8, 3, 4)

        self.layout.addWidget(self.template_info, 4, 0, 3, 2)
        self.layout.addWidget(self.result_info, 4, 4, 3, 2)
        self.layout.addWidget(self.merge_info, 4, 8, 3, 2)

        self.layout.addWidget(self.upload1_btn, 7, 0, 2, 2)
        self.layout.addWidget(self.upload2_btn, 7, 4, 2, 2)
        self.layout.addWidget(self.return_btn, 7, 8, 2, 2)
        self.setLayout(self.layout)

    def upload1(self):
        """
        传入模板图,self.template_filepath
        :return:
        """
        self.template_filepath, filetype = QFileDialog.getOpenFileName(
            self, "选取文件", "./", "All Files (*);;JPG Files (*.jpg);;PNG Files (*.png)")  # 设置文件扩展名过滤,注意用双分号间隔
        print(self.template_filepath)
        if self.template_filepath is '':
            return

        if self.template_filepath is not '' and self.merge_filepath is not '':
            self.merge()
            self.show_graph()
            self.show_info()

    def upload2(self):
        """
        传入merge图，并得到最终结果
        :return:
        """
        self.merge_filepath, filetype = QFileDialog.getOpenFileName(
            self, "选取文件", "./", "All Files (*);;JPG Files (*.jpg);;PNG Files (*.png)")  # 设置文件扩展名过滤,注意用双分号间隔
        print(self.merge_filepath)
        if self.merge_filepath is '':
            return

        if self.template_filepath is not '' and self.merge_filepath is not '':
            self.merge()
            self.show_graph()
            self.show_info()

    def merge(self):
        """
        调用merge_api
        :return:
        """
        #调用api
        self.req_dict = func.merge(self.template_filepath, self.merge_filepath)
        if(print_error(self.req_dict)):
            return

        #存储结果图片
        self.result_filepath = './temp_images/result.jpg'
        merge_file = open(self.result_filepath, 'wb')
        imgData = base64.b64decode(self.req_dict['result'])
        merge_file.write(imgData) #have sth to write about
        merge_file.close()



    def show_graph(self):
        # 将Qimage显示出来
        self.graph_template.setPixmap(QPixmap.fromImage(transfer_graph(self.template_filepath)))
        self.graph_merge.setPixmap(QPixmap.fromImage(transfer_graph(self.merge_filepath)))
        self.graph_result.setPixmap(QPixmap.fromImage(transfer_graph(self.result_filepath)))

    def show_info(self):
        """
        得到template,merge,result图片的detect info并显示
        :return:
        """
        #调用api
        req_dict_template = func.detect(self.template_filepath)
        if(print_error(req_dict_template)):
            return

        req_dict_merge = func.detect(self.merge_filepath)
        if(print_error(req_dict_merge)):
            return

        req_dict_result = func.detect(self.result_filepath)
        if(print_error(req_dict_result)):
            return

        #显示文本信息
        self.template_info.setText(getinfo(req_dict_template))
        self.merge_info.setText(getinfo(req_dict_merge))
        self.result_info.setText(getinfo(req_dict_result))

    def back(self):
        self.send.run({'option1': '0', 'option2': '0'})


