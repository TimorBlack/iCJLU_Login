# iCJLU_Login
中国计量大学教学区iCJLU自动连接

参考代码：https://github.com/huxiaofan1223/jxnu_srun 

iCJLU_Login.py-->iCJLU_Login.pyw；

  需先安装库文件：
  
  pip install requests；
  
  pip install win10toast；

使用前先修改config.ini；

  原本写了保存，后来觉得麻烦就删了，直接修改就行；
  
连接iCJLU自动执行；

  搜索并打开 ‘任务计划程序’---‘创建任务’；
  
  ‘常规’---名称随便取一个；
  
  ‘触发器’---‘新建’---‘开始任务’选择‘发生事件时’---‘自定义’中‘新建事件筛选’；
  
  选择‘XML’后勾选‘手动编辑查询’，复制xml.txt中的内容粘贴到此处---‘确定’；

  ‘操作’---‘新建’---‘浏览’找到iCJLU_Login.pyw---‘确定’；
  
  创建完成；
  
# iCJLU_Login.zip
  解压后，修改config.ini，创建计划任务时用iCJLU_Login.exe即可
