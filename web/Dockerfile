# 使用 Node.js Alpine 官方镜像作为基础镜像
FROM node:alpine

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制项目文件
COPY . .

# 构建 Next.js 应用
RUN npm run build

# 指定容器启动时执行的命令
CMD ["npm", "start"]

# 暴露 3000 端口
EXPOSE 3000
