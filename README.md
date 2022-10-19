Spectrogram-frame linear network and continuous frame sequence for bird sound classification


Here are the official implementation. This study is in the journal Ecological Informatics. You can find it here https://doi.org/10.1016/j.ecoinf.2019.101009 

Please cite if you referred our work.

```
Zhang X, Chen A, Zhou G, et al. Spectrogram-frame linear network and continuous frame sequence for bird sound classification[J]. Ecological Informatics, 2019, 54: 101009.
```

Apache License Version 2.0, January 2004 http://www.apache.org/licenses/




基于 TensorFlow 

项目内容包括：

一个从 www.xeno-canto.org 下载音频数据的网络爬虫
- 下载列表维护，支持断点续传；
- 捕获网络异常，加入重试机制；
- 可根据重试计数更换代理；
- 模块化设计，可根据文件计数器加入动态代理；

一系列音频数据预处理过程
- 从MP3到梅尔频谱图的转换
- 图像标准化，数据增强
- continuous frame sequence 的构建
- 自动化的 batch 生成器

一个音频识别神经网络
- 以上述3D图像帧序列为输入
- 为音频特殊设计的 Spectrogram-frame linear layer
- 一系列结果分析以及可视化方法


环境配置：
- Tensorflow 1.14以上，需要eager模式支持
- librosa，音频处理
- PIL，图像处理
- scipy，图像处理
- matplotlib，绘图
- sklearn，需要用到一些结果分析函数

