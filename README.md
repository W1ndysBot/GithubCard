# GithubCard

## 项目简介

GithubCard 是一个用于检测群聊中的 Github 链接并生成仓库卡片的工具。它可以自动识别消息中的 Github 链接，并返回相应的仓库信息卡片。

## 功能

- 自动检测群聊中的 Github 链接
- 生成并发送 Github 仓库的 OpenGraph 卡片
- 支持功能开关，管理员可控制功能的启用和禁用

## 使用方法

1. **功能开关**：在群聊中发送 `gc` 指令以切换 GithubCard 功能的启用状态。只有管理员或授权用户可以执行此操作。

   - 发送 `gc` 后，若功能开启，将收到确认消息 `✅✅✅GithubCard功能已开启`。
   - 再次发送 `gc`，若功能关闭，将收到确认消息 `🚫🚫🚫GithubCard功能已关闭`。

2. **获取 Github 卡片**：在群聊中发送包含 Github 仓库链接的消息，例如 `https://github.com/owner/repo`。
   - 如果功能开启，机器人将自动识别链接并发送相应的 OpenGraph 卡片。

## 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 许可证

本项目采用 GPL-3.0 许可证。详情请参阅 [LICENSE](LICENSE) 文件。
