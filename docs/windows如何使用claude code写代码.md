# Windows电脑如何使用Claude Code编写代码

- 第一步：安装wsl
- 第二步：配置环境变量
- 第三步：配置proxy
- 第四步：安装node
- 第五步：安装claude code

### 安装wsl

```
// 列出已经安装的
wsl --list
// 查看可用版本
wsl --list --online
// 安装
wsl --install XXXX
```

### 配置环境变量

需提前准备ANTHROPIC_BASE_URL和ANTHROPIC_AUTH_TOKEN
```
编辑.bashrc文件，写入
export ANTHROPIC_BASE_URL=https://xxxxxxxx.com
export ANTHROPIC_AUTH_TOKEN=sk-xxxxxxxxxxxxxxxxxxxxxxxx
然后 source ~/.bashrc
```

### 配置proxy（可选）

```
编辑.bashrc文件，写入
export HTTP_PROXY="http://172.23.160.1:7890"
export HTTPS_PROXY="http://172.23.160.1:7890"
export ALL_PROXY="http://172.23.160.1:7890"
然后 source ~/.bashrc
```

### 安装node

```
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo bash -
sudo apt-get install -y nodejs
node --version
```

### 安装claude code

```
npm install -g @anthropic-ai/claude-code
claude --version
```

### 开始使用

```
claude
```




