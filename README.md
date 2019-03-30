# HW for Python using API from Face++
*需要从[Face++](https://console.faceplusplus.com.cn/documents/)上获取key与secret*
# 功能和使用说明 
本程序通过调用Face++的4个API，并使用PYQT5以GUI界面的形式呈现，实现了
1. * 人脸识别-Detect：*
  传入人脸检测及人脸信息识别（性别，年龄，颜值评分）。
2. * 人脸识别-Compare：*
  将两个人脸进行对比，判断是否为同一个人，并给出置信度[0,100]。
3. *场景识别*
  分析上传的场景图，识别图片场景和图片中的物品，并给出相应置信度。
4. *人脸融合*
  上传模板图和人脸图，检测人脸并给出融合后的图片和对应信息。

## 使用说明：本程序分为若干不同界面，每个界面对应不同的功能
# Welcome Page：
进入程序后的选择界面，通过两个下拉框选择所需要的功能，使用Confirm确认。

# Detect Page: 
1. 在Welcome Page中选择“人脸识别”-“Face-Detect”进入。
2. 使用“Return”按键返回Welcome Page。
3. 使用“Upload”按键上传需要识别的人脸图片（免费API只可识别图中占比最大的人脸）程序给出识别前后的对比图及分析信息。

# Compare Page：
1. 在Welcome Page中选择“人脸识别”-“Face-Compare”进入。
2. 使用“Return”按键返回Welcome Page。
3. 使用“Upload Two Files”上传两人脸图片（需要一次性传两张，否则不会进行分析），程序给出两张人脸及其为同一人的置信度。

# Scene Page：
1. 在Welcome Page中选择“场景识别”-“Scene -Detect”进入。
2. 使用“Return”按键返回Welcome Page。
3. 使用“Upload”按键上传场景图，程序给出原图，识别图片场景与主体及其对应置信度。

# Merge Page：
1. 在Welcome Page中选择“人脸融合”-“Face-Merge”进入。
2. 使用“Return”按键返回Welcome Page。
3. 使用“Upload Template Graph”上传融合模板图，使用“Upload Merge Graph”上传融合图。两张图片上传后程序给出三张图片，分别为Template Graph和Merge Graph检测人脸后的图片，以及融合后的图片，并相应的给出对应人脸图片的信息。

