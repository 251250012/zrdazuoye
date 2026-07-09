# 🐾 小小动物园 · 亲子任务打卡系统

## 项目简介

一个帮助家长培养孩子日常习惯的 Web 应用。以"小小动物园"为主题，通过任务打卡、盲盒金币、宠物养成、答题闯关等有趣的方式激励孩子完成每日任务。支持 PWA，可添加到手机桌面使用。

## 技术栈

- Python Flask
- SQLite
- HTML/CSS/JavaScript
- Docker
- PWA（Service Worker + Manifest）

## 快速开始

### 方式一：直接运行

```bash
pip install -r requirements.txt
python app.py
```

访问 http://localhost:8080

### 方式二：Docker

```bash
docker build -t family-zoo .
docker run -p 8080:8080 family-zoo
```

## 首次使用

1. 打开应用，点击"首次使用？创建管理员账号"
2. 创建家长账号
3. 在设置中创建孩子账号，选择年级（影响答题难度）
4. 家长在任务管理中创建每日任务
5. 孩子登录开始打卡赚金币！

## 核心功能

- **🎯 任务打卡**：家长自定义任务（读书、写字等），孩子每日打卡获得盲盒金币
- **🎲 盲盒金币**：每次打卡获得随机金币（基准分 ±20%），充满惊喜
- **🐾 宠物养成**：200 金币购买宠物蛋，5 种动物可选，可同时养最多 5 只
- **🖼️ 宠物图片**：每种宠物幼年/成年各有 3 张真实图片，每只宠物长相不同
- **🧮 每日答题**：4 个年级的数学题，每天 10 轮，每轮最多 10 题，答对赚金币
- **🏆 勋章墙**：完成任务里程碑获得勋章
- **📊 成长周报**：每周自动生成完成率统计

## 安全说明

- 所有密码使用哈希加密存储
- 敏感配置通过环境变量传入
- 请勿将 `.env` 文件提交到代码仓库
- 密码全系统唯一，防止账号冲突

## 目录结构

```
├── app.py              # 应用入口
├── config.py           # 配置
├── db.py               # 数据库连接
├── schema.sql          # 数据库建表
├── models.py           # 数据模型
├── auth.py             # 登录认证
├── parent_routes.py    # 家长端路由
├── child_routes.py     # 孩子端路由
├── pet_routes.py       # 宠物路由
├── score_engine.py     # 盲盒积分引擎
├── badge_checker.py    # 勋章检查
├── report_generator.py # 周报生成
├── templates/          # 页面模板
├── static/             # 静态资源（CSS / 图片 / PWA）
├── Dockerfile          # 容器构建
└── requirements.txt    # Python 依赖
```

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `SECRET_KEY` | Flask 密钥 | `dev-secret-key` |
| `DATABASE` | 数据库路径 | `data/data.db` |

## 开发

运行测试：

```bash
python -m pytest tests/ -v
```