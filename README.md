# 🐾 小小动物园 · 亲子任务打卡系统

## 项目简介

一个帮助家长培养孩子日常习惯的 Web 应用。以"动物园员工"为主题，通过任务打卡、盲盒积分、宠物养成、数学游戏等有趣的方式激励孩子完成每日任务。

## 技术栈

- Python Flask
- SQLite
- HTML/CSS/JavaScript
- Docker

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

### 方式三：在线访问

[部署链接]（部署后填写）

## 首次使用

1. 打开应用，点击"首次使用？创建管理员账号"
2. 创建家长账号
3. 在设置中创建孩子账号
4. 孩子登录开始打卡！

## 核心功能

- **🎯 任务打卡**：家长自定义任务（读书、写字等），孩子每日打卡得积分
- **🎲 盲盒积分**：每次打卡获得随机积分（基准分 ± 波动），充满惊喜
- **🎮 积分商城**：孩子用积分兑换"看 10 分钟手机"等活动
- **🐾 宠物养成**：领养虚拟宠物，喂食、玩耍、抚摸，陪伴成长
- **🧮 数学游戏**：4 个年级的数学题，答对送金币
- **🏆 勋章系统**：完成任务里程碑获得勋章
- **💝 心愿单**：设定积分目标，追踪进度
- **📊 成长周报**：每周自动生成完成率统计

## 安全说明

- 所有密码使用哈希加密存储
- 敏感配置通过环境变量传入
- 请勿将 `.env` 文件提交到代码仓库

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
├── static/             # 静态资源
├── Dockerfile          # 容器构建
└── requirements.txt    # Python 依赖
```

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `SECRET_KEY` | Flask 密钥 | `change-this-in-production` |
| `DATABASE` | 数据库路径 | `data.db` |

## 开发

运行测试：

```bash
python -m pytest tests/ -v
```