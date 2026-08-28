# AI 开发资源库 - 完整索引

**更新日期**: 2026-05-11 16:30:00
**@author liuhao**

---

> 旧版资源总览（2026-05-11）。当前 `E:\aimodel` 的目录用途和文档入口请查看 [README.md](README.md) 与 [SKILLS_INDEX.md](SKILLS_INDEX.md)；本文件不再作为当前统计依据。

## 📊 资源统计

| 类别 | 仓库数 | 总 Stars |
|------|--------|---------|
| Claude 指南 | 3 | 106,651 ⭐ |
| Vue 技能 | 1 | 2,337 ⭐ |
| 技能增强 | 5 | 132,774 ⭐ |
| 安全工具 | 1 | 67,060 ⭐ |
| 系统设计 | 1 | 345,139 ⭐ |
| AI工具 | 4 | 30,000+ ⭐ |
| **总计** | **15** | **690,000+ ⭐** |

---

## 🎯 Claude 指南系列

### 1. forrestchang/andrej-karpathy-skills 🔥🔥🔥
- **Stars**: 103,365
- **本地**: `E:/aimodel/claude-guides-full/`

### 2. JuliusBrussee/caveman 🪨
- **Stars**: 51,500
- **效果**: 减少 75% Token 输出
- **本地**: `E:/aimodel/caveman-full/`

---

## 🤖 AI工具系列 (2026-05-11新增)

### 1. metacraft-labs/codetracer
- **功能**: 时间旅行调试器
- **语言**: Nim + Rust
- **本地**: `E:/aimodel/codetracer/`
- **GitHub**: https://github.com/metacraft-labs/codetracer
- **特性**: 录制程序执行，前后回放调试

### 2. heygen-com/hyperframes
- **功能**: HTML视频渲染框架
- **语言**: TypeScript + GSAP
- **本地**: `E:/aimodel/hyperframes/`
- **GitHub**: https://github.com/heygen-com/hyperframes
- **特性**: "视频即代码"，AI代理友好

### 3. nanobrowser/nanobrowser
- **功能**: AI网页自动化Chrome扩展
- **语言**: React + LangChain
- **本地**: `E:/aimodel/nanobrowser/`
- **GitHub**: https://github.com/nanobrowser/nanobrowser
- **特性**: OpenAI Operator开源替代

### 4. winshining/nginx-http-flv-module
- **功能**: HTTP-FLV直播流媒体
- **语言**: C
- **本地**: `E:/aimodel/nginx-http-flv-module/`
- **GitHub**: https://github.com/winshining/nginx-http-flv-module
- **特性**: 低延迟直播 (1-3秒)

---

## 📺 直播流媒体系列 (2026-05-11新增)

### 浩然音乐直播架构

| 节点 | 角色 | 协议 | 延迟 |
|------|------|------|------|
| node4 | 普通直播 | HTTP-FLV | 1-3s |
| node5 | 高保真直播 | HLS | 2-10s |
| node6 | 低延迟直播 | WebRTC | <500ms |

### 本地优化版
- **路径**: `E:/aimodel/nginx-live-optimized/`
- **优化点**:
  - 零拷贝发送
  - 分片锁 (32分片)
  - 多级GOP缓存
  - HTTP/2支持

---

## 📁 本地目录结构

```
E:/aimodel/
├── README.md                           # 本索引文件
├── LIVE_STREAMING.md                   # 直播架构文档
│
├── claude-guides/                       # Claude 指南
├── claude-guides-full/                  # 完整仓库
├── caveman-full/                        # Caveman 完整仓库
│
├── codetracer/                          # 时间旅行调试器 [新]
├── hyperframes/                         # HTML视频渲染 [新]
├── nanobrowser/                         # AI网页自动化 [新]
├── nginx-http-flv-module/               # 直播流媒体 [新]
├── nginx-live-optimized/                # 直播优化版 [新]
│
├── vue-skills/                          # Vue 技能
├── backend-skills/                      # 后端技能
├── security-tools/                      # 安全工具
└── system-design/                       # 系统设计
```

---

## 🚀 直播服务部署

### node6 配置 (计划)

```bash
# 编译安装
cd /opt
wget http://nginx.org/download/nginx-1.28.0.tar.gz
git clone https://github.com/winshining/nginx-http-flv-module.git

./configure --add-module=/opt/nginx-http-flv-module \
            --with-http_ssl_module \
            --with-http_v2_module
make && sudo make install
```

### 测试命令

```bash
# 推流 (OBS)
rtmp://node6:1935/normal/stream

# 播放 (flv.js)
http://node6/live?app=normal&stream=stream
```

---

**@author liuhao**
**更新时间**: 2026-05-11 16:30:00
