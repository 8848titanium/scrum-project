# This is a learning application developed by Group A3.

## Group A3 members:

**Main Beck-end:** Jiawei Guo(8848titanium)

**Front-end Framework:** Jiawei Guo(@8848titanium)

**Deputy Back-end:** Chenyuhan Shen(@chenyuhanjcu), Jiaqi Zhao(@LX-Vincent)

**Front-end Styling:** Fangyu Li(@LiFangYuBIT), Xing Gao(@Xing-Gao-FROM-PRC), Yue Cao(@CP1404-YueCao), Weijun Chew(
@CWJ02), Junwen Zhang(@zhangjunwenzzz)

## Requirements:

* ### Install all modules in requirements.txt

```
$ pip install -r requirments.txt
```

* ### Since db modeling for mysql can't operate without an existed database, please create one in your local environment.

```
CREATE DATABASE IF NOT EXISTS `YourDatabaseName` DEFAULT CHARACTER SET UTF8MB4;
```

* ### You may need to edit the config.py to use your local database.

```
'mysql://username:password@localhost/YourDatabaseName'
```

* ### Initial local database(mysql) with below commands

```
$ flask db init | flask db migrate | flask db upgrade
```

* ### Now run the project!

## How to run:

### 1. run below with python environment activate

```
$ flask run
```

### 2. run api.py as normal Python program

```
$ python api.py
```

### 3. run api.py as flask app in pycharm

![img.png](img.png)